import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('data/pesca_nacional_2014_2024.csv')
df['Origen'] = df['Origen'].str.strip().str.upper()
df['Tipogua'] = df['Tipogua'].str.strip().str.upper()

# quiebre: acuacultura dulce 2014-2018 vs 2019-2024
ad = df[(df['Origen']=='ACUACULTURA') & (df['Tipogua']=='DULCE')].groupby('Anio')['PesoVivo'].sum()/1e3
am = df[(df['Origen']=='ACUACULTURA') & (df['Tipogua']!='DULCE')].groupby('Anio')['PesoVivo'].sum()/1e3
cap = df[df['Origen']=='CAPTURA'].groupby('Anio')['PesoVivo'].sum()/1e3

print('=== QUIEBRE acuacultura DULCE (miles ton) ===')
print(f"  2014-2018 promedio: {ad[ad.index<=2018].mean():.0f} mil ton")
print(f"  2019-2024 promedio: {ad[ad.index>=2019].mean():.0f} mil ton")
print(f"  caída aparente: {(1-ad[ad.index>=2019].mean()/ad[ad.index<=2018].mean())*100:.0f}%")
print(f"\n  CAPTURA 2014-2018: {cap[cap.index<=2018].mean():.0f} vs 2019-2024: {cap[cap.index>=2019].mean():.0f} mil ton (estable)")
print(f"  ACUACULTURA marina 2014-2018: {am[am.index<=2018].mean():.0f} vs 2019-2024: {am[am.index>=2019].mean():.0f} mil ton (crece)")

# top especies por origen
print('\n=== TOP 8 especies por ORIGEN (total 2014-2024, miles ton) ===')
for o in ['CAPTURA','ACUACULTURA']:
    s = df[df['Origen']==o].groupby('Especie')['PesoVivo'].sum().sort_values(ascending=False)/1e3
    print(f'  {o}: ' + ', '.join(f'{e} {v:.0f}' for e,v in s.head(8).items()))

# top estados por origen
print('\n=== TOP 8 estados por ORIGEN (miles ton) ===')
for o in ['CAPTURA','ACUACULTURA']:
    s = df[df['Origen']==o].groupby('Estado')['PesoVivo'].sum().sort_values(ascending=False)/1e3
    print(f'  {o}: ' + ', '.join(f'{e} {v:.0f}' for e,v in s.head(8).items()))

# ---- gráficos ----
fig, axes = plt.subplots(2, 2, figsize=(13, 8))

# 1. captura vs acuacultura
a = axes[0,0]
g = df.groupby(['Anio','Origen'])['PesoVivo'].sum().unstack()/1e6
a.plot(g.index, g['CAPTURA'], color='#1f77b4', lw=2, marker='o', label='Captura')
a.plot(g.index, g['ACUACULTURA'], color='#2ca02c', lw=2, marker='o', label='Acuacultura')
a.axvline(2018.5, ls=':', color='gray'); a.text(2018.6, 300, '2018', fontsize=8, color='gray')
a.set_title('Captura vs Acuacultura (M ton)'); a.legend(); a.grid(alpha=0.3)

# 2. acuacultura dulce vs marina
b = axes[0,1]
ac = df[df['Origen']=='ACUACULTURA'].groupby(['Anio','Tipogua'])['PesoVivo'].sum().unstack()/1e3
for col, c, lab in [('DULCE','#d62728','Dulce (interior)'), ('SALOBRE / MARINA','#2ca02c','Marina'), ('MARINA','#2ca02c','Marina')]:
    if col in ac.columns:
        b.plot(ac.index, ac[col], color=c, lw=2, marker='o', label=lab)
b.axvline(2018.5, ls=':', color='gray'); b.text(2018.6, 200, '2018', fontsize=8, color='gray')
b.set_title('Acuacultura: dulce (interior) vs marina'); b.legend(); b.grid(alpha=0.3)

# 3. especies captura (top 8)
c = axes[1,0]
sp = df[df['Origen']=='CAPTURA'].groupby('Especie')['PesoVivo'].sum().sort_values(ascending=False).head(8)/1e3
c.barh(sp.index[::-1], sp.values[::-1], color='#1f77b4')
c.set_title('Top 8 especies de captura (mil ton)'); c.grid(alpha=0.3, axis='x')

# 4. especies acuacultura (top 8)
d = axes[1,1]
sp = df[df['Origen']=='ACUACULTURA'].groupby('Especie')['PesoVivo'].sum().sort_values(ascending=False).head(8)/1e3
d.barh(sp.index[::-1], sp.values[::-1], color='#2ca02c')
d.set_title('Top 8 especies de acuacultura (mil ton)'); d.grid(alpha=0.3, axis='x')

plt.tight_layout(); plt.savefig('results/pesca_nacional.png', dpi=120); plt.close()

# ---- forecasts (separando tipos) ----
def forecast(serie, nombre, file):
    y = np.log(serie.values.astype(float))
    try:
        m = ARIMA(y, order=(0,1,0), trend='t').fit()
        fc = m.get_forecast(3)
        cent = np.exp(fc.predicted_mean); lo = np.exp(fc.conf_int(alpha=0.2)[:,0]); hi = np.exp(fc.conf_int(alpha=0.2)[:,1])
        print(f'\n=== FORECAST {nombre} (2025-2027, miles ton) ===')
        for i, yr in enumerate([2025,2026,2027]):
            print(f'  {yr}: {cent[i]/1e3:.0f} [{lo[i]/1e3:.0f}-{hi[i]/1e3:.0f}]')
        pd.DataFrame({'Anio':[2025,2026,2027],'central':cent,'ic80_lo':lo,'ic80_hi':hi}).to_csv(file, index=False, encoding='utf-8')
    except Exception as e:
        print(f'  {nombre}: forecast no disponible ({e})')

cap_tot = df[df['Origen']=='CAPTURA'].groupby('Anio')['PesoVivo'].sum()
acua_tot = df[df['Origen']=='ACUACULTURA'].groupby('Anio')['PesoVivo'].sum()
forecast(cap_tot, 'CAPTURA (estable)', 'data/forecast_captura_2025_2027.csv')
forecast(acua_tot, 'ACUACULTURA (post-2019)', 'data/forecast_acuacultura_2025_2027.csv')
