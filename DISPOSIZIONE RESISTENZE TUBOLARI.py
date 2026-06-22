import streamlit as st
import math

# Impostazione layout
st.set_page_config(layout="wide", page_title="Ottimizzatore Asole/Resistenze")

# -------------------------------------------------------------------------
# DIZIONARIO LINGUE (ITALIANO / INGLESE)
# -------------------------------------------------------------------------
lang_dict = {
    "IT": {
        "title": "🔄 Ottimizzatore Grafico Disposizione Resistenze / Asole",
        "subtitle": "Confronto real-time tra il vecchio metodo Bounding Box e la nuova Capsula Reale.",
        "sidebar_lang": "🌍 Lingua / Language",
        "sidebar_params": "📐 Parametri Lamiera",
        "algo_label": "Metodo di Calcolo",
        "algo_old": "Vecchio (Proiezione)",
        "algo_new": "Nuovo (Capsula Reale)",
        "layout_label": "Tipologia di Griglia",
        "layout_reg": "Lineare Standard",
        "layout_stag": "Sfalsata (Nido d'Ape)",
        "sheet_w": "Larghezza Foglio (X)",
        "sheet_h": "Altezza Foglio (Y)",
        "slot_l": "Lunghezza Asola (L)",
        "slot_w": "Diametro Asola (W)",
        "gap": "Gap Minimo (mm)",
        "margin": "Margine Bordo (mm)",
        "angle": "Angolo Inclinazione (Gradi)",
        "metrics_tot": "Asole Inserite",
        "metrics_eff": "Sfruttamento Lamiera",
        "metrics_px": "Passo X Effettivo",
        "metrics_py": "Passo Y Effettivo",
        "area_info": "Stima Area di Taglio",
        "area_desc": "L'area utile di metallo per singola asola calcolata è pari a circa",
        "warn_no_slots": "⚠️ Nessun elemento inseribile con questi parametri. Riduci il diametro, le dimensioni o il gap.",
        "footer_title_1": "📐 Perché il vecchio metodo falliva?",
        "footer_desc_1": "Il metodo Bounding Box proiettava la capsula come un rettangolo solido sugli assi. A 45°, questo creava una cornice vuota fittizia, forzando un passo X e Y sproporzionato rispetto al Gap reale.",
        "footer_title_2": "⚡ Come funziona l'algoritmo a Capsula?",
        "footer_desc_2": "Considera l'asola nel suo profilo geometrico reale. Calcolando la minima distanza tra i segmenti centrali nel piano reale, consente alle asole di avvicinarsi sulla diagonale.",
        "footer_title_3": "🐝 Griglia Sfalsata (A nido d'ape)",
        "footer_desc_3": "Slitta le righe adiacenti di mezza colonna. Questo permette alla testa sferica superiore di scivolare nella 'gola' creata dalle asole sottostanti, massimizzando la densità."
    },
    "EN": {
        "title": "🔄 Slot / Tubular Heater Layout Optimizer",
        "subtitle": "Real-time comparison between Bounding Box method and Real Capsule algorithm.",
        "sidebar_lang": "🌍 Lingua / Language",
        "sidebar_params": "📐 Sheet Parameters",
        "algo_label": "Calculation Method",
        "algo_old": "Old (Bounding Box)",
        "algo_new": "New (Real Capsule)",
        "layout_label": "Grid Type",
        "layout_reg": "Standard Linear",
        "layout_stag": "Staggered (Honeycomb)",
        "sheet_w": "Sheet Width (X)",
        "sheet_h": "Sheet Height (Y)",
        "slot_l": "Slot Length (L)",
        "slot_w": "Slot Diameter (W)",
        "gap": "Minimum Gap (mm)",
        "margin": "Edge Margin (mm)",
        "angle": "Tilt Angle (Degrees)",
        "metrics_tot": "Inserted Slots",
        "metrics_eff": "Sheet Efficiency",
        "metrics_px": "Actual X Pitch",
        "metrics_py": "Actual Y Pitch",
        "area_info": "Cutting Area Estimation",
        "area_desc": "The useful metal area for a single calculated slot is approximately",
        "warn_no_slots": "⚠️ No items fit with these parameters. Reduce diameter, dimensions, or gap.",
        "footer_title_1": "📐 Why did the old method fail?",
        "footer_desc_1": "The Bounding Box method projected the capsule as a solid rectangle on the axes. At 45°, this created a fictitious empty frame, forcing an oversized X and Y pitch.",
        "footer_title_2": "⚡ How does the Capsule algorithm work?",
        "footer_desc_2": "It considers the slot in its real geometric profile. By calculating the minimum distance between central segments, it allows the slots to get closer on the diagonal.",
        "footer_title_3": "🐝 Staggered Grid (Honeycomb)",
        "footer_desc_3": "Shifts adjacent rows by half a column. This allows the upper spherical head to slide into the 'groove' created by the underlying slots, maximizing density."
    }
}

# -------------------------------------------------------------------------
# UI: BARRA LATERALE E LINGUA
# -------------------------------------------------------------------------
lang_choice = st.sidebar.radio("🌍 Lingua / Language", ["Italiano (IT)", "English (EN)"])
lang_code = "IT" if "IT" in lang_choice else "EN"
t = lang_dict[lang_code]

st.title(t["title"])
st.write(t["subtitle"])

st.sidebar.header(t["sidebar_params"])

# Metodo e Layout impostati come bottoni visibili
algo_choice = st.sidebar.radio(t["algo_label"], [t["algo_old"], t["algo_new"]])
algo_mode = 'boundingbox' if algo_choice == t["algo_old"] else 'capsule'

layout_mode = 'regular'
if algo_mode == 'capsule':
    layout_choice = st.sidebar.radio(t["layout_label"], [t["layout_reg"], t["layout_stag"]])
    layout_mode = 'regular' if layout_choice == t["layout_reg"] else 'staggered'

st.sidebar.markdown("---")

# Parametri dimensionali
foglio_w = st.sidebar.number_input(t["sheet_w"], min_value=100.0, max_value=5000.0, value=611.0, step=1.0)
foglio_h = st.sidebar.number_input(t["sheet_h"], min_value=50.0, max_value=5000.0, value=240.0, step=1.0)

asola_l = st.sidebar.number_input(t["slot_l"], min_value=10.0, max_value=2000.0, value=100.0, step=1.0)
asola_w = st.sidebar.number_input(t["slot_w"], min_value=2.0, max_value=500.0, value=35.0, step=1.0)

gap = st.sidebar.number_input(t["gap"], min_value=0.0, max_value=100.0, value=20.0, step=0.5)
margine_bordo = st.sidebar.number_input(t["margin"], min_value=0.0, max_value=200.0, value=10.0, step=1.0)

angolo_gradi = st.sidebar.slider(t["angle"], min_value=0, max_value=180, value=45, step=1)

# -------------------------------------------------------------------------
# FUNZIONI GEOMETRICHE (DISTANZA REALE TRA CAPSULE)
# -------------------------------------------------------------------------
def get_capsule_distance(dx, dy, L, W, theta):
    L_d = max(0, L - W)
    rad = math.radians(theta)
    cos_t = math.cos(rad)
    sin_t = math.sin(rad)

    d_parallel = dx * cos_t + dy * sin_t
    d_perp = -dx * sin_t + dy * cos_t

    clamp_val = max(-L_d, min(L_d, d_parallel))
    dist_sq = (d_parallel - clamp_val)**2 + d_perp**2
    dist_segment = math.sqrt(dist_sq)

    return dist_segment - W

# -------------------------------------------------------------------------
# CALCOLO ALGORITMO E DISPOSIZIONE
# -------------------------------------------------------------------------
rad = math.radians(angolo_gradi)
L_d = max(0, asola_l - asola_w)

ingombro_x = abs(L_d * math.cos(rad)) + asola_w
ingombro_y = abs(L_d * math.sin(rad)) + asola_w

spazio_utile_w = foglio_w - (2 * margine_bordo)
spazio_utile_h = foglio_h - (2 * margine_bordo)

Px = asola_w + gap
Py = asola_w + gap

if algo_mode == 'boundingbox':
    Px = ingombro_x + gap
    Py = ingombro_y + gap
else:
    # Calcolo Passo X
    temp_px = asola_w + gap
    while temp_px < asola_l + asola_w + gap + 300:
        if get_capsule_distance(temp_px, 0, asola_l, asola_w, angolo_gradi) >= gap:
            Px = temp_px
            break
        temp_px += 0.2

    # Calcolo Passo Y
    temp_py = asola_w + gap
    while temp_py < asola_l + asola_w + gap + 300:
        if get_capsule_distance(0, temp_py, asola_l, asola_w, angolo_gradi) >= gap:
            Py = temp_py
            break
        temp_py += 0.2

    if layout_mode == 'staggered':
        temp_py_stag = asola_w + gap
        while temp_py_stag < asola_l + asola_w + gap + 300:
            dist1 = get_capsule_distance(0.5 * Px, temp_py_stag, asola_l, asola_w, angolo_gradi)
            dist2 = get_capsule_distance(-0.5 * Px, temp_py_stag, asola_l, asola_w, angolo_gradi)
            if dist1 >= gap and dist2 >= gap:
                Py = temp_py_stag
                break
            temp_py_stag += 0.2
    else:
        while Py < asola_l + asola_w + gap + 300:
            dist1 = get_capsule_distance(Px, Py, asola_l, asola_w, angolo_gradi)
            dist2 = get_capsule_distance(Px, -Py, asola_l, asola_w, angolo_gradi)
            if dist1 >= gap and dist2 >= gap:
                break
            Py += 0.2

# Generazione posizioni
slots = []
if spazio_utile_w >= ingombro_x and spazio_utile_h >= ingombro_y:
    max_cols = math.ceil(spazio_utile_w / Px) + 2
    max_rows = math.ceil(spazio_utile_h / Py) + 2

    start_x = margine_bordo + (ingombro_x / 2)
    start_y = margine_bordo + (ingombro_y / 2)

    for r in range(max_rows):
        for c in range(max_cols):
            cx = start_x + c * Px
            cy = start_y + r * Py

            if layout_mode == 'staggered' and algo_mode == 'capsule':
                cx += (r % 2) * 0.5 * Px

            minX_slot = cx - (ingombro_x / 2)
            maxX_slot = cx + (ingombro_x / 2)
            minY_slot = cy - (ingombro_y / 2)
            maxY_slot = cy + (ingombro_y / 2)

            if (minX_slot >= margine_bordo - 0.01 and 
                maxX_slot <= foglio_w - margine_bordo + 0.01 and 
                minY_slot >= margine_bordo - 0.01 and 
                maxY_slot <= foglio_h - margine_bordo + 0.01):
                slots.append({'cx': cx, 'cy': cy})

# Statistiche
area_singola = (asola_l - asola_w) * asola_w + math.pi * math.pow(asola_w / 2, 2)
efficienza = ((len(slots) * area_singola) / (foglio_w * foglio_h)) * 100 if foglio_w * foglio_h > 0 else 0

st.sidebar.info(f"**{t['area_info']}**\n\n{t['area_desc']} **{area_singola:.1f} mm²**.")

# -------------------------------------------------------------------------
# RISULTATI E GRAFICA (RENDERING SVG)
# -------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["metrics_tot"], f"{len(slots)} pz")
col2.metric(t["metrics_eff"], f"{efficienza:.1f} %")
col3.metric(t["metrics_px"], f"{Px:.2f} mm")
col4.metric(t["metrics_py"], f"{Py:.2f} mm")

if len(slots) == 0:
    st.warning(t["warn_no_slots"])
else:
    scala = min(800 / foglio_w, 400 / foglio_h)
    canvas_w = foglio_w * scala
    canvas_h = foglio_h * scala

    svg_code = f"""
    <svg width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" style="background-color: #1e293b; border-radius: 8px; margin-top: 20px;">
        <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="#b8860b" opacity="0.6" rx="5"/>
        
        <rect x="{margine_bordo * scala}" y="{margine_bordo * scala}" 
              width="{(foglio_w - 2 * margine_bordo) * scala}" height="{(foglio_h - 2 * margine_bordo) * scala}" 
              fill="none" stroke="#ffffff" stroke-dasharray="4" stroke-width="1.5" opacity="0.5"/>
    """

    for s in slots:
        cx_scaled = s['cx'] * scala
        # Invertiamo l'asse Y per far combaciare l'origine col disegno industriale (basso-sinistra)
        cy_scaled = (foglio_h - s['cy']) * scala
        
        svg_code += f"""
        <g transform="translate({cx_scaled},{cy_scaled}) rotate({-angolo_gradi})">
            <rect x="{-(asola_l/2)*scala}" y="{-(asola_w/2)*scala}" 
                  width="{asola_l*scala}" height="{asola_w*scala}" 
                  fill="#ef4444" rx="{(asola_w/2)*scala}" stroke="#991b1b" stroke-width="1.5" opacity="0.9"/>
            <line x1="{-(asola_l/2 - asola_w/2)*scala}" y1="0" x2="{(asola_l/2 - asola_w/2)*scala}" y2="0" 
                  stroke="#ffffff" stroke-width="1" stroke-dasharray="2" opacity="0.6"/>
        </g>
        """
    svg_code += "</svg>"
    st.components.v1.html(svg_code, width=int(canvas_w) + 20, height=int(canvas_h) + 20)

# -------------------------------------------------------------------------
# SPIEGAZIONI A PIE DI PAGINA
# -------------------------------------------------------------------------
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"#### {t['footer_title_1']}")
    st.caption(t['footer_desc_1'])
with c2:
    st.markdown(f"#### {t['footer_title_2']}")
    st.caption(t['footer_desc_2'])
with c3:
    st.markdown(f"#### {t['footer_title_3']}")
    st.caption(t['footer_desc_3'])
