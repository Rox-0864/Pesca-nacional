# Informe — Pesca y Acuacultura Nacional (México)

> Análisis de la producción pesquera y acuícola **nacional**, separando **captura**
> de **acuacultura**, con foco en el quiebre estadístico de 2018.

---

## 1. Resumen

| Fuente | Cobertura | Registros |
|---|---|---|
| CONAPESCA (Anuario, base de datos de producción) | 2014–2024 (10 años) | 117,898 |

Producción nacional (peso vivo):

- **Captura** (pesca de captura, marina): **~1.5–1.8 M ton/año**, estable.
- **Acuacultura** (cultivo): **~350 mil ton/año**, con un quiebre en 2018.

---

## 2. El hallazgo central: el quiebre de 2018 es estadístico, no productivo

Separando la acuacultura por tipo de agua:

| Serie | 2014–2018 | 2019–2024 | Cambio |
|---|---|---|---|
| Captura (marina) | 1.52 M ton | 1.74 M ton | estable |
| Acuacultura **marina** | 178 mil ton | 230 mil ton | **+29%** |
| Acuacultura **dulce (interior)** | 197 mil ton | 91 mil ton | **−54%** |

La caída se concentra **exclusivamente en la acuacultura de aguas interiores
(dulce)**, exactamente cuando (2018) CONAPESCA desapareció las oficinas de pesca
en aguas interiores y cedió los centros acuícolas — administrados antes por el
gobierno federal — a los gobiernos estatales, cambiando la metodología reportada
al INEGI.

La captura y la acuacultura marina, que siguieron bajo el registro federal, no
caen (la marina incluso crece). Por lo tanto, la "caída" de la acuacultura
interior es en gran parte un **artefacto de cambio metodológico**, no
necesariamente un colapso real de la producción.

> Esta es la misma lección que el maguey pulquero en Tlaxcala: un cambio de
> registro puede verse como un "quiebre estructural" si no se distingue el dato
> de la producción.

### El contraste por estado confirma el cambio de cobertura

Separando la acuacultura dulce por entidad, el "colapso" **no es uniforme**:

- **5 estados NO cayeron** (incluso crecieron): Yucatán **+132%**, Baja California
  **+101%**, Quintana Roo **+32%**, Baja California Sur **−1%**, Nayarit **−8%**.
  Son estados **costeros con agencias acuícolas propias** que siguieron reportando.
- **El resto cayó −24% a −99%**: México −99%, San Luis Potosí −97%, Guanajuato −94%,
  Puebla −89%, Zacatecas −88%, Tlaxcala −84%, Michoacán −75%, Jalisco −72%… en su
  mayoría estados **sin litoral**, cuya acuacultura interior quedó sin reporte
  federal en 2018.

Un colapso real de producción sería homogéneo entre estados; este contraste tan
marcado es la firma de un **cambio de cobertura estadística**, no de una caída
productiva.

---

## 3. Especies y estados

**Top especies (total 2014–2024):**

- Captura: sardina (6.1 M ton), anchoveta, otras, atún, macarela, jaiba, camarón.
- Acuacultura: mojarra/tilapia (1.0 M ton), camarón (1.6 M ton sumando acentos),
  ostión, carpa, trucha.

**Top estados:**

- Captura: Sonora, Sinaloa, Baja California, Baja California Sur (litoral Pacífico).
- Acuacultura: Sinaloa, Sonora, Veracruz, **Chiapas**, Jalisco, Nayarit, Tabasco.

---

## 4. Forecast 2025–2027 (separado)

- **Captura**: ~1.90 → 2.01 M ton (tendencia estable, ligeramente creciente).
- **Acuacultura**: ~352 → 358 mil ton (nivel post-2019).

Ambos con la advertencia de que la serie acuícola interior está distorsionada por
el cambio metodológico de 2018.

---

## 5. Reproducir

```bash
python scripts/analisis.py      # quiebre + gráficos + forecasts
streamlit run app.py            # dashboard
```

Datos en `data/pesca_nacional_2014_2024.csv`; gráficos en `results/`.
