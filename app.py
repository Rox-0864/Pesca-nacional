import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Pesca y Acuacultura Nacional", page_icon="🐟", layout="wide")

@st.cache_data
def cargar():
    df = pd.read_csv("data/pesca_nacional_2014_2024.csv")
    fc = pd.read_csv("data/forecast_captura_2025_2027.csv")
    fa = pd.read_csv("data/forecast_acuacultura_2025_2027.csv")
    return df, fc, fa

df, fc, fa = cargar()
df["Origen"] = df["Origen"].str.strip().str.upper()
df["Tipogua"] = df["Tipogua"].str.strip().str.upper()

KT = 1e6  # kg -> miles de toneladas

st.title("🐟 Pesca y Acuacultura Nacional (México)")
st.caption("CONAPESCA 2014–2024 · separando captura vs acuacultura")

st.markdown("""
**Hallazgo central:** la producción pesquera nacional se compone de dos regímenes muy distintos.
La **captura marina** (~1.5 M ton) es estable; la **acuacultura** (~350 mil ton) muestra un
quiebre en 2018 que es **estadístico, no productivo**: CONAPESCA cedió los centros acuícolas
de aguas interiores a los estados y cambió la metodología reportada al INEGI.
""")

cap = df[df["Origen"]=="CAPTURA"].groupby("Anio")["PesoVivo"].sum()/KT
acua = df[df["Origen"]=="ACUACULTURA"].groupby("Anio")["PesoVivo"].sum()/KT

c1, c2, c3, c4 = st.columns(4)
c1.metric("Captura 2024", f"{cap.iloc[-1]:.2f} M ton")
c2.metric("Acuacultura 2024", f"{acua.iloc[-1]*1e3:.0f} mil ton")
c3.metric("Quiebre acuacultura dulce", "−54%")
c4.metric("Acuacultura marina (tendencia)", "↑ crece")

st.markdown("---")

# 1. Captura vs Acuacultura
st.header("1 · Captura vs Acuacultura")
fig = go.Figure()
fig.add_trace(go.Scatter(x=cap.index, y=cap.values, mode="lines+markers", name="Captura",
                         line=dict(color="#1f77b4", width=2.5)))
fig.add_trace(go.Scatter(x=acua.index, y=acua.values*1e3, mode="lines+markers", name="Acuacultura",
                         line=dict(color="#2ca02c", width=2.5), yaxis="y2"))
fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0),
                  yaxis_title="Captura (M ton)", yaxis2=dict(title="Acuacultura (mil ton)",
                  overlaying="y", side="right"),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 2. El quiebre: acuacultura dulce vs marina
st.header("2 · El quiebre de 2018 (acuacultura de aguas interiores)")
ac = df[df["Origen"]=="ACUACULTURA"].copy()
ac["tipo"] = ac["Tipogua"].apply(lambda t: "Dulce (interior)" if t=="DULCE" else "Marina")
g = ac.groupby(["Anio","tipo"])["PesoVivo"].sum().unstack()/1e3

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=g.index, y=g.get("Dulce (interior)", pd.Series(dtype=float)),
                          mode="lines+markers", name="Dulce (interior)",
                          line=dict(color="#d62728", width=2.5)))
fig2.add_trace(go.Scatter(x=g.index, y=g.get("Marina", pd.Series(dtype=float)),
                          mode="lines+markers", name="Marina",
                          line=dict(color="#2ca02c", width=2.5)))
fig2.add_vline(x=2018.5, line_dash="dot", line_color="gray",
               annotation_text="2018: cesión a estados", annotation_position="top left")
fig2.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="miles de toneladas",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig2, use_container_width=True)

st.info("**La caída del −54% es solo en acuacultura DULCE (interior)**, justo cuando CONAPESCA "
        "desapareció las oficinas de pesca en aguas interiores y cedió los centros acuícolas a los "
        "gobiernos estatales (2018). La captura y la acuacultura marina — que siguieron bajo reporte "
        "federal — no caen. Es un **cambio de metodología estadística**, no necesariamente un colapso "
        "real de la producción interior.")

st.markdown("---")

# 2b. Contraste por estado
st.header("2b · El contraste por estado (¿todos cayeron?)")
est_df = pd.read_csv("data/acuacultura_dulce_estado.csv").sort_values("cambio_pct")
colores = ["#2ca02c" if c > -15 else "#d62728" for c in est_df["cambio_pct"]]
fig_est = go.Figure(go.Bar(y=est_df["estado"], x=est_df["cambio_pct"], orientation="h",
                           marker_color=colores))
fig_est.add_vline(x=0, line_color="gray", line_width=1)
fig_est.add_vline(x=-15, line_color="gray", line_width=1, line_dash="dot")
fig_est.update_layout(height=640, margin=dict(l=0, r=0, t=10, b=0),
                      xaxis_title="Cambio % (2014-18 → 2019-24)")
st.plotly_chart(fig_est, use_container_width=True)
st.success("**5 estados NO cayeron** (verde): Yucatán +132%, Baja California +101%, Quintana Roo +32%, "
           "Baja California Sur −1%, Nayarit −8%. Son estados **costeros con agencias acuícolas propias** "
           "que siguieron reportando sin hueco. El resto (−24% a −99%, en rojo) son mayormente estados "
           "**sin litoral**, cuya acuacultura interior quedó huérfana de reporte federal en 2018. "
           "Un colapso real sería uniforme; este contraste es la firma de un **cambio de cobertura "
           "estadística**, no de producción.")

st.markdown("---")

# 3. Top especies y estados
st.header("3 · Especies y estados")
colA, colB = st.columns(2)
with colA:
    st.subheader("Top 8 especies — captura")
    sp = df[df["Origen"]=="CAPTURA"].groupby("Especie")["PesoVivo"].sum().sort_values().tail(8)/1e3
    fig = go.Figure(go.Bar(x=sp.values, y=sp.index, orientation="h", marker_color="#1f77b4"))
    fig.update_layout(height=330, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="mil ton")
    st.plotly_chart(fig, use_container_width=True)
with colB:
    st.subheader("Top 8 especies — acuacultura")
    sp = df[df["Origen"]=="ACUACULTURA"].groupby("Especie")["PesoVivo"].sum().sort_values().tail(8)/1e3
    fig = go.Figure(go.Bar(x=sp.values, y=sp.index, orientation="h", marker_color="#2ca02c"))
    fig.update_layout(height=330, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="mil ton")
    st.plotly_chart(fig, use_container_width=True)

colC, colD = st.columns(2)
with colC:
    st.subheader("Top 8 estados — captura")
    s = df[df["Origen"]=="CAPTURA"].groupby("Estado")["PesoVivo"].sum().sort_values().tail(8)/1e3
    fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color="#1f77b4"))
    fig.update_layout(height=330, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="mil ton")
    st.plotly_chart(fig, use_container_width=True)
with colD:
    st.subheader("Top 8 estados — acuacultura")
    s = df[df["Origen"]=="ACUACULTURA"].groupby("Estado")["PesoVivo"].sum().sort_values().tail(8)/1e3
    fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color="#2ca02c"))
    fig.update_layout(height=330, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="mil ton")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. Forecast
st.header("4 · Forecast 2025-2027 (separado por tipo)")
colE, colF = st.columns(2)
with colE:
    st.subheader("Captura (M ton)")
    f = go.Figure()
    f.add_trace(go.Scatter(x=cap.index, y=cap.values, mode="lines", name="Histórico",
                           line=dict(color="#1f77b4", width=2)))
    f.add_trace(go.Scatter(x=fc["Anio"], y=fc["central"]/KT, mode="lines+markers", name="Forecast",
                           line=dict(color="#d62728", width=2, dash="dash")))
    f.add_trace(go.Scatter(x=fc["Anio"], y=fc["ic80_hi"]/KT, mode="lines", line=dict(width=0), showlegend=False))
    f.add_trace(go.Scatter(x=fc["Anio"], y=fc["ic80_lo"]/KT, mode="lines", line=dict(width=0),
                           fill="tonexty", fillcolor="rgba(214,39,40,0.15)", name="IC 80%"))
    f.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(f, use_container_width=True)
with colF:
    st.subheader("Acuacultura (mil ton)")
    f = go.Figure()
    f.add_trace(go.Scatter(x=acua.index, y=acua.values*1e3, mode="lines", name="Histórico",
                           line=dict(color="#2ca02c", width=2)))
    f.add_trace(go.Scatter(x=fa["Anio"], y=fa["central"]/1e3, mode="lines+markers", name="Forecast",
                           line=dict(color="#d62728", width=2, dash="dash")))
    f.add_trace(go.Scatter(x=fa["Anio"], y=fa["ic80_hi"]/1e3, mode="lines", line=dict(width=0), showlegend=False))
    f.add_trace(go.Scatter(x=fa["Anio"], y=fa["ic80_lo"]/1e3, mode="lines", line=dict(width=0),
                           fill="tonexty", fillcolor="rgba(214,39,40,0.15)", name="IC 80%"))
    f.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(f, use_container_width=True)

st.caption("Captura: ~1.9–2.0 M ton. Acuacultura: ~352–358 mil ton (nivel post-2019). "
           "Reproducible: `scripts/analisis.py` · datos en `data/pesca_nacional_2014_2024.csv`.")
