import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('data/pesca_nacional_2014_2024.csv')
df['Origen'] = df['Origen'].str.strip().str.upper()
df['Tipogua'] = df['Tipogua'].str.strip().str.upper()

dulce = df[(df['Origen']=='ACUACULTURA') & (df['Tipogua']=='DULCE')]
g = dulce.groupby(['Estado','Anio'])['PesoVivo'].sum().unstack()
pre = g[[c for c in g.columns if c<=2018]].mean(axis=1)
post = g[[c for c in g.columns if c>=2019]].mean(axis=1)
cambio = (post - pre) / pre * 100

res = pd.DataFrame({'estado': g.index, 'pre_ton': pre.values, 'post_ton': post.values, 'cambio_pct': cambio.values})
res = res[res['pre_ton'] > 1000]  # producción interior significativa
res = res.sort_values('cambio_pct')
res.to_csv('data/acuacultura_dulce_estado.csv', index=False, encoding='utf-8')

# gráfico: barras horizontales, verdes los que no caen (cambio > -15%)
fig, ax = plt.subplots(figsize=(8, 9))
colores = ['#2ca02c' if c > -15 else '#d62728' for c in res['cambio_pct']]
ax.barh(res['estado'], res['cambio_pct'], color=colores)
ax.axvline(0, color='gray', lw=1)
ax.axvline(-15, color='gray', ls=':', lw=1)
ax.set_xlabel('Cambio % (2014-18 → 2019-24)')
ax.set_title('Acuacultura dulce (aguas interiores) por estado\nverde = no cae · rojo = quiebre')
ax.grid(alpha=0.3, axis='x')
plt.tight_layout(); plt.savefig('results/acuacultura_dulce_estado.png', dpi=120); plt.close()

print('Estados que NO caen (cambio > -15%):')
for _, r in res.iterrows():
    if r['cambio_pct'] > -15:
        print(f"  {r['estado']:22s} {r['cambio_pct']:+.0f}%")
print(f'\nTotal estados con producción interior significativa: {len(res)}')
print('Guardado: data/acuacultura_dulce_estado.csv + results/acuacultura_dulce_estado.png')
