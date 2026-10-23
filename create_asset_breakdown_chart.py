# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('data/capital_m15_1m_backtest_trade_ledger.csv')
agg = df.groupby('symbol').agg(
    trades=('trade_id', 'count'),
    wins=('pnl_dollars', lambda x: (x > 0).sum()),
    net_pnl=('pnl_dollars', 'sum')
).reset_index()
agg['win_rate'] = (agg['wins'] / agg['trades'] * 100).round(1)
agg = agg.sort_values('net_pnl', ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 5.2))
colors_list = ['#059669' if x >= 0 else '#DC2626' for x in agg['net_pnl']]
bars = ax.barh(agg['symbol'], agg['net_pnl'], color=colors_list, height=0.62, alpha=0.9, edgecolor='#0F172A', linewidth=0.8)

ax.axvline(0, color='#64748B', linestyle='--', linewidth=1.2, alpha=0.7)
ax.set_title('ANGKOR QUANT — 1-Month M15 Net PnL by TradFi Asset ($1,000 Capital)', fontsize=13, fontweight='bold', pad=12, color='#0F172A')
ax.set_xlabel('Realized Net Profit / Loss ($ USD)', fontsize=11, fontweight='bold', color='#1E293B')
ax.grid(axis='x', alpha=0.3, linestyle=':')

min_x, max_x = agg['net_pnl'].min(), agg['net_pnl'].max()
ax.set_xlim(min_x - 15, max_x + 22)

for bar, (_, row) in zip(bars, agg.iterrows()):
    w = bar.get_width()
    x_pos = w + (1.2 if w >= 0 else -1.2)
    ha = 'left' if w >= 0 else 'right'
    tr = int(row['trades'])
    wr = row['win_rate']
    txt = f"${w:+,.2f} ({tr}t | {wr}% WR)"
    ax.text(x_pos, bar.get_y() + bar.get_height()/2.0, txt, va='center', ha=ha, fontsize=8.5, fontweight='bold', color='#0F172A')

plt.tight_layout()
p = os.path.join('data', 'capital_m15_1m_asset_breakdown.png')
fig.savefig(p, dpi=300)
plt.close(fig)
print('Generated asset breakdown chart successfully:', p)
