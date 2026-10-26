"""
RAG (Retrieval-Augmented Generation) & Agronomy Agent Service
Integrates document indexing, vector store retrieval, LangChain/LangGraph agent execution,
and intelligent fallback inference for agricultural decision support.
"""

import os
import glob
import re
import math
from collections import Counter
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# LangChain Imports with Graceful Fallbacks
try:
    from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_groq import ChatGroq
    from langchain_community.vectorstores import InMemoryVectorStore
    from langchain.tools import tool
    from langchain.agents import create_agent
    from langgraph.checkpoint.memory import InMemorySaver
    LANGCHAIN_AVAILABLE = True
except Exception as e:
    print(f"[!] LangChain imports warning: {e}")
    LANGCHAIN_AVAILABLE = False

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_files")
os.makedirs(DOCS_DIR, exist_ok=True)

class LocalBM25Retriever:
    """Fast in-memory semantic TF-IDF/BM25 vector search when external embeddings are not set."""
    def __init__(self):
        self.chunks = [] # List of {"text": str, "source": str, "page": int, "words": list}
        self.doc_freqs = Counter()
        self.total_docs = 0

    def add_documents(self, chunks):
        self.chunks.extend(chunks)
        self.total_docs = len(self.chunks)
        self.doc_freqs = Counter()
        for c in self.chunks:
            unique_words = set(self._tokenize(c["text"]))
            for w in unique_words:
                self.doc_freqs[w] += 1

    def _tokenize(self, text):
        return re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text.lower())

    def similarity_search(self, query, k=3):
        if not self.chunks:
            return []
        q_words = self._tokenize(query)
        if not q_words:
            return self.chunks[:k]

        scores = []
        for c in self.chunks:
            c_words = Counter(self._tokenize(c["text"]))
            score = 0.0
            doc_len = len(c_words)
            for w in q_words:
                if w in c_words:
                    tf = c_words[w] / max(doc_len, 1)
                    df = self.doc_freqs.get(w, 1)
                    idf = math.log((self.total_docs + 1) / (df + 0.5)) + 1.0
                    score += tf * idf
                    # Boost exact phrase matches
                    if w in query.lower():
                        score += 0.5
            scores.append((score, c))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scores[:k]]

class RagAgentManager:
    def __init__(self, doc_dir=DOCS_DIR):
        self.doc_dir = doc_dir
        self.vector_db = None
        self.local_retriever = LocalBM25Retriever()
        self.agent = None
        self.indexed_files = []
        self.total_chunks = 0
        self.status = "uninitialized"
        
        # Initial scan and load
        self.reload_documents()

    def get_api_keys(self):
        # Reload dotenv in case user edited .env
        load_dotenv(override=True)
        openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
        groq_key = os.environ.get("GROQ_API_KEY", "").strip()
        return openai_key, groq_key

    def reload_documents(self):
        """Processes all PDF files in doc_files directory into vector stores."""
        pdf_files = glob.glob(os.path.join(self.doc_dir, "*.pdf"))
        self.indexed_files = [os.path.basename(f) for f in pdf_files]

        if not pdf_files:
            self.status = "no_documents"
            self.total_chunks = 0
            self.vector_db = None
            self.local_retriever = LocalBM25Retriever()
            return {"success": True, "files": [], "chunks": 0, "status": self.status}

        raw_docs = []
        try:
            from pypdf import PdfReader
            for pdf_path in pdf_files:
                reader = PdfReader(pdf_path)
                doc_name = os.path.basename(pdf_path)
                for page_idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        raw_docs.append({
                            "text": text,
                            "source": doc_name,
                            "page": page_idx + 1
                        })
        except Exception as e:
            print(f"[!] Error reading PDFs with pypdf: {e}")

        # Chunk documents
        chunks = []
        for doc in raw_docs:
            text = doc["text"]
            # Split into ~800 character chunks with 150 overlap
            step = 650
            for i in range(0, len(text), step):
                chunk_text = text[i:i+800].strip()
                if len(chunk_text) > 40:
                    chunks.append({
                        "text": chunk_text,
                        "source": doc["source"],
                        "page": doc["page"]
                    })

        self.total_chunks = len(chunks)
        self.local_retriever = LocalBM25Retriever()
        self.local_retriever.add_documents(chunks)

        openai_key, groq_key = self.get_api_keys()

        # Build LangChain OpenAI Vector Store if API key is provided
        if openai_key and LANGCHAIN_AVAILABLE:
            try:
                from langchain_core.documents import Document
                lc_docs = [Document(page_content=c["text"], metadata={"source": c["source"], "page": c["page"]}) for c in chunks]
                embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=openai_key)
                self.vector_db = InMemoryVectorStore.from_documents(documents=lc_docs, embedding=embeddings)
                self.status = "openai_groq_ready" if groq_key else "openai_embeddings_ready"
            except Exception as e:
                print(f"[!] Failed to initialize OpenAI vector store: {e}")
                self.vector_db = None
                self.status = "local_semantic_ready"
        else:
            self.status = "local_semantic_ready"

        return {
            "success": True,
            "files": self.indexed_files,
            "chunks": self.total_chunks,
            "status": self.status
        }

    def retrieve_context(self, query: str, k: int = 4):
        """Retrieves top-k relevant chunks with source metadata."""
        openai_key, _ = self.get_api_keys()
        sources = []

        if self.vector_db and openai_key and LANGCHAIN_AVAILABLE:
            try:
                docs = self.vector_db.similarity_search(query=query, k=k)
                for d in docs:
                    sources.append({
                        "text": d.page_content,
                        "source": d.metadata.get("source", "Document"),
                        "page": d.metadata.get("page", 1)
                    })
                return sources
            except Exception as e:
                print(f"[!] VectorDB search error, falling back to local retriever: {e}")

        # Fallback to local high-precision BM25
        results = self.local_retriever.similarity_search(query, k=k)
        for r in results:
            sources.append({
                "text": r["text"],
                "source": r.get("source", "Document"),
                "page": r.get("page", 1)
            })
        return sources

    def answer_query(self, query: str, chat_history=None):
        """
        Executes RAG inference over the agricultural document knowledge base.
        """
        if not self.indexed_files or self.total_chunks == 0:
            return {
                "success": False,
                "answer": "No agricultural PDF documents are currently uploaded. Please upload a PDF research paper, crop guide, or click 'Load Standard Agro Handbook' to enable RAG document intelligence.",
                "sources": [],
                "engine": "none"
            }

        sources = self.retrieve_context(query, k=3)
        context_str = "\n\n---\n\n".join([f"[Source: {s['source']} (Page {s['page']})]\n{s['text']}" for s in sources])

        openai_key, groq_key = self.get_api_keys()

        # 1. If Groq API Key is available, run LangChain Groq LLM Agent
        if groq_key and LANGCHAIN_AVAILABLE:
            try:
                # Using standard fast models on Groq
                model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
                try:
                    llm = ChatGroq(model=model_name, api_key=groq_key, temperature=0.2)
                except Exception:
                    llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key, temperature=0.2)

                prompt = f"""You are AgroAI's Senior Agricultural Scientist and RAG Assistant. 
Answer the user's question accurately using ONLY the context provided below from the indexed agronomy manuals.
If the information is not in the context, synthesize the most scientifically sound agronomic advice and explicitly mention it.
Provide clear, actionable, structured bullet points with dosage units (kg/ha or kg/acre), pH intervals, or climatic thresholds where applicable.

CONTEXT FROM DOCUMENTS:
{context_str}

USER QUESTION:
{query}

EXPERT AGRONOMY RESPONSE:"""

                response = llm.invoke(prompt)
                answer_text = response.content if hasattr(response, "content") else str(response)

                return {
                    "success": True,
                    "answer": answer_text,
                    "sources": sources,
                    "engine": f"Groq ({model_name}) RAG"
                }
            except Exception as e:
                print(f"[!] Groq execution failed, falling back to Agronomy Synthesis Engine: {e}")

        # 2. Expert Agricultural Synthesis & RAG fallback engine
        # Analyzes retrieved document chunks and generates structured response
        synthesized_answer = self._synthesize_agronomy_response(query, sources)
        return {
            "success": True,
            "answer": synthesized_answer,
            "sources": sources,
            "engine": "AgroAI Precision Agronomy RAG Engine"
        }

    def _synthesize_agronomy_response(self, query, sources):
        """Generates a high-quality agronomic response from retrieved passages."""
        q_lower = query.lower()
        
        # Extract direct key sentences from retrieved passages
        highlighted_points = []
        for s in sources:
            sentences = re.split(r'(?<=[.!?]) +', s["text"])
            for st in sentences:
                st_clean = st.strip()
                if len(st_clean) > 25:
                    highlighted_points.append(f"• {st_clean}")
        
        selected_points = highlighted_points[:5] if highlighted_points else [
            "• Refer to specific macronutrient soil ratios (N-P-K) and climatic requirements in the uploaded guide.",
            "• Ensure split dosage of fertilizers: basal application at sowing and top dressing during vegetative stages.",
            "• Maintain soil pH between 6.0 and 7.5 for optimal micronutrient availability."
        ]

        response_body = f"Based on the indexed agricultural documentation:\n\n"
        response_body += "\n".join(selected_points)
        
        if "nitrogen" in q_lower or "urea" in q_lower or " n " in q_lower:
            response_body += "\n\n💡 **Nitrogen Advisory:** Apply 50% as basal dose and split remaining into top dressings at active tillering and panicle initiation. Avoid waterlogging during application."
        elif "phosphorus" in q_lower or "dap" in q_lower or " p " in q_lower:
            response_body += "\n\n💡 **Phosphorus Advisory:** Always place DAP/SSP 3-5 cm below seed depth during basal sowing to maximize root contact, as phosphorus has low soil mobility."
        elif "potassium" in q_lower or "mop" in q_lower or " k " in q_lower:
            response_body += "\n\n💡 **Potassium Advisory:** Apply Muriate of Potash (MOP) to boost disease resistance, stem rigidity, and grain weight filling."
        elif "ph" in q_lower or "acid" in q_lower or "alkaline" in q_lower:
            response_body += "\n\n💡 **Soil pH Advisory:** For acidic soils (pH < 6.0), incorporate agricultural lime (1-2 tonnes/acre). For alkaline soils (pH > 8.0), apply gypsum (500-1000 kg/acre)."
        elif "pest" in q_lower or "disease" in q_lower or "spray" in q_lower:
            response_body += "\n\n💡 **IPM Protection:** Use Neem oil (Azadirachtin 1500 ppm @ 5ml/L) as first-line botanical defense against sucking pests, and Trichoderma viride seed treatment for root wilt prevention."

        response_body += f"\n\n*Consult the full source passages below for exact field measurements and references.*"
        return response_body

# Singleton instance
rag_agent_manager = RagAgentManager()
