import streamlit as st
import streamlit.components.v1 as components
import math

# Impostazione layout
st.set_page_config(layout="wide", page_title="Ottimizzatore Asole/Resistenze")

# -------------------------------------------------------------------------
# DIZIONARIO LINGUE
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

# Metodo e Layout
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
# FUNZIONI GEOMETRICHE
# -------------------------------------------------------------------------
def get_capsule_distance(dx, dy, L, W, theta):
    """Calcola distanza minima tra asole con geometria a capsula"""
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

def find_optimal_pitch(axis, L, W, angle, gap, max_search=1000):
    """Trova il passo ottimale con ricerca robusta"""
    min_pitch = W + gap
    max_pitch = max(L + W + gap + 100, max_search)
    current = min_pitch
    step = 0.1
    found = False
    
    while current < max_pitch:
        if axis == 'X':
            dist = get_capsule_distance(current, 0, L, W, angle)
        elif axis == 'Y':
            dist = get_capsule_distance(0, current, L, W, angle)
        else:
            dist = -1
        
        if dist >= gap - 0.01: 
            found = True
            return current
        current += step
    
    if not found:
        st.warning(f"⚠️ Attenzione: Passo {axis} non ottimizzabile con questi parametri")
        return max_pitch
    return current

# -------------------------------------------------------------------------
# CALCOLO ALGORITMO
# -------------------------------------------------------------------------
rad = math.radians(angolo_gradi)
L_d = max(0, asola_l - asola_w)

ingombro_x = L_d * abs(math.cos(rad)) + asola_w
ingombro_y = L_d * abs(math.sin(rad)) + asola_w

spazio_utile_w = foglio_w - (2 * margine_bordo)
spazio_utile_h = foglio_h - (2 * margine_bordo)

Px = asola_w + gap
Py = asola_w + gap

if algo_mode == 'boundingbox':
    Px = ingombro_x + gap
    Py = ingombro_y + gap
else:
    Px = find_optimal_pitch('X', asola_l, asola_w, angolo_gradi, gap)
    
    if layout_mode == 'staggered':
        Py = asola_w + gap
        max_search = asola_l + asola_w + gap + 100
        found_stag = False
        
        while Py < max_search:
            dist1 = get_capsule_distance(0.5 * Px, Py, asola_l, asola_w, angolo_gradi)
            dist2 = get_capsule_distance(-0.5 * Px, Py, asola_l, asola_w, angolo_gradi)
            
            if dist1 >= gap - 0.01 and dist2 >= gap - 0.01:
                found_stag = True
                break
            Py += 0.1
        
        if not found_stag:
            Py = find_optimal_pitch('Y', asola_l, asola_w, angolo_gradi, gap)
    else:
        Py = find_optimal_pitch('Y', asola_l, asola_w, angolo_gradi, gap)
        
        max_search = asola_l + asola_w + gap + 100
        while Py < max_search:
            dist_diag_x = get_capsule_distance(Px, Py, asola_l, asola_w, angolo_gradi)
            dist_diag_y = get_capsule_distance(Px, -Py, asola_l, asola_w, angolo_gradi)
            
            if dist_diag_x >= gap - 0.01 and dist_diag_y >= gap - 0.01:
                break
            Py += 0.1

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
# RISULTATI E RENDERING
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
        cy_scaled = (foglio_h - s['cy']) * scala
        
        # 1. DISEGNO DEI PROFILI DI CALCOLO (AREA DI RISPETTO)
        if algo_mode == 'boundingbox':
            # Profilo dell'ingombro effettivo (Rettangolo Giallo)
            w_box = ingombro_x * scala
            h_box = ingombro_y * scala
            svg_code += f"""
            <rect x="{cx_scaled - w_box/2}" y="{cy_scaled - h_box/2}" 
                  width="{w_box}" height="{h_box}" 
                  fill="none" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4" opacity="0.8"/>
            """
            
            # Profilo di ingombro sommato al GAP (le asole adiacenti si toccano qui)
            w_gap = (ingombro_x + gap) * scala
            h_gap = (ingombro_y + gap) * scala
            svg_code += f"""
            <rect x="{cx_scaled - w_gap/2}" y="{cy_scaled - h_gap/2}" 
                  width="{w_gap}" height="{h_gap}" 
                  fill="none" stroke="#fbbf24" stroke-width="1" stroke-dasharray="2" opacity="0.3"/>
            """

        svg_code += f"""
        <g transform="translate({cx_scaled},{cy_scaled}) rotate({-angolo_gradi})">
        """
        
        if algo_mode == 'capsule':
            # Profilo della Capsula sommato al GAP (Capsula Verde)
            # Viene espansa di 'gap' totali (gap/2 per lato) così le aree di rispetto si toccano
            l_gap = (asola_l + gap) * scala
            w_gap = (asola_w + gap) * scala
            r_gap = w_gap / 2
            svg_code += f"""
            <rect x="{-l_gap/2}" y="{-w_gap/2}" 
                  width="{l_gap}" height="{w_gap}" 
                  fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.8" rx="{r_gap}"/>
            """

        # 2. DISEGNO DELL'ASOLA FISICA
        svg_code += f"""
            <rect x="{-(asola_l/2)*scala}" y="{-(asola_w/2)*scala}" 
                  width="{asola_l*scala}" height="{asola_w*scala}" 
                  fill="#ef4444" rx="{(asola_w/2)*scala}" stroke="#991b1b" stroke-width="1.5" opacity="0.9"/>
            <line x1="{-(asola_l/2 - asola_w/2)*scala}" y1="0" x2="{(asola_l/2 - asola_w/2)*scala}" y2="0" 
                  stroke="#ffffff" stroke-width="1" stroke-dasharray="2" opacity="0.6"/>
        </g>
        """
    svg_code += "</svg>"
    
    # Render dell'HTML content
    components.html(svg_code, width=int(canvas_w) + 20, height=int(canvas_h) + 20)

# -------------------------------------------------------------------------
# FOOTER
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
