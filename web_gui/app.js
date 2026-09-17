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
    sseSource: null
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
// Real-Time Server-Sent Events (SSE) Stream Controller
// -----------------------------------------------------------------------------
function initRealtimeSSEStream() {
    if (state.sseSource) {
        state.sseSource.close();
    }
    const sseUrl = `/api/stream?chat_id=${state.chatId}`;
    try {
        state.sseSource = new EventSource(sseUrl);
        state.sseSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data) {
                    if (elements.latencyVal) elements.latencyVal.textContent = `${data.hft_latency_ms} ms`;
                    if (elements.hftSyncTicker) elements.hftSyncTicker.textContent = `0.001ms TOKYO HFT SYNC • LIVE (${data.timestamp})`;
                }
            } catch (err) {}
        };
        state.sseSource.onerror = () => {
            state.sseSource.close();
            // Fallback to polling every 3 seconds if SSE is blocked
            setTimeout(initRealtimeSSEStream, 5000);
        };
    } catch (e) {
        console.warn('SSE not supported, using polling fallback');
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

            if (d.allocation && state.allocationChart) {
                state.allocationChart.data.datasets[0].data = [
                    d.allocation.futures,
                    d.allocation.spot_usdt,
                    d.allocation.btc,
                    d.allocation.paxg
                ];
                state.allocationChart.update();
                document.getElementById('leg-fut-pct').textContent = `${d.allocation.futures}%`;
                document.getElementById('leg-spot-pct').textContent = `${d.allocation.spot_usdt}%`;
                document.getElementById('leg-btc-pct').textContent = `${d.allocation.btc}%`;
                document.getElementById('leg-paxg-pct').textContent = `${d.allocation.paxg}%`;
            }
        }
    } catch (e) {
        console.error('Portfolio fetch error:', e);
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
async function toggleEngine(engineName, isChecked) {
    triggerHaptic('impact');
    try {
        const res = await fetch('/api/action/engine_toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: state.chatId, engine: engineName, enable: isChecked })
        });
        const json = await res.json();
        if (json.status === 'success') {
            showToast(`✅ Engine <strong>${engineName.toUpperCase()}</strong>: ${isChecked ? 'ENABLED 🟢' : 'DISABLED 🔴'}`);
        } else {
            showToast(`❌ Toggle Failed: ${json.message}`);
        }
    } catch (e) {
        showToast(`❌ Network Error toggling engine`);
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
// App Lifecycle
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initNeuralCanvas();
    startClocks();
    initCharts();
    setupEventListeners();
    initRealtimeSSEStream();

    // Initial Load
    fetchPortfolio();
    fetchWealthCockpit();
    fetchAIBrain();
    fetchHFTMEV();
    fetchAnalytics();

    // Auto Refresh Interval every 3s
    setInterval(() => {
        fetchPortfolio();
        fetchWealthCockpit();
    }, 3000);
});
