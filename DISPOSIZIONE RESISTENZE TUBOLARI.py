import streamlit as st
import math

# Impostazione layout della pagina web
st.set_page_config(layout="wide", page_title="Ottimizzatore Asole/Resistenze")

st.title("🔄 Ottimizzatore Grafico Disposizione Resistenze / Asole (Profilo Reale)")
st.write("Calcolo geometrico con algoritmo a capsula per il nesting preciso delle estremità arrotondate.")

# -------------------------------------------------------------------------
# BARRA LATERALE: CONTROLLI E INPUT
# -------------------------------------------------------------------------
st.sidebar.header("📐 Parametri di Configurazione")

st.sidebar.subheader("Dimensioni Foglio (mm)")
foglio_w = st.sidebar.number_input("Larghezza Foglio (X)", min_value=100.0, max_value=5000.0, value=611.0, step=1.0)
foglio_h = st.sidebar.number_input("Altezza Foglio (Y)", min_value=100.0, max_value=5000.0, value=240.0, step=1.0)

st.sidebar.subheader("Dimensioni Asola/Resistenza (mm)")
asola_l = st.sidebar.number_input("Lunghezza Oggetto (L)", min_value=10.0, max_value=2000.0, value=100.0, step=1.0)
asola_w = st.sidebar.number_input("Larghezza/Diametro (W)", min_value=2.0, max_value=500.0, value=35.0, step=1.0)

st.sidebar.subheader("Parametri di Taglio / Tolleranze")
gap_inter_asola = st.sidebar.number_input("Distanza Minima tra Asole (Gap)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
margine_bordo = st.sidebar.number_input("Margine dal Bordo Foglio", min_value=0.0, max_value=200.0, value=10.0, step=1.0)

st.sidebar.subheader("Orientamento")
angolo_gradi = st.sidebar.slider("Inclinazione Asole (Gradi)", min_value=0, max_value=180, value=90, step=1)

# -------------------------------------------------------------------------
# LOGICA DI CALCOLO GEOMETRICO REALE (ALGORITMO A CAPSULA)
# -------------------------------------------------------------------------
rad = math.radians(angolo_gradi)

# Un'asola è formata da un segmento centrale dritto e due semicerchi alle estremità.
# Lunghezza della parte dritta tra i centri dei raccordi:
lunghezza_dritta = max(0.0, asola_l - asola_w)
raggio = asola_w / 2.0

# Calcolo dell'ingombro reale proiettato della capsula (Non del rettangolo!)
# La proiezione dei semicerchi è sempre pari al diametro (asola_w) in qualsiasi angolo.
ingombro_x = abs(lunghezza_dritta * math.cos(rad)) + asola_w
ingombro_y = abs(lunghezza_dritta * math.sin(rad)) + asola_w

# Il passo tra le file/colonne parallele
passo_x = ingombro_x + gap_inter_asola
passo_y = ingombro_y + gap_inter_asola

# Spazio utile interno dedotto il margine perimetrale
spazio_utile_w = foglio_w - (2 * margine_bordo)
spazio_utile_h = foglio_h - (2 * margine_bordo)

if spazio_utile_w >= ingombro_x and spazio_utile_h >= ingombro_y:
    colonne = math.floor((spazio_utile_w - ingombro_x) / passo_x) + 1
    righe = math.floor((spazio_utile_h - ingombro_y) / passo_y) + 1
    totale_asole = colonne * righe
else:
    colonne, righe, totale_asole = 0, 0, 0

# -------------------------------------------------------------------------
# PANNELLO CENTRALE: RISULTATI E GRAFICA
# -------------------------------------------------------------------------
col_ris1, col_ris2 = st.columns(2)
with col_ris1:
    st.metric(label="Totale Asole Inseribili", value=f"{totale_asole} pz")
with col_ris2:
    st.metric(label="Configurazione Griglia", value=f"{colonne} Colonne x {righe} Righe")

st.subheader("🎨 Anteprima Visiva del Layout")

# Scala dinamica per la visualizzazione a schermo
scala = min(700 / foglio_w, 400 / foglio_h)
canvas_w = foglio_w * scala
canvas_h = foglio_h * scala

svg_code = f"""
<svg width="{canvas_w + 40}" height="{canvas_h + 40}" xmlns="http://www.w3.org/2000/svg" style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 20px;">
    <rect x="0" y="0" width="{foglio_w * scala}" height="{foglio_h * scala}" fill="#b8860b" opacity="0.8" rx="5"/>
    
    <rect x="{margine_bordo * scala}" y="{margine_bordo * scala}" 
          width="{spazio_utile_w * scala}" height="{spazio_utile_h * scala}" 
          fill="none" stroke="#ffffff" stroke-dasharray="4" stroke-width="1" opacity="0.5"/>
"""

if totale_asole > 0:
    start_x = margine_bordo + (ingombro_x / 2)
    start_y = margine_bordo + (ingombro_y / 2)
    
    for r in range(righe):
        for c in range(colonne):
            cx = (start_x + c * passo_x) * scala
            cy = (start_y + r * passo_y) * scala
            
            svg_code += f"""
            <g transform="translate({cx},{cy}) rotate({angolo_gradi})">
                <rect x="-{(asola_l/2)*scala}" y="-{(asola_w/2)*scala}" 
                      width="{asola_l*scala}" height="{asola_w*scala}" 
                      fill="#ff4b4b" rx="{raggio*scala}" stroke="#990000" stroke-width="1"/>
            </g>
            """

svg_code += "</svg>"

st.components.v1.html(svg_code, width=canvas_w + 50, height=canvas_h + 50)

st.info("💡 L'algoritmo ora calcola l'ingombro reale della testa sferica (capsula). Muovendo lo slider attorno a 90° noterai che la seconda riga non scompare più istantaneamente.")