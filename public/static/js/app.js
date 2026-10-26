/**
 * AgroAI - Planet-Friendly Gardening & Precision Agriculture Frontend Engine
 * Integrates Ensemble ML Inference, RAG Document Assistant, Radar Match Visuals,
 * Soil Diagnostics, Weather Telemetry, and Multi-Model Analytics.
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // Global State & Chart Handles
    // -------------------------------------------------------------------------
    let radarChartInstance = null;
    let featureChartInstance = null;
    let allCropsData = {};
    let presetsData = {};
    let batchPredictionsData = [];
    let ragChatHistory = [];
    let ragStatusData = {};

    // -------------------------------------------------------------------------
    // Theme Management (Light / Dark)
    // -------------------------------------------------------------------------
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const savedTheme = localStorage.getItem('agroai_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('agroai_theme', nextTheme);
            updateChartTheme();
        });
    }

    // -------------------------------------------------------------------------
    // Navigation Tabs & Global Switcher
    // -------------------------------------------------------------------------
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');

    window.switchTab = (tabId) => {
        navTabs.forEach(t => {
            if (t.getAttribute('data-tab') === tabId) {
                t.classList.add('active');
            } else {
                t.classList.remove('active');
            }
        });

        tabContents.forEach(c => {
            if (c.id === tabId) {
                c.classList.add('active');
            } else {
                c.classList.remove('active');
            }
        });

        // Specific Tab Lifecycle triggers
        if (tabId === 'tab-analytics') {
            loadAnalyticsDashboard();
        } else if (tabId === 'tab-crops' && Object.keys(allCropsData).length === 0) {
            loadCropsCatalog();
        } else if (tabId === 'tab-rag') {
            loadRagStatus();
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTabId = tab.getAttribute('data-tab');
            switchTab(targetTabId);
        });
    });

    // Jump from Winner Card to Fertilizer Doctor
    const jumpBtn = document.getElementById('jumpToFertilizerDoctorBtn');
    if (jumpBtn) {
        jumpBtn.addEventListener('click', () => switchTab('tab-fertilizer'));
    }

    // Floating Chat Trigger
    const floatingTrigger = document.getElementById('floatingChatTrigger');
    if (floatingTrigger) {
        floatingTrigger.addEventListener('click', () => switchTab('tab-rag'));
    }

    // -------------------------------------------------------------------------
    // Sliders & Number Inputs Synchronization
    // -------------------------------------------------------------------------
    const paramControls = [
        { slider: 'sliderN', input: 'inputN', badge: 'badgeN', type: 'nutrient' },
        { slider: 'sliderP', input: 'inputP', badge: 'badgeP', type: 'nutrient' },
        { slider: 'sliderK', input: 'inputK', badge: 'badgeK', type: 'nutrient' },
        { slider: 'sliderPH', input: 'inputPH', badge: 'badgePH', type: 'ph' },
        { slider: 'sliderTemp', input: 'inputTemp', badge: 'badgeTemp', type: 'temp' },
        { slider: 'sliderHumidity', input: 'inputHumidity', badge: 'badgeHumidity', type: 'humidity' },
        { slider: 'sliderRainfall', input: 'inputRainfall', badge: 'badgeRainfall', type: 'rainfall' }
    ];

    paramControls.forEach(ctrl => {
        const sliderEl = document.getElementById(ctrl.slider);
        const inputEl = document.getElementById(ctrl.input);
        const badgeEl = document.getElementById(ctrl.badge);

        if (!sliderEl || !inputEl) return;

        const updateBadge = (val) => {
            const num = parseFloat(val);
            if (!badgeEl) return;
            if (ctrl.type === 'nutrient') {
                if (num < 35) badgeEl.textContent = 'Low';
                else if (num < 85) badgeEl.textContent = 'Medium';
                else badgeEl.textContent = 'High';
            } else if (ctrl.type === 'ph') {
                if (num < 5.8) badgeEl.textContent = 'Acidic';
                else if (num > 7.5) badgeEl.textContent = 'Alkaline';
                else badgeEl.textContent = 'Neutral';
            } else if (ctrl.type === 'temp') {
                if (num < 18) badgeEl.textContent = 'Cool';
                else if (num < 30) badgeEl.textContent = 'Warm';
                else badgeEl.textContent = 'Hot';
            } else if (ctrl.type === 'humidity') {
                if (num < 45) badgeEl.textContent = 'Dry';
                else if (num < 75) badgeEl.textContent = 'Moderate';
                else badgeEl.textContent = 'Humid';
            } else if (ctrl.type === 'rainfall') {
                if (num < 65) badgeEl.textContent = 'Low';
                else if (num < 160) badgeEl.textContent = 'Moderate';
                else badgeEl.textContent = 'High';
            }
        };

        sliderEl.addEventListener('input', (e) => {
            inputEl.value = e.target.value;
            updateBadge(e.target.value);
        });

        inputEl.addEventListener('input', (e) => {
            sliderEl.value = e.target.value;
            updateBadge(e.target.value);
        });

        updateBadge(inputEl.value);
    });

    // Reset Form
    const resetBtn = document.getElementById('resetParamsBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            document.getElementById('sliderN').value = 90; document.getElementById('inputN').value = 90;
            document.getElementById('sliderP').value = 42; document.getElementById('inputP').value = 42;
            document.getElementById('sliderK').value = 43; document.getElementById('inputK').value = 43;
            document.getElementById('sliderPH').value = 6.5; document.getElementById('inputPH').value = 6.5;
            document.getElementById('sliderTemp').value = 23.5; document.getElementById('inputTemp').value = 23.5;
            document.getElementById('sliderHumidity').value = 82; document.getElementById('inputHumidity').value = 82;
            document.getElementById('sliderRainfall').value = 202; document.getElementById('inputRainfall').value = 202;
            paramControls.forEach(c => {
                const el = document.getElementById(c.input);
                if (el) el.dispatchEvent(new Event('input'));
            });
        });
    }

    // -------------------------------------------------------------------------
    // Regional Agro Presets & Weather Telemetry
    // -------------------------------------------------------------------------
    fetch('/api/presets')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                presetsData = data.presets;
                const selectEl = document.getElementById('regionalPresetSelect');
                if (selectEl) {
                    for (const [key, preset] of Object.entries(presetsData)) {
                        const opt = document.createElement('option');
                        opt.value = key;
                        opt.textContent = preset.name;
                        selectEl.appendChild(opt);
                    }
                }
            }
        })
        .catch(err => console.error('Presets loading failed:', err));

    window.applyPreset = (presetKey) => {
        const preset = presetsData[presetKey];
        if (!preset) return;

        // Switch to recommender tab if on another tab
        switchTab('tab-recommender');

        document.getElementById('inputN').value = preset.N;
        document.getElementById('sliderN').value = preset.N;
        document.getElementById('inputP').value = preset.P;
        document.getElementById('sliderP').value = preset.P;
        document.getElementById('inputK').value = preset.K;
        document.getElementById('sliderK').value = preset.K;
        document.getElementById('inputPH').value = preset.ph;
        document.getElementById('sliderPH').value = preset.ph;
        document.getElementById('inputTemp').value = preset.temperature;
        document.getElementById('sliderTemp').value = preset.temperature;
        document.getElementById('inputHumidity').value = preset.humidity;
        document.getElementById('sliderHumidity').value = preset.humidity;
        document.getElementById('inputRainfall').value = preset.rainfall;
        document.getElementById('sliderRainfall').value = preset.rainfall;
        document.getElementById('weatherCityInput').value = preset.city;

        paramControls.forEach(c => {
            const el = document.getElementById(c.input);
            if (el) el.dispatchEvent(new Event('input'));
        });

        // Trigger prediction
        document.getElementById('cropPredictForm').dispatchEvent(new Event('submit'));
    };

    const presetSelect = document.getElementById('regionalPresetSelect');
    if (presetSelect) {
        presetSelect.addEventListener('change', (e) => {
            if (e.target.value) applyPreset(e.target.value);
        });
    }

    // Weather Search Button
    const fetchWeatherBtn = document.getElementById('fetchWeatherBtn');
    if (fetchWeatherBtn) {
        fetchWeatherBtn.addEventListener('click', () => {
            const city = document.getElementById('weatherCityInput').value.trim();
            if (!city) {
                alert('Please enter a city name (e.g., Ludhiana, Nagpur, Shimla, Bangalore)');
                return;
            }
            fetchWeatherBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Fetching...';
            if (window.lucide) lucide.createIcons();

            fetch(`/api/weather?city=${encodeURIComponent(city)}`)
                .then(res => res.json())
                .then(w => {
                    fetchWeatherBtn.innerHTML = '<i data-lucide="cloud-sun"></i> <span>Fetch Weather</span>';
                    if (window.lucide) lucide.createIcons();
                    if (w.success) {
                        document.getElementById('inputTemp').value = w.temperature;
                        document.getElementById('sliderTemp').value = w.temperature;
                        document.getElementById('inputHumidity').value = w.humidity;
                        document.getElementById('sliderHumidity').value = w.humidity;
                        document.getElementById('inputRainfall').value = w.rainfall;
                        document.getElementById('sliderRainfall').value = w.rainfall;
                        document.getElementById('weatherCityInput').value = w.city;

                        paramControls.forEach(c => {
                            const el = document.getElementById(c.input);
                            if (el) el.dispatchEvent(new Event('input'));
                        });
                    }
                })
                .catch(err => {
                    fetchWeatherBtn.innerHTML = '<i data-lucide="cloud-sun"></i> <span>Fetch Weather</span>';
                    if (window.lucide) lucide.createIcons();
                    alert('Could not fetch weather: ' + err.message);
                });
        });
    }

    // Auto-locate GPS Weather
    const autoLocateBtn = document.getElementById('autoLocateBtn');
    if (autoLocateBtn) {
        autoLocateBtn.addEventListener('click', () => {
            if (!navigator.geolocation) {
                alert('Geolocation is not supported by your browser');
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude;
                    const lon = pos.coords.longitude;
                    fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m&daily=precipitation_sum&timezone=auto`)
                        .then(res => res.json())
                        .then(wData => {
                            const cur = wData.current || {};
                            document.getElementById('inputTemp').value = cur.temperature_2m || 25;
                            document.getElementById('sliderTemp').value = cur.temperature_2m || 25;
                            document.getElementById('inputHumidity').value = cur.relative_humidity_2m || 70;
                            document.getElementById('sliderHumidity').value = cur.relative_humidity_2m || 70;
                            document.getElementById('weatherCityInput').value = `GPS (${lat.toFixed(2)}, ${lon.toFixed(2)})`;
                            paramControls.forEach(c => {
                                const el = document.getElementById(c.input);
                                if (el) el.dispatchEvent(new Event('input'));
                            });
                        })
                        .catch(() => alert('Could not sync GPS weather.'));
                },
                () => alert('Location permission denied or unavailable.')
            );
        });
    }

    // -------------------------------------------------------------------------
    // Crop Prediction Form Submission & Results Rendering
    // -------------------------------------------------------------------------
    const predictForm = document.getElementById('cropPredictForm');
    const predictSubmitBtn = document.getElementById('predictSubmitBtn');

    if (predictForm) {
        predictForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const payload = {
                N: parseFloat(document.getElementById('inputN').value),
                P: parseFloat(document.getElementById('inputP').value),
                K: parseFloat(document.getElementById('inputK').value),
                ph: parseFloat(document.getElementById('inputPH').value),
                temperature: parseFloat(document.getElementById('inputTemp').value),
                humidity: parseFloat(document.getElementById('inputHumidity').value),
                rainfall: parseFloat(document.getElementById('inputRainfall').value)
            };

            predictSubmitBtn.innerHTML = '<i data-lucide="loader" class="spin"></i> <span>Analyzing Soil & Climate...</span>';
            if (window.lucide) lucide.createIcons();

            try {
                const resp = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await resp.json();
                predictSubmitBtn.innerHTML = '<i data-lucide="sparkles"></i> <span>Predict Optimal Crop Now</span>';
                if (window.lucide) lucide.createIcons();

                if (result.success) {
                    renderPredictionResults(result);
                } else {
                    alert('Prediction Error: ' + result.error);
                }
            } catch (err) {
                predictSubmitBtn.innerHTML = '<i data-lucide="sparkles"></i> <span>Predict Optimal Crop Now</span>';
                if (window.lucide) lucide.createIcons();
                alert('Request Failed: ' + err.message);
            }
        });
    }

    function renderPredictionResults(data) {
        document.getElementById('emptyStateCard').style.display = 'none';
        const panel = document.getElementById('dynamicResultsPanel');
        panel.style.display = 'block';

        const primary = data.primary_recommendation;
        const info = primary.info;

        // Populate Primary Crop Winner Card
        document.getElementById('resPrimaryIcon').textContent = info.icon || '🌾';
        document.getElementById('resPrimaryName').textContent = info.name || primary.crop.toUpperCase();
        document.getElementById('resPrimaryScientific').textContent = `${info.scientific_name || 'Agro spec'} • ${info.category || 'Crop'}`;
        document.getElementById('resConfidenceVal').textContent = `${primary.confidence}%`;

        document.getElementById('resDuration').textContent = info.duration || '90-120 days';
        document.getElementById('resSeason').textContent = info.season || 'Seasonal';
        document.getElementById('resSoilType').textContent = info.soil_type || 'Loamy';
        document.getElementById('resWater').textContent = info.water_requirement || 'Moderate';

        // Best Practices
        document.getElementById('resEconomicVal').textContent = info.economic_value || 'High market liquidity.';
        const bpList = document.getElementById('resBestPracticesList');
        bpList.innerHTML = '';
        const practices = info.best_practices || ['Follow standard soil prep and weed control.'];
        practices.forEach(bp => {
            const li = document.createElement('li');
            li.innerHTML = `<i data-lucide="check-circle" style="color: var(--primary-green); width: 16px; height: 16px; flex-shrink: 0; margin-top: 2px;"></i> <span>${bp}</span>`;
            bpList.appendChild(li);
        });

        // Fertilizer Mini Guide
        document.getElementById('resFertilizerGuideText').textContent = info.fertilizer_guide || 'Apply recommended basal NPK dose.';

        // Alternatives
        const altList = document.getElementById('resAlternativesList');
        altList.innerHTML = '';
        data.alternatives.forEach(alt => {
            const altInfo = alt.info;
            const item = document.createElement('div');
            item.className = 'alt-crop-item';
            item.innerHTML = `
                <div class="alt-avatar">${altInfo.icon || '🌱'}</div>
                <div class="alt-info">
                    <strong>${altInfo.name}</strong>
                    <span>${altInfo.category} • ${altInfo.season}</span>
                </div>
                <div class="alt-confidence">${alt.confidence}% Fit</div>
            `;
            altList.appendChild(item);
        });

        // Render Multivariate Radar Match Chart
        renderRadarChart(data.radar_data);

        if (window.lucide) lucide.createIcons();
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderRadarChart(radarData) {
        const ctx = document.getElementById('soilRadarChart').getContext('2d');
        if (radarChartInstance) radarChartInstance.destroy();

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';
        const textColor = isDark ? '#cbd5e1' : '#4a5e52';

        radarChartInstance = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: radarData.labels,
                datasets: [
                    {
                        label: 'Your Soil Reading',
                        data: radarData.user_values,
                        backgroundColor: 'rgba(34, 197, 94, 0.25)',
                        borderColor: '#22c55e',
                        borderWidth: 2,
                        pointBackgroundColor: '#22c55e',
                        pointBorderColor: '#ffffff'
                    },
                    {
                        label: 'Ideal Crop Benchmark',
                        data: radarData.crop_ideals,
                        backgroundColor: 'rgba(59, 130, 246, 0.15)',
                        borderColor: '#3b82f6',
                        borderWidth: 2,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#ffffff'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: gridColor },
                        grid: { color: gridColor },
                        pointLabels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } },
                        ticks: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                    }
                }
            }
        });
    }

    // -------------------------------------------------------------------------
    // RAG AGENT & DOCUMENT INTELLIGENCE (TAB 2 / rag_agent.py INTEGRATION)
    // -------------------------------------------------------------------------
    const ragDropZone = document.getElementById('ragDropZone');
    const ragPdfFileInput = document.getElementById('ragPdfFileInput');
    const ragChatForm = document.getElementById('ragChatForm');
    const ragChatInput = document.getElementById('ragChatInput');
    const chatMessagesContainer = document.getElementById('chatMessagesContainer');
    const loadSampleHandbookBtn = document.getElementById('loadSampleHandbookBtn');
    const ragClearDocsBtn = document.getElementById('ragClearDocsBtn');
    const clearChatHistoryBtn = document.getElementById('clearChatHistoryBtn');
    const ragConfigKeysBtn = document.getElementById('ragConfigKeysBtn');
    const ragKeysModal = document.getElementById('ragKeysModal');
    const closeRagModalBtn = document.getElementById('closeRagModalBtn');
    const cancelKeysBtn = document.getElementById('cancelKeysBtn');
    const saveKeysBtn = document.getElementById('saveKeysBtn');

    // Load RAG Status & Indexed Documents
    function loadRagStatus() {
        fetch('/api/rag/status')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    ragStatusData = data;
                    renderRagStatus(data);
                }
            })
            .catch(err => console.error('Failed to fetch RAG status:', err));
    }

    function renderRagStatus(data) {
        const countEl = document.getElementById('ragDocCount');
        if (countEl) countEl.textContent = data.files.length;

        const statusText = document.getElementById('ragStatusText');
        const statusDot = document.getElementById('ragStatusDot');
        if (statusText && statusDot) {
            if (data.files.length === 0) {
                statusText.textContent = 'No documents indexed. Upload a PDF or click Load Handbook below.';
                statusDot.style.background = '#f59e0b';
            } else {
                statusText.textContent = `Active • ${data.files.length} PDF(s) (${data.chunks} text chunks indexed)`;
                statusDot.style.background = 'var(--primary-green)';
            }
        }

        // Render Files List
        const listEl = document.getElementById('ragIndexedFilesList');
        if (listEl) {
            listEl.innerHTML = '';
            if (data.files.length === 0) {
                listEl.innerHTML = '<div style="font-size: 0.82rem; color: var(--text-muted); padding: 0.5rem;">No files uploaded yet.</div>';
            } else {
                data.files.forEach(f => {
                    const row = document.createElement('div');
                    row.className = 'doc-item-row';
                    row.innerHTML = `
                        <div class="doc-item-info">
                            <i data-lucide="file-text"></i>
                            <span class="doc-name-text" title="${f}">${f}</span>
                        </div>
                        <button class="doc-delete-btn" onclick="deleteRagDoc('${f}')" title="Delete document">
                            <i data-lucide="x"></i>
                        </button>
                    `;
                    listEl.appendChild(row);
                });
            }
        }

        // Badges for API Key status
        const groqBadge = document.getElementById('groqStatusBadge');
        if (groqBadge) {
            groqBadge.textContent = data.has_groq_key ? 'Connected (ChatGroq)' : 'Built-in Agro Engine';
            groqBadge.style.color = data.has_groq_key ? 'var(--primary-green)' : 'var(--text-muted)';
        }

        const openaiBadge = document.getElementById('openaiStatusBadge');
        if (openaiBadge) {
            openaiBadge.textContent = data.has_openai_key ? 'OpenAI Embeddings' : 'Local BM25 Vectorizer';
            openaiBadge.style.color = data.has_openai_key ? 'var(--primary-green)' : 'var(--primary-green)';
        }

        if (window.lucide) lucide.createIcons();
    }

    // Delete single document
    window.deleteRagDoc = (filename) => {
        if (!confirm(`Delete ${filename}?`)) return;
        fetch('/api/rag/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                loadRagStatus();
            } else {
                alert('Delete failed: ' + data.error);
            }
        });
    };

    // Clear all docs
    if (ragClearDocsBtn) {
        ragClearDocsBtn.addEventListener('click', () => {
            if (!confirm('Clear all indexed documents?')) return;
            fetch('/api/rag/clear', { method: 'POST' })
                .then(res => res.json())
                .then(() => loadRagStatus());
        });
    }

    // Load Sample Agronomy Handbook
    if (loadSampleHandbookBtn) {
        loadSampleHandbookBtn.addEventListener('click', () => {
            loadSampleHandbookBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Loading Handbook...';
            if (window.lucide) lucide.createIcons();
            fetch('/api/rag/load-sample', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    loadSampleHandbookBtn.innerHTML = '<i data-lucide="book-check"></i> Load Preloaded Agronomy Handbook';
                    if (window.lucide) lucide.createIcons();
                    if (data.success) {
                        loadRagStatus();
                        appendBotMessage("Preloaded **Sustainable Agriculture & Agronomy Handbook** successfully! You can now ask questions about NPK fertilizer protocols, soil acidity remedies, irrigation stages, and organic pest control.");
                    }
                })
                .catch(() => {
                    loadSampleHandbookBtn.innerHTML = '<i data-lucide="book-check"></i> Load Preloaded Agronomy Handbook';
                    if (window.lucide) lucide.createIcons();
                });
        });
    }

    // Upload PDF via input & dropzone
    if (ragPdfFileInput) {
        ragPdfFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) uploadRagFiles(e.target.files);
        });
    }

    if (ragDropZone) {
        ragDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            ragDropZone.classList.add('dragover');
        });
        ragDropZone.addEventListener('dragleave', () => {
            ragDropZone.classList.remove('dragover');
        });
        ragDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            ragDropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) uploadRagFiles(e.dataTransfer.files);
        });
    }

    async function uploadRagFiles(fileList) {
        const formData = new FormData();
        let validPdfCount = 0;
        for (let i = 0; i < fileList.length; i++) {
            if (fileList[i].name.toLowerCase().endsWith('.pdf')) {
                formData.append('files', fileList[i]);
                validPdfCount++;
            }
        }

        if (validPdfCount === 0) {
            alert('Please select valid PDF documents.');
            return;
        }

        const statusText = document.getElementById('ragStatusText');
        if (statusText) statusText.textContent = `Uploading and indexing ${validPdfCount} PDF(s)...`;

        try {
            const resp = await fetch('/api/rag/upload', {
                method: 'POST',
                body: formData
            });
            const data = await resp.json();
            if (data.success) {
                loadRagStatus();
                appendBotMessage(`Successfully indexed **${validPdfCount} new PDF document(s)** into the vector database. You can now ask questions related to them!`);
            } else {
                alert('Upload error: ' + data.error);
                loadRagStatus();
            }
        } catch (err) {
            alert('Upload failed: ' + err.message);
            loadRagStatus();
        }
    }

    // Chat Execution
    if (ragChatForm) {
        ragChatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = ragChatInput.value.trim();
            if (!query) return;

            ragChatInput.value = '';
            executeRagChat(query);
        });
    }

    window.askSuggestedPrompt = (promptText) => {
        executeRagChat(promptText);
    };

    function appendUserMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'chat-message msg-user';
        msg.innerHTML = `
            <div class="msg-avatar"><i data-lucide="user"></i></div>
            <div class="msg-bubble"><p>${escapeHtml(text)}</p></div>
        `;
        chatMessagesContainer.appendChild(msg);
        if (window.lucide) lucide.createIcons();
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    function appendBotMessage(text, sources = [], engine = null) {
        const msg = document.createElement('div');
        msg.className = 'chat-message msg-bot';

        let formattedText = formatMarkdown(text);

        let citationsHtml = '';
        if (sources && sources.length > 0) {
            citationsHtml = `
                <div class="citation-box">
                    <div class="citation-header"><i data-lucide="book-open" style="width: 12px;"></i> Cited Document Sources:</div>
                    <div class="source-pill-list">
            `;
            sources.forEach(s => {
                citationsHtml += `
                    <div class="source-pill">
                        <span class="source-tag">📄 ${s.source} (Page ${s.page})</span>
                        <div class="source-snippet">"...${escapeHtml(s.text.substring(0, 160))}..."</div>
                    </div>
                `;
            });
            citationsHtml += `</div></div>`;
        }

        msg.innerHTML = `
            <div class="msg-avatar"><i data-lucide="sprout"></i></div>
            <div class="msg-bubble">
                ${formattedText}
                ${citationsHtml}
            </div>
        `;
        chatMessagesContainer.appendChild(msg);
        if (window.lucide) lucide.createIcons();
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    async function executeRagChat(query) {
        appendUserMessage(query);

        // Typing loading bubble
        const typingMsg = document.createElement('div');
        typingMsg.className = 'chat-message msg-bot';
        typingMsg.id = 'tempTypingIndicator';
        typingMsg.innerHTML = `
            <div class="msg-avatar"><i data-lucide="sprout"></i></div>
            <div class="msg-bubble"><p><em>Searching document vectors & synthesizing answer... 🌱</em></p></div>
        `;
        chatMessagesContainer.appendChild(typingMsg);
        if (window.lucide) lucide.createIcons();
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

        try {
            const resp = await fetch('/api/rag/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, history: ragChatHistory })
            });

            const data = await resp.json();
            const temp = document.getElementById('tempTypingIndicator');
            if (temp) temp.remove();

            if (data.success) {
                ragChatHistory.push({ role: 'user', content: query });
                ragChatHistory.push({ role: 'ai', content: data.answer });
                appendBotMessage(data.answer, data.sources, data.engine);
                if (data.engine) {
                    document.getElementById('chatEngineLabel').textContent = `Active • ${data.engine}`;
                }
            } else {
                appendBotMessage(`⚠️ ${data.answer || data.error}`);
            }
        } catch (err) {
            const temp = document.getElementById('tempTypingIndicator');
            if (temp) temp.remove();
            appendBotMessage(`⚠️ Connection error: ${err.message}`);
        }
    }

    if (clearChatHistoryBtn) {
        clearChatHistoryBtn.addEventListener('click', () => {
            ragChatHistory = [];
            chatMessagesContainer.innerHTML = `
                <div class="chat-message msg-bot">
                    <div class="msg-avatar"><i data-lucide="sprout"></i></div>
                    <div class="msg-bubble">
                        <p><strong>Chat Cleared. 🌱</strong></p>
                        <p>Ask any question related to soil chemistry, NPK dosing, or crop cultivation from your indexed documents.</p>
                    </div>
                </div>
            `;
            if (window.lucide) lucide.createIcons();
        });
    }

    // Modal API Keys Configuration
    if (ragConfigKeysBtn) {
        ragConfigKeysBtn.addEventListener('click', () => {
            ragKeysModal.style.display = 'flex';
        });
    }
    if (closeRagModalBtn) closeRagModalBtn.addEventListener('click', () => ragKeysModal.style.display = 'none');
    if (cancelKeysBtn) cancelKeysBtn.addEventListener('click', () => ragKeysModal.style.display = 'none');

    if (saveKeysBtn) {
        saveKeysBtn.addEventListener('click', async () => {
            const groq_api_key = document.getElementById('modalGroqKey').value.trim();
            const openai_api_key = document.getElementById('modalOpenAIKey').value.trim();

            saveKeysBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Saving...';
            if (window.lucide) lucide.createIcons();

            try {
                const resp = await fetch('/api/rag/config-keys', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ groq_api_key, openai_api_key })
                });
                const data = await resp.json();
                saveKeysBtn.innerHTML = '<i data-lucide="check"></i> Save & Re-index';
                if (window.lucide) lucide.createIcons();

                if (data.success) {
                    ragKeysModal.style.display = 'none';
                    loadRagStatus();
                    alert('API keys configured and vector database refreshed!');
                } else {
                    alert('Configuration error: ' + data.error);
                }
            } catch (err) {
                saveKeysBtn.innerHTML = '<i data-lucide="check"></i> Save & Re-index';
                alert('Save failed: ' + err.message);
            }
        });
    }

    // -------------------------------------------------------------------------
    // Fertilizer Doctor Formulation Calculator (TAB 3)
    // -------------------------------------------------------------------------
    const fertilizerForm = document.getElementById('fertilizerForm');
    if (fertilizerForm) {
        fertilizerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const payload = {
                target_crop: document.getElementById('fertTargetCrop').value,
                N: parseFloat(document.getElementById('fertN').value),
                P: parseFloat(document.getElementById('fertP').value),
                K: parseFloat(document.getElementById('fertK').value),
                ph: parseFloat(document.getElementById('fertPH').value)
            };

            try {
                const resp = await fetch('/api/fertilizer-recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await resp.json();
                if (result.success) {
                    renderFertilizerReport(result.data);
                }
            } catch (err) {
                console.error('Fertilizer calculation error:', err);
            }
        });
    }

    function renderFertilizerReport(data) {
        document.getElementById('fertHealthScore').textContent = `${data.soil_health_score}%`;

        // Nutrient Deficit Grid
        const grid = document.getElementById('fertNutrientGrid');
        grid.innerHTML = '';

        const nuts = [
            { label: 'Nitrogen (N)', d: data.nutrients.N },
            { label: 'Phosphorus (P)', d: data.nutrients.P },
            { label: 'Potassium (K)', d: data.nutrients.K }
        ];

        nuts.forEach(n => {
            const chip = document.createElement('div');
            chip.className = `nutrient-status-chip status-${n.d.status}`;
            chip.innerHTML = `
                <div><strong>${n.label}</strong></div>
                <div style="font-size: 0.82rem; margin: 0.2rem 0;">Status: <span style="text-transform: capitalize;">${n.d.status}</span></div>
                <div style="font-size: 0.78rem; opacity: 0.85;">Current: ${n.d.current} | Ideal: ${n.d.ideal} kg/ha</div>
            `;
            grid.appendChild(chip);
        });

        // Prescriptions List
        const prescList = document.getElementById('fertPrescriptionsList');
        prescList.innerHTML = '';
        data.prescriptions.forEach(p => {
            const div = document.createElement('div');
            div.className = 'prescription-card';
            div.innerHTML = `
                <span class="presc-icon">${p.icon || '📦'}</span>
                <div style="flex: 1;">
                    <div class="presc-header">
                        <span class="presc-name">${p.fertilizer}</span>
                        <span class="presc-dosage">${p.dosage}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); margin-bottom: 0.2rem;">${p.purpose}</div>
                    <div class="presc-timing"><i data-lucide="clock" style="width: 13px; height: 13px; vertical-align: middle;"></i> ${p.timing}</div>
                </div>
            `;
            prescList.appendChild(div);
        });

        // pH Remedy
        document.getElementById('phRemedyText').textContent = data.nutrients.ph.remedy;
        if (window.lucide) lucide.createIcons();
    }

    // -------------------------------------------------------------------------
    // Crops Catalog (TAB 4)
    // -------------------------------------------------------------------------
    function loadCropsCatalog() {
        fetch('/api/crops')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    allCropsData = data.crops;
                    populateCropSelectOptions(allCropsData);
                    renderCropsGrid(allCropsData);
                }
            })
            .catch(err => console.error('Failed to load crops catalog:', err));
    }

    function populateCropSelectOptions(crops) {
        const selectEl = document.getElementById('fertTargetCrop');
        if (!selectEl) return;
        selectEl.innerHTML = '';
        for (const [key, crop] of Object.entries(crops)) {
            const opt = document.createElement('option');
            opt.value = key;
            opt.textContent = `${crop.icon || '🌱'} ${crop.name}`;
            selectEl.appendChild(opt);
        }
    }

    function renderCropsGrid(crops, searchTerm = '', filterCategory = 'all') {
        const grid = document.getElementById('cropsDirectoryGrid');
        if (!grid) return;
        grid.innerHTML = '';

        const terms = searchTerm.toLowerCase().trim();

        for (const [key, crop] of Object.entries(crops)) {
            const matchesSearch = crop.name.toLowerCase().includes(terms) ||
                                  crop.category.toLowerCase().includes(terms) ||
                                  crop.soil_type.toLowerCase().includes(terms);

            let matchesCat = true;
            if (filterCategory !== 'all') {
                matchesCat = crop.category.toLowerCase().includes(filterCategory);
            }

            if (matchesSearch && matchesCat) {
                const card = document.createElement('div');
                card.className = 'crop-card';
                card.innerHTML = `
                    <div class="crop-card-top">
                        <span class="crop-card-icon">${crop.icon || '🌱'}</span>
                        <div>
                            <h4 class="crop-card-title">${crop.name}</h4>
                            <span class="crop-card-category">${crop.category}</span>
                        </div>
                    </div>
                    <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.75rem;">${crop.scientific_name}</p>
                    <div style="font-size: 0.82rem; margin-bottom: 1rem; flex-grow: 1;">
                        <div><strong>Season:</strong> ${crop.season}</div>
                        <div><strong>Duration:</strong> ${crop.duration}</div>
                        <div><strong>Water:</strong> ${crop.water_requirement}</div>
                    </div>
                    <button class="btn-outline-sm btn-full" onclick="testCropInRecommender('${key}')">
                        <i data-lucide="sparkles"></i> Test in AI Recommender
                    </button>
                `;
                grid.appendChild(card);
            }
        }
        if (window.lucide) lucide.createIcons();
    }

    window.testCropInRecommender = (cropKey) => {
        switchTab('tab-recommender');

        fetch('/api/analytics')
            .then(res => res.json())
            .then(data => {
                const stats = data.analytics.crop_stats[cropKey];
                if (stats) {
                    document.getElementById('inputN').value = Math.round(stats.N.mean);
                    document.getElementById('sliderN').value = Math.round(stats.N.mean);
                    document.getElementById('inputP').value = Math.round(stats.P.mean);
                    document.getElementById('sliderP').value = Math.round(stats.P.mean);
                    document.getElementById('inputK').value = Math.round(stats.K.mean);
                    document.getElementById('sliderK').value = Math.round(stats.K.mean);
                    document.getElementById('inputPH').value = stats.ph.mean.toFixed(1);
                    document.getElementById('sliderPH').value = stats.ph.mean.toFixed(1);
                    document.getElementById('inputTemp').value = stats.temperature.mean.toFixed(1);
                    document.getElementById('sliderTemp').value = stats.temperature.mean.toFixed(1);
                    document.getElementById('inputHumidity').value = Math.round(stats.humidity.mean);
                    document.getElementById('sliderHumidity').value = Math.round(stats.humidity.mean);
                    document.getElementById('inputRainfall').value = Math.round(stats.rainfall.mean);
                    document.getElementById('sliderRainfall').value = Math.round(stats.rainfall.mean);

                    paramControls.forEach(c => {
                        const el = document.getElementById(c.input);
                        if (el) el.dispatchEvent(new Event('input'));
                    });

                    document.getElementById('cropPredictForm').dispatchEvent(new Event('submit'));
                }
            });
    };

    const cropSearchInput = document.getElementById('cropSearchInput');
    if (cropSearchInput) {
        cropSearchInput.addEventListener('input', (e) => {
            const activeFilter = document.querySelector('.filter-pill.active').getAttribute('data-category');
            renderCropsGrid(allCropsData, e.target.value, activeFilter);
        });
    }

    const filterPills = document.querySelectorAll('.filter-pill');
    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const cat = pill.getAttribute('data-category');
            const searchVal = cropSearchInput ? cropSearchInput.value : '';
            renderCropsGrid(allCropsData, searchVal, cat);
        });
    });

    // -------------------------------------------------------------------------
    // ML Analytics Dashboard (TAB 5)
    // -------------------------------------------------------------------------
    function loadAnalyticsDashboard() {
        fetch('/api/analytics')
            .then(res => res.json())
            .then(data => {
                if (data.success) renderAnalytics(data.analytics);
            })
            .catch(err => console.error('Failed to load analytics:', err));
    }

    function renderAnalytics(analytics) {
        const topModelEl = document.getElementById('statTopModel');
        if (topModelEl) topModelEl.textContent = analytics.best_model || 'Random Forest';

        const rfAccuracy = analytics.model_comparison['Random Forest']?.accuracy || 99.55;
        const topAccEl = document.getElementById('statTopAccuracy');
        if (topAccEl) topAccEl.textContent = `${rfAccuracy}%`;

        // Populate Table
        const tbody = document.querySelector('#modelsBenchmarkTable tbody');
        if (tbody) {
            tbody.innerHTML = '';
            const models = analytics.model_comparison;
            for (const [name, m] of Object.entries(models)) {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${name}</strong> ${name === analytics.best_model ? '🏆' : ''}</td>
                    <td>${m.accuracy}%</td>
                    <td>${m.precision}%</td>
                    <td>${m.recall}%</td>
                    <td>${m.f1_score}%</td>
                    <td>${m.cv_mean}% ± ${m.cv_std}%</td>
                `;
                tbody.appendChild(tr);
            }
        }

        // Feature Importance Chart
        renderFeatureImportanceChart(analytics.feature_importances);
    }

    function renderFeatureImportanceChart(importances) {
        const canvas = document.getElementById('featureImportanceChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (featureChartInstance) featureChartInstance.destroy();

        const labels = Object.keys(importances).map(k => {
            const map = {
                'N': 'Nitrogen (N)',
                'P': 'Phosphorus (P)',
                'K': 'Potassium (K)',
                'temperature': 'Temperature',
                'humidity': 'Humidity',
                'ph': 'Soil pH',
                'rainfall': 'Rainfall'
            };
            return map[k] || k;
        });
        const values = Object.values(importances);

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#f1f5f9' : '#14231b';

        featureChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feature Contribution (%)',
                    data: values,
                    backgroundColor: [
                        '#16a34a', '#3b82f6', '#f59e0b', '#ec4899', '#a855f7', '#06b6d4', '#10b981'
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => ` Predictive Weight: ${ctx.parsed.x}%`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)' },
                        ticks: { color: textColor }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: textColor, font: { weight: '600' } }
                    }
                }
            }
        });
    }

    function updateChartTheme() {
        if (radarChartInstance) radarChartInstance.update();
        if (featureChartInstance) featureChartInstance.update();
    }

    // -------------------------------------------------------------------------
    // Batch CSV Prediction (TAB 6)
    // -------------------------------------------------------------------------
    const csvFileInput = document.getElementById('batchCsvFileInput');
    const csvDropZone = document.getElementById('csvDropZone');

    if (csvFileInput) {
        csvFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) handleCsvUpload(e.target.files[0]);
        });
    }

    if (csvDropZone) {
        csvDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            csvDropZone.style.borderColor = 'var(--primary-green)';
        });
        csvDropZone.addEventListener('dragleave', () => {
            csvDropZone.style.borderColor = 'var(--border-color)';
        });
        csvDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            csvDropZone.style.borderColor = 'var(--border-color)';
            if (e.dataTransfer.files.length > 0) handleCsvUpload(e.dataTransfer.files[0]);
        });
    }

    async function handleCsvUpload(file) {
        if (!file.name.endsWith('.csv')) {
            alert('Please upload a valid .csv file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const resp = await fetch('/api/batch-predict', {
                method: 'POST',
                body: formData
            });
            const data = await resp.json();
            if (data.success) {
                batchPredictionsData = data.results;
                renderBatchResults(data.results);
            } else {
                alert('Batch Processing Error: ' + data.error);
            }
        } catch (err) {
            alert('Upload failed: ' + err.message);
        }
    }

    function renderBatchResults(results) {
        const card = document.getElementById('batchResultsCard');
        card.style.display = 'block';
        document.getElementById('batchCountText').textContent = `Processed ${results.length} soil samples successfully.`;

        const tbody = document.querySelector('#batchResultsTable tbody');
        tbody.innerHTML = '';

        results.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${r.sample_id}</td>
                <td>${r.N}</td>
                <td>${r.P}</td>
                <td>${r.K}</td>
                <td>${r.temperature}°C</td>
                <td>${r.humidity}%</td>
                <td>${r.ph}</td>
                <td>${r.rainfall}mm</td>
                <td><strong style="color: var(--primary-green);">${r.recommended_crop}</strong></td>
                <td>${r.confidence}%</td>
            `;
            tbody.appendChild(tr);
        });

        card.scrollIntoView({ behavior: 'smooth' });
    }

    // Export Batch CSV
    const exportBatchBtn = document.getElementById('exportBatchCsvBtn');
    if (exportBatchBtn) {
        exportBatchBtn.addEventListener('click', () => {
            if (batchPredictionsData.length === 0) return;

            let csvContent = 'data:text/csv;charset=utf-8,Sample_ID,N,P,K,Temperature,Humidity,pH,Rainfall,Recommended_Crop,Confidence_Percent\n';
            batchPredictionsData.forEach(r => {
                csvContent += `${r.sample_id},${r.N},${r.P},${r.K},${r.temperature},${r.humidity},${r.ph},${r.rainfall},${r.recommended_crop},${r.confidence}\n`;
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', 'crop_recommendation_batch_results.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }

    // -------------------------------------------------------------------------
    // Utility Helpers
    // -------------------------------------------------------------------------
    function escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function formatMarkdown(text) {
        if (!text) return '';
        let escaped = escapeHtml(text);
        // Bold: **text**
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Bullets: • text or * text
        escaped = escaped.replace(/^[•*]\s+(.*)$/gm, '<li style="margin-left: 1.2rem;">$1</li>');
        // Linebreaks
        escaped = escaped.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
        return `<p>${escaped}</p>`;
    }

    // Initial Status Loads
    loadCropsCatalog();
    loadRagStatus();
});
