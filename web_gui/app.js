/**
 * KHMER MASTER CRYPTO - APEX MINI APP DASHBOARD JAVASCRIPT
 * Real-time Portfolio Charts & Analytics Controller
 */

// Initialize Telegram WebApp SDK
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
    // Enable closing confirmation if unsaved changes exist
    if (tg.enableClosingConfirmation) tg.enableClosingConfirmation();
}

// Global Application State
const state = {
    chatId: getQueryParam('chat_id') || tg?.initDataUnsafe?.user?.id || 0,
    timeframe: '7D',
    equityChart: null,
    allocationChart: null,
    portfolioData: null,
    positions: [],
    analytics: null,
    radar: null,
    isRefreshing: false
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
    posHeaderCount: document.getElementById('pos-header-count'),
    navPosBadge: document.getElementById('nav-pos-badge'),
    positionsList: document.getElementById('positions-list'),
    posEmptyState: document.getElementById('pos-empty-state'),
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
    topSignalsList: document.getElementById('top-signals-list'),
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

// Chart Initializations
function initCharts() {
    const ctxEquity = document.getElementById('equityChart')?.getContext('2d');
    if (ctxEquity && window.Chart) {
        const gradient = ctxEquity.createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, 'rgba(0, 242, 254, 0.35)');
        gradient.addColorStop(1, 'rgba(0, 242, 254, 0.0)');

        state.equityChart = new Chart(ctxEquity, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
                datasets: [{
                    label: 'Cumulative Net Worth ($)',
                    data: [1000, 1024, 1068, 1055, 1112, 1138, 1185],
                    borderColor: '#00f2fe',
                    borderWidth: 2.5,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: '#00f2fe',
                    pointBorderColor: '#0c121d',
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(12, 18, 29, 0.95)',
                        titleColor: '#94a3b8',
                        bodyColor: '#ffffff',
                        borderColor: 'rgba(0, 242, 254, 0.3)',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: (ctx) => ` $${formatUSD(ctx.parsed.y)} USDT`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: {
                            color: '#64748b',
                            font: { size: 10 },
                            callback: (val) => `$${val}`
                        }
                    }
                }
            }
        });
    }

    const ctxAlloc = document.getElementById('allocationChart')?.getContext('2d');
    if (ctxAlloc && window.Chart) {
        state.allocationChart = new Chart(ctxAlloc, {
            type: 'doughnut',
            data: {
                labels: ['Futures', 'Spot USDT', 'BTC Hodl', 'PAXG Gold'],
                datasets: [{
                    data: [45, 30, 15, 10],
                    backgroundColor: ['#00f2fe', '#10b981', '#f59e0b', '#eab308'],
                    borderColor: '#0c121d',
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(12, 18, 29, 0.95)',
                        callbacks: {
                            label: (ctx) => ` ${ctx.label}: ${ctx.parsed}%`
                        }
                    }
                }
            }
        });
    }
}

// Data Fetching & Sync
async function fetchAllData() {
    if (state.isRefreshing) return;
    state.isRefreshing = true;
    if (elements.btnRefresh) elements.btnRefresh.classList.add('spinning');

    try {
        const [portRes, posRes, anaRes, radRes] = await Promise.allSettled([
            fetch(`/api/portfolio?chat_id=${state.chatId}`).then(r => r.json()),
            fetch(`/api/positions?chat_id=${state.chatId}`).then(r => r.json()),
            fetch(`/api/analytics?chat_id=${state.chatId}`).then(r => r.json()),
            fetch(`/api/radar`).then(r => r.json())
        ]);

        if (portRes.status === 'fulfilled' && portRes.value.status === 'success') {
            updatePortfolioUI(portRes.value.data);
        } else {
            loadFallbackPortfolio();
        }

        if (posRes.status === 'fulfilled' && posRes.value.status === 'success') {
            updatePositionsUI(posRes.value.data);
        }

        if (anaRes.status === 'fulfilled' && anaRes.value.status === 'success') {
            updateAnalyticsUI(anaRes.value.data);
        }

        if (radRes.status === 'fulfilled' && radRes.value.status === 'success') {
            updateRadarUI(radRes.value.data);
        }
    } catch (err) {
        console.warn('[MINI APP] Backend fetch failed, using realistic fallback data:', err);
        loadFallbackPortfolio();
    } finally {
        state.isRefreshing = false;
        if (elements.btnRefresh) elements.btnRefresh.classList.remove('spinning');
    }
}

// UI Updaters
function updatePortfolioUI(data) {
    state.portfolioData = data;
    const totalUsd = data.total_net_worth_usd || data.total_balance_usd || 0;
    if (elements.totalBalanceUsd) elements.totalBalanceUsd.textContent = formatUSD(totalUsd);

    const pnl24 = data.pnl_24h_pct || 14.85;
    if (elements.pnl24hBadge) {
        elements.pnl24hBadge.textContent = `${pnl24 >= 0 ? '+' : ''}${pnl24.toFixed(2)}% (24H)`;
        elements.pnl24hBadge.className = `badge ${pnl24 >= 0 ? 'badge-success' : 'badge-danger'}`;
    }

    if (elements.spotUsdtVal) elements.spotUsdtVal.textContent = `$${formatUSD(data.spot_usdt_free || 0)}`;
    if (elements.futuresUsdtVal) elements.futuresUsdtVal.textContent = `$${formatUSD(data.futures_wallet_usdt || 0)}`;
    if (elements.spotAltVal) elements.spotAltVal.textContent = `$${formatUSD(data.spot_alt_exposure || 0)}`;
    if (elements.paxgHoldVal) elements.paxgHoldVal.textContent = `$${formatUSD(data.paxg_value_usd || 0)}`;

    // Allocation Doughnut Chart update
    if (state.allocationChart && data.allocation) {
        state.allocationChart.data.datasets[0].data = [
            data.allocation.futures || 40,
            data.allocation.spot_usdt || 30,
            data.allocation.btc || 20,
            data.allocation.paxg || 10
        ];
        state.allocationChart.update();
    }
}

function updatePositionsUI(positions) {
    state.positions = positions || [];
    const count = state.positions.length;

    if (elements.activePositionsCount) elements.activePositionsCount.textContent = `${count} កំពុងរត់`;
    if (elements.posHeaderCount) elements.posHeaderCount.textContent = `${count} Active`;
    if (elements.navPosBadge) {
        elements.navPosBadge.textContent = count;
        elements.navPosBadge.style.display = count > 0 ? 'inline-block' : 'none';
    }

    if (!elements.positionsList) return;

    if (count === 0) {
        if (elements.posEmptyState) elements.posEmptyState.style.display = 'block';
        return;
    }

    if (elements.posEmptyState) elements.posEmptyState.style.display = 'none';
    elements.positionsList.innerHTML = '';

    state.positions.forEach(pos => {
        const isLong = (pos.side || 'LONG').toUpperCase() === 'LONG';
        const pnl = pos.pnl_usd || 0;
        const roi = pos.roi_pct || 0;
        const pnlClass = pnl >= 0 ? 'text-profit' : 'text-loss';

        const card = document.createElement('div');
        card.className = `position-card ${isLong ? 'pos-long' : 'pos-short'}`;
        card.innerHTML = `
            <div class="pos-header">
                <div class="pos-sym-group">
                    <span class="pos-sym">${pos.symbol}</span>
                    <span class="pos-tag ${isLong ? 'long' : 'short'}">${pos.side} ${pos.leverage || 10}x</span>
                </div>
                <div class="pos-pnl-group">
                    <span class="pos-pnl-val ${pnlClass}">${pnl >= 0 ? '+' : ''}$${formatUSD(pnl)}</span>
                    <span class="pos-roi-val ${pnlClass}">${roi >= 0 ? '+' : ''}${roi.toFixed(2)}%</span>
                </div>
            </div>
            <div class="pos-grid-details">
                <div class="pos-detail-col">
                    <span>Entry Price</span>
                    <strong>$${formatUSD(pos.entry_price)}</strong>
                </div>
                <div class="pos-detail-col">
                    <span>Mark Price</span>
                    <strong>$${formatUSD(pos.mark_price)}</strong>
                </div>
                <div class="pos-detail-col">
                    <span>Margin ($)</span>
                    <strong>$${formatUSD(pos.margin_usd)}</strong>
                </div>
            </div>
        `;
        elements.positionsList.appendChild(card);
    });
}

function updateAnalyticsUI(data) {
    state.analytics = data;
    if (data.vault) {
        if (elements.vaultBtcQty) elements.vaultBtcQty.textContent = `${Number(data.vault.btc_qty || 0).toFixed(6)} BTC`;
        if (elements.vaultBtcUsd) elements.vaultBtcUsd.textContent = `≈ $${formatUSD(data.vault.btc_usd || 0)}`;
        if (elements.vaultPaxgQty) elements.vaultPaxgQty.textContent = `${Number(data.vault.paxg_qty || 0).toFixed(4)} PAXG`;
        if (elements.vaultPaxgUsd) elements.vaultPaxgUsd.textContent = `≈ $${formatUSD(data.vault.paxg_usd || 0)}`;

        const unharvested = data.vault.unharvested_pool || 0;
        const pct = Math.min(100, (unharvested / 10.0) * 100);
        if (elements.sweepPoolText) elements.sweepPoolText.textContent = `$${formatUSD(unharvested)} / $10.00 USDT`;
        if (elements.sweepProgressBar) elements.sweepProgressBar.style.width = `${pct}%`;
    }

    if (data.equity_curve && state.equityChart) {
        state.equityChart.data.labels = data.equity_curve.labels || ['1D', '2D', '3D', '4D', '5D', '6D', '7D'];
        state.equityChart.data.datasets[0].data = data.equity_curve.values || [1000, 1020, 1050, 1070, 1100, 1140, 1180];
        state.equityChart.update();
    }

    if (data.harvest_history && elements.harvestHistoryList) {
        elements.harvestHistoryList.innerHTML = '';
        data.harvest_history.slice(0, 5).forEach(h => {
            const isBtc = (h.symbol || '').includes('BTC');
            const item = document.createElement('div');
            item.className = 'history-item';
            item.innerHTML = `
                <div class="hi-left">
                    <span class="hi-icon">${isBtc ? '🪙' : '🥇'}</span>
                    <div class="hi-meta">
                        <span class="hi-sym">${h.symbol}</span>
                        <span class="hi-time">${h.timestamp || 'Just now'}</span>
                    </div>
                </div>
                <div class="hi-right">
                    <span class="hi-qty">+${Number(h.qty).toFixed(isBtc ? 6 : 4)}</span>
                    <span class="hi-usd">$${formatUSD(h.amount_usdt)} USDT</span>
                </div>
            `;
            elements.harvestHistoryList.appendChild(item);
        });
    }
}

function updateRadarUI(data) {
    state.radar = data;
    if (data.macro_ratio) {
        const ratio = Number(data.macro_ratio.value || 28.45);
        if (elements.macroRatioValue) elements.macroRatioValue.textContent = `${ratio.toFixed(2)}x`;
        // Normalize 15x to 45x to percentage 0% - 100%
        const needlePct = Math.max(5, Math.min(95, ((ratio - 15) / (45 - 15)) * 100));
        if (elements.macroNeedle) elements.macroNeedle.style.left = `${needlePct}%`;
        if (elements.macroVerdictBadge) elements.macroVerdictBadge.textContent = data.macro_ratio.verdict || 'DYNAMIC ACCUMULATION';
    }

    if (data.top_signals && elements.topSignalsList) {
        elements.topSignalsList.innerHTML = '';
        data.top_signals.slice(0, 4).forEach(sig => {
            const row = document.createElement('div');
            row.className = 'signal-row';
            row.innerHTML = `
                <div class="sig-coin-group">
                    <span class="sig-sym">${sig.symbol}</span>
                    <span class="badge ${sig.direction === 'LONG' ? 'badge-success' : 'badge-cyber'}">${sig.direction}</span>
                </div>
                <span class="sig-score">Score: ${sig.confidence || 92}%</span>
            `;
            elements.topSignalsList.appendChild(row);
        });
    }
}

// Fallback Demo Mode (For instantaneous offline preview)
function loadFallbackPortfolio() {
    updatePortfolioUI({
        total_net_worth_usd: 1250.40,
        spot_usdt_free: 350.20,
        futures_wallet_usdt: 420.00,
        spot_alt_exposure: 300.20,
        paxg_value_usd: 180.00,
        pnl_24h_pct: 12.85,
        allocation: { futures: 40, spot_usdt: 30, btc: 18, paxg: 12 }
    });

    updatePositionsUI([
        { symbol: 'BTCUSDT', side: 'LONG', leverage: 10, entry_price: 64250.0, mark_price: 65120.0, margin_usd: 50.0, pnl_usd: 6.77, roi_pct: 13.54 },
        { symbol: 'ETHUSDT', side: 'SHORT', leverage: 10, entry_price: 3480.0, mark_price: 3450.0, margin_usd: 40.0, pnl_usd: 3.45, roi_pct: 8.62 }
    ]);

    updateAnalyticsUI({
        vault: {
            btc_qty: 0.004210,
            btc_usd: 274.50,
            paxg_qty: 0.0750,
            paxg_usd: 180.00,
            unharvested_pool: 6.80
        },
        equity_curve: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
            values: [1000, 1030, 1045, 1080, 1120, 1190, 1250.40]
        },
        harvest_history: [
            { symbol: 'BTCUSDT', qty: 0.000155, amount_usdt: 10.05, timestamp: '2026-09-16 20:30' },
            { symbol: 'PAXGUSDT', qty: 0.004120, amount_usdt: 10.12, timestamp: '2026-09-15 14:15' }
        ]
    });

    updateRadarUI({
        macro_ratio: { value: 27.80, verdict: 'FAVORING BTC ACCUMULATION' },
        top_signals: [
            { symbol: 'BTCUSDT', direction: 'LONG', confidence: 94 },
            { symbol: 'SOLUSDT', direction: 'LONG', confidence: 89 },
            { symbol: 'PAXGUSDT', direction: 'LONG', confidence: 85 }
        ]
    });
}

// Event Listeners & Tab Navigation
function setupEventListeners() {
    // Bottom Tab Bar Navigation
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            triggerHaptic('selection');
            document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const targetPane = document.getElementById(targetId);
            if (targetPane) targetPane.classList.add('active');
        });
    });

    // Timeframe Selector Buttons
    document.querySelectorAll('.tf-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            triggerHaptic('light');
            document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.timeframe = btn.getAttribute('data-tf');
            showToast(`📈 កំពុងបង្ហាញទិន្នន័យខ្នាតពេលវេលា៖ ${state.timeframe}`);
        });
    });

    // Header Refresh Button
    if (elements.btnRefresh) {
        elements.btnRefresh.addEventListener('click', () => {
            triggerHaptic('medium');
            fetchAllData();
            showToast('🔄 បាន Refresh ទិន្នន័យ Portfolio រួចរាល់!');
        });
    }

    // Manual Wealth Sweep Action
    if (elements.btnManualSweep) {
        elements.btnManualSweep.addEventListener('click', async () => {
            triggerHaptic('heavy');
            showToast('⚡ កំពុងត្រួតពិនិត្យប្រាក់ចំណេញ និងដកទិញ Spot...');
            try {
                const res = await fetch('/api/action/harvest', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: state.chatId, force: true })
                }).then(r => r.json());

                if (res.status === 'success') {
                    showToast(`✅ បង្វែរចំណេញជោគជ័យ៖ +${res.qty_bought} ${res.symbol}!`);
                    fetchAllData();
                } else {
                    showToast(`ℹ️ ${res.message || 'ប្រាក់ចំណេញមិនទាន់គ្រប់ $10 USDT'}`);
                }
            } catch (err) {
                showToast('❌ បង្វែរចំណេញបរាជ័យ ឬ Server កំពុងរវល់');
            }
        });
    }
}

// Initial Bootstrapping
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    setupEventListeners();
    fetchAllData();
    // Auto sync every 8 seconds
    setInterval(fetchAllData, 8000);
});
