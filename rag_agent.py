
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# All Required Packages
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st


### Data in st session

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "Messages" not in st.session_state:
    st.session_state.messages = []

def process_document(path):


    ## load the PDF file
    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()


    ### Split the document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(docs)

    ## embeddings and vector DB
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_db = InMemoryVectorStore.from_documents(
        documents= docs,
        embedding=embeddings
    )

    vector_db.add_documents(docs)

    ## create a agent - tool , llm, prompt
    llm = ChatGroq(model="openai/gpt-oss-20b")

    @tool
    def retriever_context(query: str):
        """Retrieve documents relevant to query from the knowledge base."""
        context = ""

        docs = vector_db.similarity_search(query=query, k=3)
        for doc in docs:
            context = doc.page_content + "\n\n"

        return context


    system_prompt = """ you are the helpful assisant that give me the answer of my questions
        and always use the 'retriever_context' to fetch relevant information from the knowledge base.
    """


    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retriever_context],
        system_prompt=system_prompt,
        checkpointer =memory
    )

    st.session_state.agent = agent
    st.session_state.document_uploaded = True
### Upload ui
if not st.session_state.document_uploaded:
    uploaded =st.file_uploader(label="Select pdf files", type =["pdf"], accept_multiple_files =True)
    if uploaded:
        with st.spinner("Processing..."):
            path = "./doc_files/"
            for file in uploaded:
                with open(path + file.name, "wb") as f:
                    f.write(file.getvalue())
            process_document(path)
            st.rerun()



### chat ui

if st.session_state.document_uploaded and st.session_state.agent:
    for message in st.session_state.messages:
        role = message.get("role")
        content= message.get("content")
        st.chat_message(role).markdown(content)
   
    query = st.chat_input("ask anything related to uploaded document...")
    if query:
        st.session_state.messages.append({"role":"user", "content":query}) 
        st.chat_message("user").markdown(query)
        response = st.session_state.agent.invoke(
            {"messages":[{"role":"user","content":query}]},
            {"configurable": {"thread_id":1}}
        )

        answer = response["messages"][-1].content
        st.chat_message("ai").markdown(answer)
        st.session_state.messages.append({"role":"ai", "content":answer}) 

