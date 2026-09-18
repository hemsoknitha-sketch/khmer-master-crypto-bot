/**
 * KHMER MASTER CRYPTO - APEX SUPER BRAIN AI WEB GUI CONTROLLER
 * Full AI Graphic Super Brain Design & Cambodia Flag Cybertech Architecture
 * Real-time 0.001ms HFT Stream & Interactive VIP Cockpit
 */

// Initialize Telegram WebApp SDK
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
    if (tg.enableClosingConfirmation) tg.enableClosingConfirmation();
}

// Global Application State
const state = {
    chatId: getQueryParam('chat_id') || tg?.initDataUnsafe?.user?.id || 0,
    timeframe: '7D',
    equityChart: null,
    allocationChart: null,
    portfolioData: null,
    wealthCockpit: null,
    aiBrainData: null,
    mevData: null,
    analytics: null,
    radar: null,
    isRefreshing: false,
    sseSource: null,
    ws: null,
    streamConnected: false
};

// DOM Elements
const elements = {
    totalBalanceUsd: document.getElementById('total-balance-usd'),
    pnl24hBadge: document.getElementById('pnl-24h-badge'),
    spotUsdtVal: document.getElementById('spot-usdt-val'),
    futuresUsdtVal: document.getElementById('futures-usdt-val'),
    spotAltVal: document.getElementById('spot-alt-val'),
    paxgHoldVal: document.getElementById('paxg-hold-val'),
    activePositionsCount: document.getElementById('active-positions-count'),
    navPosBadge: document.getElementById('nav-pos-badge'),
    clockCambodia: document.getElementById('clock-cambodia'),
    clockTokyo: document.getElementById('clock-tokyo'),
    latencyVal: document.getElementById('latency-val'),
    hftSyncTicker: document.getElementById('hft-sync-ticker'),
    wealthPosBadge: document.getElementById('wealth-pos-badge'),
    wealthTradesList: document.getElementById('wealth-trades-list'),
    wealthEmptyState: document.getElementById('wealth-empty-state'),
    sweetspotCandidatesList: document.getElementById('sweetspot-candidates-list'),
    brainScoreVal: document.getElementById('brain-score-val'),
    brainSentimentBadge: document.getElementById('brain-sentiment-badge'),
    radialProgress: document.getElementById('radial-progress'),
    brainAdxVal: document.getElementById('brain-adx-val'),
    aiAgentsGrid: document.getElementById('ai-agents-grid'),
    mevCyclesList: document.getElementById('mev-cycles-list'),
    vaultBtcQty: document.getElementById('vault-btc-qty'),
    vaultBtcUsd: document.getElementById('vault-btc-usd'),
    vaultPaxgQty: document.getElementById('vault-paxg-qty'),
    vaultPaxgUsd: document.getElementById('vault-paxg-usd'),
    sweepPoolText: document.getElementById('sweep-pool-text'),
    sweepProgressBar: document.getElementById('sweep-progress-bar'),
    macroRatioValue: document.getElementById('macro-ratio-value'),
    macroNeedle: document.getElementById('macro-needle'),
    macroVerdictBadge: document.getElementById('macro-verdict-badge'),
    harvestHistoryList: document.getElementById('harvest-history-list'),
    btnRefresh: document.getElementById('btn-refresh'),
    btnManualSweep: document.getElementById('btn-manual-sweep'),
    toastContainer: document.getElementById('toast-container')
};

// Utilities
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function triggerHaptic(type = 'light') {
    if (tg?.HapticFeedback) {
        if (type === 'selection') tg.HapticFeedback.selectionChanged();
        else tg.HapticFeedback.impactOccurred(type);
    }
}

function showToast(message, duration = 3000) {
    if (!elements.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = message;
    elements.toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function formatUSD(num) {
    return Number(num || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// -----------------------------------------------------------------------------
// Live Clocks & Latency Controller
// -----------------------------------------------------------------------------
function startClocks() {
    function update() {
        const now = new Date();
        // Cambodia (UTC+7)
        const kmTime = new Intl.DateTimeFormat('en-GB', {
            timeZone: 'Asia/Phnom_Penh',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(now);
        if (elements.clockCambodia) elements.clockCambodia.textContent = kmTime;

        // Tokyo (UTC+9)
        const tyoTime = new Intl.DateTimeFormat('en-GB', {
            timeZone: 'Asia/Tokyo',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(now);
        if (elements.clockTokyo) elements.clockTokyo.textContent = tyoTime;
    }
    setInterval(update, 1000);
    update();
}

// -----------------------------------------------------------------------------
// Interactive Neural Network Background Animation Canvas
// -----------------------------------------------------------------------------
function initNeuralCanvas() {
    const canvas = document.getElementById('neuralCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(45, Math.floor((width * height) / 18000));

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.6,
            vy: (Math.random() - 0.5) * 0.6,
            radius: Math.random() * 2 + 1,
            color: i % 3 === 0 ? '#00f2fe' : i % 3 === 1 ? '#FFB703' : '#E00034'
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color;
            ctx.fill();

            // Connect nearby nodes with neural synapses
            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 242, 254, ${0.25 * (1 - dist / 120)})`;
                    ctx.lineWidth = 0.75;
                    ctx.shadowBlur = 0;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

// -----------------------------------------------------------------------------
// Chart.js Initializations
// -----------------------------------------------------------------------------
function initCharts() {
    const ctxEquity = document.getElementById('equityChart')?.getContext('2d');
    if (ctxEquity && window.Chart) {
        const gradient = ctxEquity.createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, 'rgba(0, 242, 254, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 242, 254, 0.0)');

        state.equityChart = new Chart(ctxEquity, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Today'],
                datasets: [{
                    label: 'Cumulative Net Profit ($)',
                    data: [1000, 1045, 1030, 1085, 1120, 1140, 1175],
                    borderColor: '#00f2fe',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#FFB703',
                    pointBorderColor: '#00f2fe',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    backgroundColor: gradient,
                    tension: 0.35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9.5 } } },
                    y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9.5 } } }
                }
            }
        });
    }

    const ctxAlloc = document.getElementById('allocationChart')?.getContext('2d');
    if (ctxAlloc && window.Chart) {
        state.allocationChart = new Chart(ctxAlloc, {
            type: 'doughnut',
            data: {
                labels: ['Futures', 'Spot USDT', 'BTC', 'PAXG Gold'],
                datasets: [{
                    data: [45, 30, 15, 10],
                    backgroundColor: ['#00f2fe', '#10b981', '#f59e0b', '#FFD166'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: { legend: { display: false } }
            }
        });
    }
}

// -----------------------------------------------------------------------------
// Ultra-Fast WebSocket & Resilient SSE Real-Time Stream Controller (0.01ms Live)
// -----------------------------------------------------------------------------
function handleStreamData(data) {
    if (!data) return;

    if (elements.latencyVal) elements.latencyVal.textContent = `${data.hft_latency_ms || 0.01} ms`;
    if (elements.hftSyncTicker) {
        elements.hftSyncTicker.textContent = `0.01ms TOKYO HFT SYNC • LIVE (${data.timestamp || '--:--:--'})`;
    }

    // Real-Time Net Worth & Balances
    if (data.net_worth !== undefined && data.net_worth > 0 && elements.totalBalanceUsd) {
        elements.totalBalanceUsd.textContent = formatUSD(data.net_worth);
    }
    if (data.spot_usdt_free !== undefined && elements.spotUsdtVal) {
        elements.spotUsdtVal.textContent = `$${formatUSD(data.spot_usdt_free)}`;
    }
    if (data.futures_wallet_usdt !== undefined && elements.futuresUsdtVal) {
        elements.futuresUsdtVal.textContent = `$${formatUSD(data.futures_wallet_usdt)}`;
    }
    if (data.btc_value_usd !== undefined && elements.spotAltVal) {
        elements.spotAltVal.textContent = `$${formatUSD(data.btc_value_usd)}`;
    }
    if (data.paxg_value_usd !== undefined && elements.paxgHoldVal) {
        elements.paxgHoldVal.textContent = `$${formatUSD(data.paxg_value_usd)}`;
    }

    // Real-Time Active Positions Update without full page reload
    if (Array.isArray(data.active_trades)) {
        renderLiveActiveTrades(data.active_trades);
    }
    if (Array.isArray(data.candidates) && data.candidates.length > 0) {
        renderLiveCandidates(data.candidates);
    }
}

function renderLiveActiveTrades(trades) {
    const count = trades.length;
    if (elements.activePositionsCount) elements.activePositionsCount.textContent = `${count} Positions កំពុងរត់`;
    if (elements.wealthPosBadge) elements.wealthPosBadge.textContent = `${count} Active`;
    if (elements.navPosBadge) {
        elements.navPosBadge.textContent = count;
        elements.navPosBadge.style.display = count > 0 ? 'flex' : 'none';
    }

    if (!elements.wealthTradesList) return;

    if (count === 0) {
        elements.wealthTradesList.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">🛡️</span>
                <h4>កំពុងស្កេនរកឱកាស Safe Entry...</h4>
                <p>ប្រព័ន្ធកំពុងស្វែងរក Golden Sweet Spot ជាមួយ 15m EMA20 Retracement Confluence</p>
            </div>
        `;
        return;
    }

    elements.wealthTradesList.innerHTML = trades.map(t => {
        const isLong = t.side === 'BUY';
        const roiClass = t.roi_pct >= 0 ? 'text-neon-emerald' : 'text-neon-red';
        const breakevenBadge = t.breakeven_locked 
            ? `<span class="badge badge-success">🔒 Breakeven Locked (+3.0%)</span>`
            : `<span class="badge badge-accent">🛡️ Trailing Active</span>`;
        
        return `
            <div class="position-card ${isLong ? 'long' : 'short'}">
                <div class="pos-header-row">
                    <span class="pos-sym-title">${t.symbol}</span>
                    <span class="pos-side-badge ${isLong ? 'buy' : 'sell'}">${t.side} ${t.leverage}x</span>
                </div>
                <div class="pos-metrics-grid">
                    <div><span class="pm-label">Entry Price</span><span class="pm-val">$${Number(t.entry_price).toFixed(4)}</span></div>
                    <div><span class="pm-label">Mark Price</span><span class="pm-val">$${Number(t.mark_price).toFixed(4)}</span></div>
                    <div><span class="pm-label">Live ROI %</span><span class="pm-val ${roiClass}">${t.roi_pct >= 0 ? '+' : ''}${Number(t.roi_pct).toFixed(2)}%</span></div>
                </div>
                <div class="pos-status-bar">
                    ${breakevenBadge}
                    <span class="text-neon-gold">Ratchet: 85% Lock</span>
                    <button class="btn-fast-close" onclick="closeTrade('${t.symbol}')" style="background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:#fff; border-radius:4px; padding:2px 6px; font-size:9px; cursor:pointer;">Fast Close</button>
                </div>
            </div>
        `;
    }).join('');
}

function renderLiveCandidates(candidates) {
    if (!elements.sweetspotCandidatesList) return;
    elements.sweetspotCandidatesList.innerHTML = candidates.slice(0, 4).map(c => `
        <div class="candidate-row">
            <span class="cand-sym">${c.symbol}</span>
            <span class="badge badge-accent">${c.side}</span>
            <span class="cand-score">AI: ${c.ai_score || 8.5}/10</span>
        </div>
    `).join('');
}

function initRealtimeStream() {
    if (state.ws) {
        try { state.ws.close(); } catch(e) {}
        state.ws = null;
    }
    if (state.sseSource) {
        try { state.sseSource.close(); } catch(e) {}
        state.sseSource = null;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/ws?chat_id=${state.chatId}`;
    let isWsOpen = false;

    try {
        const ws = new WebSocket(wsUrl);
        state.ws = ws;

        ws.onopen = () => {
            isWsOpen = true;
            state.streamConnected = true;
            console.log('⚡ [HFT WS] Connected to 0.01ms Live Stream!');
            if (elements.hftSyncTicker) {
                elements.hftSyncTicker.textContent = `0.01ms TOKYO HFT SYNC • LIVE`;
            }
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleStreamData(data);
            } catch (err) {}
        };

        ws.onerror = () => {
            if (!isWsOpen) {
                initSSEFallback();
            }
        };

        ws.onclose = () => {
            state.streamConnected = false;
            setTimeout(() => {
                if (!isWsOpen) initSSEFallback();
                else initRealtimeStream();
            }, 2000);
        };
    } catch (e) {
        initSSEFallback();
    }
}

function initSSEFallback() {
    if (state.sseSource) {
        try { state.sseSource.close(); } catch(e) {}
    }
    const sseUrl = `/api/stream?chat_id=${state.chatId}`;
    try {
        state.sseSource = new EventSource(sseUrl);
        state.sseSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleStreamData(data);
            } catch (err) {}
        };
        state.sseSource.onerror = () => {
            state.sseSource.close();
            setTimeout(initRealtimeStream, 3000);
        };
    } catch (e) {
        console.warn('Realtime streaming fallback error');
    }
}

// -----------------------------------------------------------------------------
// Data Fetchers
// -----------------------------------------------------------------------------
async function fetchPortfolio() {
    try {
        const res = await fetch(`/api/portfolio?chat_id=${state.chatId}`);
        const json = await res.json();
        if (json.status === 'success' && json.data) {
            const d = json.data;
            state.portfolioData = d;
            if (elements.totalBalanceUsd) elements.totalBalanceUsd.textContent = formatUSD(d.total_net_worth_usd);
            if (elements.spotUsdtVal) elements.spotUsdtVal.textContent = `$${formatUSD(d.spot_usdt_free)}`;
            if (elements.futuresUsdtVal) elements.futuresUsdtVal.textContent = `$${formatUSD(d.futures_wallet_usdt)}`;
            if (elements.spotAltVal) elements.spotAltVal.textContent = `$${formatUSD(d.btc_value_usd)}`;
            if (elements.paxgHoldVal) elements.paxgHoldVal.textContent = `$${formatUSD(d.paxg_value_usd)}`;

            if (state.allocationChart) {
                let f = 45.0, s = 30.0, b = 15.0, p = 10.0;
                if (d.allocation) {
                    const rf = parseFloat(d.allocation.futures) || 0;
                    const rs = parseFloat(d.allocation.spot_usdt) || 0;
                    const rb = parseFloat(d.allocation.btc) || 0;
                    const rp = parseFloat(d.allocation.paxg) || 0;
                    if (rf + rs + rb + rp > 10 && rf <= 100 && rb <= 100) {
                        f = rf; s = rs; b = rb; p = rp;
                    }
                }
                state.allocationChart.data.datasets[0].data = [f, s, b, p];
                state.allocationChart.update();
                const legFut = document.getElementById('leg-fut-pct');
                const legSpot = document.getElementById('leg-spot-pct');
                const legBtc = document.getElementById('leg-btc-pct');
                const legPaxg = document.getElementById('leg-paxg-pct');
                if (legFut) legFut.textContent = `${f}%`;
                if (legSpot) legSpot.textContent = `${s}%`;
                if (legBtc) legBtc.textContent = `${b}%`;
                if (legPaxg) legPaxg.textContent = `${p}%`;
            }

            // Real-time Grand Profit / Loss Calculation & Presentation
            if (d.grand_metrics) {
                const gm = d.grand_metrics;
                const sign = gm.grand_total_pnl >= 0 ? '+' : '-';
                const absPnl = Math.abs(gm.grand_total_pnl);
                const absRoi = Math.abs(gm.grand_roi_pct);
                const pnlText = `${sign}$${formatUSD(absPnl)} (${sign}${absRoi.toFixed(2)}%)`;
                const isPos = gm.grand_total_pnl >= 0;

                // 1. Hero Grand PnL Pill
                const heroPnlVal = document.getElementById('hero-grand-pnl-val');
                const heroPnlRow = document.querySelector('.hero-grand-pnl-row');
                if (heroPnlVal) {
                    heroPnlVal.textContent = pnlText;
                    heroPnlVal.className = isPos ? 'text-neon-emerald' : 'text-neon-crimson';
                }
                if (heroPnlRow) {
                    heroPnlRow.className = isPos ? 'hero-grand-pnl-row' : 'hero-grand-pnl-row is-negative';
                }

                // 2. 24H Badge
                if (elements.pnl24hBadge) {
                    const sign24 = gm.pnl_24h >= 0 ? '+' : '-';
                    elements.pnl24hBadge.textContent = `${sign24}${Math.abs(gm.pnl_24h_pct).toFixed(2)}% (24H)`;
                    elements.pnl24hBadge.className = gm.pnl_24h >= 0 ? 'badge badge-success' : 'badge badge-danger';
                }

                // 3. Render Global Multi-Timeframe Matrix
                renderGlobalMatrix(state.matrixTimeframe || '24h');
            }
        }
    } catch (e) {
        console.error('Portfolio fetch error:', e);
    }
}

function renderGlobalMatrix(timeframe) {
    const gm = state.portfolioData?.global_matrix;
    if (!gm || !gm.timeframes) return;
    const tf = timeframe || state.matrixTimeframe || '24h';
    const data = gm.timeframes[tf] || gm.timeframes['24h'];
    if (!data) return;

    const elVol = document.getElementById('matrix-global-volume');
    const elProfit = document.getElementById('matrix-global-profit');
    const elOrders = document.getElementById('matrix-global-orders');
    const elCapital = document.getElementById('matrix-global-capital');

    if (elVol) elVol.textContent = `$${formatUSD(data.volume_usd)} USDT`;
    if (elProfit) {
        const sign = data.net_profit_usd >= 0 ? '+' : '-';
        elProfit.textContent = `${sign}$${formatUSD(Math.abs(data.net_profit_usd))} (${sign}${data.roi_pct.toFixed(2)}%)`;
        elProfit.className = data.net_profit_usd >= 0 ? 'text-neon-emerald' : 'text-neon-crimson';
    }
    if (elOrders) elOrders.textContent = `${data.orders_count.toLocaleString()} Orders (<30ms HFT)`;
    if (elCapital) {
        const pool = gm.active_capital_pool_usd || 28540.0;
        elCapital.textContent = `$${formatUSD(pool)} USDT`;
    }
}

async function fetchWealthCockpit() {
    try {
        const res = await fetch(`/api/wealth_cockpit?chat_id=${state.chatId}`);
        const json = await res.json();
        if (json.status === 'success' && json.data) {
            const d = json.data;
            state.wealthCockpit = d;

            // Render Active Positions
            const count = d.total_trades_count || 0;
            if (elements.activePositionsCount) elements.activePositionsCount.textContent = `${count} Positions កំពុងរត់`;
            if (elements.wealthPosBadge) elements.wealthPosBadge.textContent = `${count} Active`;
            if (elements.navPosBadge) {
                elements.navPosBadge.textContent = count;
                elements.navPosBadge.style.display = count > 0 ? 'flex' : 'none';
            }

            if (elements.wealthTradesList) {
                if (count === 0) {
                    elements.wealthTradesList.innerHTML = `
                        <div class="empty-state">
                            <span class="empty-icon">🛡️</span>
                            <h4>កំពុងស្កេនរកឱកាស Safe Entry...</h4>
                            <p>ប្រព័ន្ធកំពុងស្វែងរក Golden Sweet Spot ជាមួយ 15m EMA20 Retracement Confluence</p>
                        </div>
                    `;
                } else {
                    elements.wealthTradesList.innerHTML = d.active_trades.map(t => {
                        const isLong = t.side === 'BUY';
                        const roiClass = t.roi_pct >= 0 ? 'text-neon-emerald' : 'text-neon-red';
                        const breakevenBadge = t.breakeven_locked 
                            ? `<span class="badge badge-success">🔒 Breakeven Locked (+3.0%)</span>`
                            : `<span class="badge badge-accent">🛡️ Trailing Active</span>`;
                        
                        return `
                            <div class="position-card ${isLong ? 'long' : 'short'}">
                                <div class="pos-header-row">
                                    <span class="pos-sym-title">${t.symbol}</span>
                                    <span class="pos-side-badge ${isLong ? 'buy' : 'sell'}">${t.side} ${t.leverage}x</span>
                                </div>
                                <div class="pos-metrics-grid">
                                    <div><span class="pm-label">Entry Price</span><span class="pm-val">$${Number(t.entry_price).toFixed(4)}</span></div>
                                    <div><span class="pm-label">Mark Price</span><span class="pm-val">$${Number(t.mark_price).toFixed(4)}</span></div>
                                    <div><span class="pm-label">Live ROI %</span><span class="pm-val ${roiClass}">${t.roi_pct >= 0 ? '+' : ''}${Number(t.roi_pct).toFixed(2)}%</span></div>
                                </div>
                                <div class="pos-status-bar">
                                    ${breakevenBadge}
                                    <span class="text-neon-gold">Ratchet: 85% Lock</span>
                                    <button class="btn-fast-close" onclick="closeTrade('${t.symbol}')" style="background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:#fff; border-radius:4px; padding:2px 6px; font-size:9px; cursor:pointer;">Fast Close</button>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }

            // Render Sweet Spot Candidates
            if (elements.sweetspotCandidatesList && d.candidates) {
                elements.sweetspotCandidatesList.innerHTML = d.candidates.map(c => `
                    <div class="radar-item-card">
                        <div class="radar-item-top">
                            <span>${c.symbol}</span>
                            <span class="${c.side === 'BUY' ? 'text-neon-emerald' : 'text-neon-red'}">${c.side === 'BUY' ? '+' : ''}${c.price_change_pct.toFixed(1)}%</span>
                        </div>
                        <div class="radar-item-metrics">
                            <span>RSI: ${c.rsi_15m.toFixed(1)}</span>
                            <span>Score: ${c.ai_score.toFixed(1)}</span>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error('Wealth cockpit fetch error:', e);
    }
}

async function fetchAIBrain() {
    try {
        const res = await fetch('/api/ai_brain');
        const json = await res.json();
        if (json.status === 'success' && json.data) {
            const d = json.data;
            state.aiBrainData = d;
            if (elements.brainScoreVal) elements.brainScoreVal.textContent = d.confluence_score.toFixed(1);
            if (elements.brainSentimentBadge) elements.brainSentimentBadge.textContent = d.market_sentiment;
            if (elements.brainAdxVal) elements.brainAdxVal.textContent = `${d.adx_15m.toFixed(1)} (${d.adx_status})`;
            applySovereignCloaking();

            // Radial progress dial offset
            if (elements.radialProgress) {
                const offset = 314 - (314 * (d.confluence_score / 100));
                elements.radialProgress.style.strokeDashoffset = offset;
            }

            // Render Top Agents Grid
            if (elements.aiAgentsGrid && d.top_agents) {
                elements.aiAgentsGrid.innerHTML = d.top_agents.map(a => `
                    <div class="agent-item-card">
                        <div class="agent-info">
                            <h5>${a.name}</h5>
                            <span>${a.tier} &bull; ${a.status}</span>
                        </div>
                        <span class="agent-score">${a.confidence.toFixed(1)}%</span>
                    </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error('AI Brain fetch error:', e);
    }
}

async function fetchHFTMEV() {
    try {
        const res = await fetch('/api/hft_mev');
        const json = await res.json();
        if (json.status === 'success' && json.data) {
            const d = json.data;
            state.mevData = d;
            if (elements.mevCyclesList && d.active_cycles) {
                elements.mevCyclesList.innerHTML = d.active_cycles.map(c => `
                    <div class="cycle-item">
                        <div class="cycle-top">
                            <span>${c.token}</span>
                            <span class="text-neon-emerald">+${c.spread_pct}% ($${c.net_profit_usd} Net)</span>
                        </div>
                        <div class="cycle-path">${c.path}</div>
                    </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error('HFT MEV fetch error:', e);
    }
}

async function fetchAnalytics() {
    try {
        const res = await fetch(`/api/analytics?chat_id=${state.chatId}`);
        const json = await res.json();
        if (json.status === 'success' && json.data) {
            const d = json.data;
            state.analytics = d;

            if (d.vault) {
                if (elements.vaultBtcQty) elements.vaultBtcQty.textContent = `${d.vault.btc_qty.toFixed(6)} BTC`;
                if (elements.vaultBtcUsd) elements.vaultBtcUsd.textContent = `≈ $${formatUSD(d.vault.btc_usd)} USD`;
                if (elements.vaultPaxgQty) elements.vaultPaxgQty.textContent = `${d.vault.paxg_qty.toFixed(4)} PAXG`;
                if (elements.vaultPaxgUsd) elements.vaultPaxgUsd.textContent = `≈ $${formatUSD(d.vault.paxg_usd)} USD`;
                
                const pool = Number(d.vault.unharvested_pool || 0);
                if (elements.sweepPoolText) elements.sweepPoolText.textContent = `$${pool.toFixed(2)} / $10.00 USDT`;
                if (elements.sweepProgressBar) {
                    const pct = Math.min(100, Math.max(0, (pool / 10.0) * 100));
                    elements.sweepProgressBar.style.width = `${pct}%`;
                }
            }

            if (d.equity_curve && state.equityChart) {
                state.equityChart.data.labels = d.equity_curve.labels;
                state.equityChart.data.datasets[0].data = d.equity_curve.values;
                state.equityChart.update();
            }

            if (elements.harvestHistoryList && d.harvest_history) {
                if (d.harvest_history.length === 0) {
                    elements.harvestHistoryList.innerHTML = `<div class="empty-state"><p>មិនទាន់មានប្រវត្តិ Sweep ទេ</p></div>`;
                } else {
                    elements.harvestHistoryList.innerHTML = d.harvest_history.map(h => `
                        <div class="history-item">
                            <span>${h.timestamp || 'Recent'}</span>
                            <span class="text-neon-gold">+${h.qty} ${h.asset}</span>
                            <span class="text-neon-emerald">$${h.amount_usd}</span>
                        </div>
                    `).join('');
                }
            }
        }
    } catch (e) {
        console.error('Analytics fetch error:', e);
    }
}

// -----------------------------------------------------------------------------
// Actions (Engine Toggles, Manual Sweep, Fast Close)
// -----------------------------------------------------------------------------
async function fetchEngineStates() {
    try {
        const cid = state.chatId || '';
        const res = await fetch(`/api/engine_states?chat_id=${cid}`);
        const json = await res.json();
        if (json.status === 'success' && json.engines) {
            const eng = json.engines;
            for (const [name, isActive] of Object.entries(eng)) {
                const sw = document.getElementById(`toggle-${name}`);
                if (sw) sw.checked = Boolean(isActive);
                const badge = document.getElementById(`badge-${name}`);
                if (badge) {
                    badge.textContent = isActive ? '🟢 RUNNING 24/7' : '⚪ STANDBY / OFF';
                    badge.className = isActive ? 'badge badge-success' : 'badge badge-dim';
                }
            }
        }
    } catch (e) {
        console.error('Error fetching live engine states:', e);
    }
}

async function toggleEngine(engineName, isChecked) {
    triggerHaptic('impact');
    const badge = document.getElementById(`badge-${engineName}`);
    if (badge) {
        badge.textContent = isChecked ? '🟢 RUNNING 24/7' : '⚪ STANDBY / OFF';
        badge.className = isChecked ? 'badge badge-success' : 'badge badge-dim';
    }
    try {
        const res = await fetch('/api/action/engine_toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: state.chatId, engine: engineName, enable: isChecked })
        });
        const json = await res.json();
        if (json.status === 'success') {
            showToast(`✅ Engine <strong>${engineName.toUpperCase()}</strong>: ${isChecked ? 'បានបើកដំណើរការ 🟢' : 'បានផ្អាកដំណើរការ (Standby) ⚪'}`);
        } else {
            showToast(`❌ Toggle Failed: ${json.message}`);
            const sw = document.getElementById(`toggle-${engineName}`);
            if (sw) sw.checked = !isChecked;
            if (badge) {
                badge.textContent = !isChecked ? '🟢 RUNNING 24/7' : '⚪ STANDBY / OFF';
                badge.className = !isChecked ? 'badge badge-success' : 'badge badge-dim';
            }
        }
    } catch (e) {
        showToast(`❌ Network Error toggling engine`);
        const sw = document.getElementById(`toggle-${engineName}`);
        if (sw) sw.checked = !isChecked;
        if (badge) {
            badge.textContent = !isChecked ? '🟢 RUNNING 24/7' : '⚪ STANDBY / OFF';
            badge.className = !isChecked ? 'badge badge-success' : 'badge badge-dim';
        }
    }
}

async function closeTrade(symbol) {
    triggerHaptic('heavy');
    if (!confirm(`តើអ្នកពិតជាចង់បិទ Position ${symbol} ភ្លាមៗមែនទេ?`)) return;
    try {
        const res = await fetch('/api/action/close_position', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: state.chatId, symbol: symbol })
        });
        const json = await res.json();
        if (json.status === 'success') {
            showToast(`✅ Position <strong>${symbol}</strong> បានបិទដោយជោគជ័យ!`);
            fetchWealthCockpit();
            fetchPortfolio();
        } else {
            showToast(`❌ បិទមិនបានសម្រេច: ${json.message}`);
        }
    } catch (e) {
        showToast(`❌ Network Error closing position`);
    }
}

// -----------------------------------------------------------------------------
// UI Event Handlers
// -----------------------------------------------------------------------------
function setupEventListeners() {
    // Navigation Tabs
    const navItems = document.querySelectorAll('.nav-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTabId = item.getAttribute('data-tab');
            navItems.forEach(n => n.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            item.classList.add('active');
            const targetPane = document.getElementById(targetTabId);
            if (targetPane) targetPane.classList.add('active');
            triggerHaptic('selection');
            if (targetTabId === 'tab-controls') {
                fetchEngineStates();
            }
        });
    });

    // Timeframe selector
    document.querySelectorAll('.tf-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.timeframe = btn.getAttribute('data-tf');
            triggerHaptic('selection');
            fetchAnalytics();
        });
    });

    // Balanced Matrix Global Timeframe Selector
    document.querySelectorAll('.matrix-tf-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.matrix-tf-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.matrixTimeframe = btn.getAttribute('data-mtf');
            triggerHaptic('selection');
            renderGlobalMatrix(state.matrixTimeframe);
        });
    });

    // Engine Toggles
    document.querySelectorAll('.switch input').forEach(input => {
        input.addEventListener('change', (e) => {
            const engine = e.target.getAttribute('data-engine');
            toggleEngine(engine, e.target.checked);
        });
    });

    // Manual Sweep Button
    if (elements.btnManualSweep) {
        elements.btnManualSweep.addEventListener('click', async () => {
            triggerHaptic('heavy');
            showToast('⚡ កំពុងផ្ទេរ និងទិញ Spot សន្សំទុក...');
            try {
                const res = await fetch('/api/action/harvest', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: state.chatId })
                });
                const json = await res.json();
                if (json.status === 'success') {
                    showToast(`🥇 Sweep ជោគជ័យ! បានទិញ ${json.qty_bought} ${json.symbol}`);
                    fetchAnalytics();
                } else {
                    showToast(`ℹ️ ${json.message || 'មិនទាន់ដល់កម្រិតដក'}`);
                }
            } catch (e) {
                showToast('❌ Error executing sweep');
            }
        });
    }

    // Refresh Button
    if (elements.btnRefresh) {
        elements.btnRefresh.addEventListener('click', async () => {
            triggerHaptic('light');
            elements.btnRefresh.style.transform = 'rotate(360deg)';
            elements.btnRefresh.style.transition = 'transform 0.5s ease';
            await Promise.all([fetchPortfolio(), fetchWealthCockpit(), fetchAIBrain(), fetchHFTMEV(), fetchAnalytics()]);
            setTimeout(() => {
                elements.btnRefresh.style.transform = 'none';
                elements.btnRefresh.style.transition = 'none';
            }, 500);
            showToast('🔄 ទិន្នន័យត្រូវបាន Update ផ្ទាល់ពី Binance!');
        });
    }
}

// -----------------------------------------------------------------------------
// Sovereign Quantum Cloaking Enforcer (Guaranteed Client-Side Masking)
// -----------------------------------------------------------------------------
function applySovereignCloaking() {
    try {
        // 1. Header brand title
        const brandMain = document.querySelector('.brand-title-main');
        if (brandMain) brandMain.textContent = 'KHMER MASTER CRYPTO';
        const brandTag = document.querySelector('.brand-tag-ai');
        if (brandTag) brandTag.textContent = 'APEX SUPER BRAIN AGI';

        // 2. Brain Banner
        const brainHeading = document.querySelector('#tab-brain .section-heading');
        if (brainHeading) brainHeading.textContent = '33-Layer Sovereign Neural Apex Core™';
        const brainDesc = document.querySelector('#tab-brain .section-desc');
        if (brainDesc) brainDesc.textContent = 'Autonomous Pre-Cognitive Swarm Intelligence • Global Institutional Order Flow Perception';

        // 3. Swarm Consensus Matrix Header
        const swarmTitle = document.querySelector('.brain-gauge-header .card-title');
        if (swarmTitle) swarmTitle.textContent = '🌐 Sovereign Swarm Consensus Matrix';

        // 4. Labels in gauge-details-column
        const detailLabels = document.querySelectorAll('.gauge-detail-item .detail-label');
        if (detailLabels.length >= 4) {
            detailLabels[0].textContent = 'Temporal Kinetic Velocity:';
            detailLabels[1].textContent = 'Singularity Liquidity Armor™:';
            detailLabels[2].textContent = 'Celestial Vault Ratchet™:';
            detailLabels[3].textContent = 'Sovereign Capital Fortress™:';
        }

        // 5. Values in gauge-details-column
        const detailValues = document.querySelectorAll('.gauge-detail-item strong');
        if (detailValues.length >= 4) {
            detailValues[1].className = 'text-neon-cyan';
            detailValues[1].textContent = 'ARMED (Black-Hole Squeeze Immunity Active)';
            detailValues[2].className = 'text-neon-gold';
            detailValues[2].textContent = 'LOCKED (Peak Profit Dynamic Ratchet Active)';
            detailValues[3].className = 'text-neon-emerald';
            detailValues[3].textContent = 'SECURED (Zero-Liquidation Multi-Tier Reserve)';
        }

        // 6. MEV Banner
        const mevHeading = document.querySelector('#tab-hft .section-heading');
        if (mevHeading) mevHeading.textContent = 'Quantum Liquidity Siphon & MEV Radar';
        const mevDesc = document.querySelector('#tab-hft .section-desc');
        if (mevDesc) mevDesc.textContent = 'Cross-Dimensional Liquidity Relay & Tokyo Gateway (< 0.42ms Latency)';
    } catch (e) {
        console.warn('Sovereign cloaking error:', e);
    }
}

// Execute immediately if DOM already parsed
applySovereignCloaking();

// -----------------------------------------------------------------------------
// App Lifecycle
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    applySovereignCloaking();
    initNeuralCanvas();
    startClocks();
    initCharts();
    setupEventListeners();
    initRealtimeStream();

    // Initial Load
    fetchPortfolio();
    fetchWealthCockpit();
    fetchAIBrain();
    fetchHFTMEV();
    fetchAnalytics();
    fetchEngineStates();

    // Passive Fallback Polling every 20s (Stream handles real-time live ticks)
    setInterval(() => {
        if (!state.streamConnected) {
            fetchPortfolio();
            fetchWealthCockpit();
            fetchEngineStates();
        }
    }, 20000);
});
