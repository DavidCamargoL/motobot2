
import re  
import json
import html
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import streamlit as st  
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

from services.groq_service import consultar_motobot


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="MotoBot Colombia",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

RUTA_IMAGEN = Path(__file__).parent / "assets" / "motobot_hero.png"


# ============================================================
# 2. ESTILOS VISUALES
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #081321;
    --panel: #101f32;
    --panel2: #172a40;
    --text: #f4f7fb;
    --muted: #aebdd0;
    --orange: #ff7847;
    --border: rgba(155,180,210,.22);
}

/* ------------------------------------------------
   FONDO GENERAL
------------------------------------------------ */

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #081321 !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 85% 0%,
            rgba(30,75,120,.20),
            transparent 35%
        ),
        #081321 !important;
}

[data-testid="stHeader"] {
    background: #081321 !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* ------------------------------------------------
   BARRA LATERAL
------------------------------------------------ */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101f32,
        #091321
    ) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: #edf3fa;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #b7c5d6 !important;
}

/* Texto descriptivo de la barra lateral */

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #c3d0df !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
}

/* Avisos de la barra lateral */

[data-testid="stSidebar"] [data-testid="stAlert"],
[data-testid="stSidebar"] [data-testid="stAlert"] > div {
    background: #142a40 !important;
    border: 1px solid #294966 !important;
    border-radius: 14px !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] p,
[data-testid="stSidebar"] [data-testid="stAlert"] div {
    color: #e7f0fa !important;
}

/* ------------------------------------------------
   IMAGEN PRINCIPAL
------------------------------------------------ */

[data-testid="stImage"] img {
    border-radius: 16px;
}

.hero-caption {
    color: #aebdd0;
    font-size: .82rem;
    margin-top: .35rem;
}

/* ------------------------------------------------
   TEXTOS Y SECCIONES
------------------------------------------------ */

h1, h2, h3, h4, p, label {
    color: var(--text);
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #d8e2ed;
}

.section-kicker {
    color: #ff9a72 !important;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-top: 1.5rem;
    margin-bottom: .65rem;
}

.section-description {
    color: #aebdd0 !important;
    font-size: 1.08rem;
    margin-bottom: 1rem;
}

/* ------------------------------------------------
   BOTONES DE LA INTERFAZ
------------------------------------------------ */

div.stButton > button {
    width: 100%;
    min-height: 3.1rem;
    border-radius: 13px;
    border: 1px solid rgba(155,180,210,.28);
    background: #172a40;
    color: #f5f7fb !important;
    font-weight: 700;
    transition: all .18s ease;
}

/* Botones principales de funciones */

[data-testid="stHorizontalBlock"] [data-testid="column"] div.stButton > button {
    min-height: 3.7rem;
    font-size: 1.08rem;
}

div.stButton > button:hover {
    background: #213a55 !important;
    border-color: #ff895b !important;
    color: #ffffff !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(
        100deg,
        #e95e32,
        #ff895b
    ) !important;
    border-color: #ff9a72 !important;
    color: #ffffff !important;
}

/* ------------------------------------------------
   MENSAJES DEL CHAT
------------------------------------------------ */

[data-testid="stChatMessage"] {
    background: #101f32 !important;
    border: 1px solid var(--border) !important;
    border-radius: 17px !important;
    padding: .9rem 1rem !important;
    margin-bottom: .8rem;
}

/* Texto de las respuestas */

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h5,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h6,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] td,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] th {
    color: #f4f7fb !important;
}

/* Enlaces de las fuentes */

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] a {
    color: #ff9a72 !important;
    text-decoration: underline;
}

/* Tablas */

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] table {
    color: #f4f7fb !important;
    border-color: rgba(155,180,210,.30) !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] th,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] td {
    border-color: rgba(155,180,210,.30) !important;
}

/* Código dentro de las respuestas */

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    color: #ffd2bd !important;
    background: #172a40 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre {
    background: #091725 !important;
    border: 1px solid var(--border) !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre code {
    color: #f4f7fb !important;
    background: transparent !important;
}

/* ------------------------------------------------
   CAMPO DE PREGUNTA
------------------------------------------------ */

/* Contenedor inferior */

[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {
    background: #081321 !important;
}

/* Caja exterior */

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: #172a40 !important;
    border: 1px solid rgba(255,120,71,.70) !important;
    border-radius: 17px !important;
    box-shadow: 0 8px 25px rgba(0,0,0,.22) !important;
}

/* Contenedor interno */

[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"],
[data-testid="stChatInput"] div {
    background-color: transparent !important;
}

/* Texto escrito por el usuario */

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ff895b !important;
    opacity: 1 !important;
}

/* Texto de ejemplo */

[data-testid="stChatInput"] textarea::placeholder {
    color: #b9c7d7 !important;
    -webkit-text-fill-color: #b9c7d7 !important;
    opacity: 1 !important;
}

/* Botón de enviar */

[data-testid="stChatInput"] button {
    background: #ff7847 !important;
    color: #ffffff !important;
    border-radius: 50% !important;
}

/* Al enfocar el campo */

[data-testid="stChatInput"]:focus-within {
    border-color: #ff9a72 !important;
    box-shadow: 0 0 0 2px rgba(255,120,71,.18) !important;
}

/* ------------------------------------------------
   AVISOS Y MENSAJES GLOBALES
------------------------------------------------ */

/* Fondo azul para st.error, st.warning y st.info */

[data-testid="stAlert"],
[data-testid="stAlert"] > div,
[data-testid="stAlert"] [data-testid="stAlertContent"] {
    background: #142a40 !important;
    background-color: #142a40 !important;
    border: 1px solid #294966 !important;
    border-radius: 13px !important;
}

/* Texto de los avisos */

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #e7f0fa !important;
}

/* Iconos de los avisos */

[data-testid="stAlert"] svg {
    color: #ff9a72 !important;
}

/* ------------------------------------------------
   EXPANSORES Y OTROS COMPONENTES
------------------------------------------------ */

[data-testid="stExpander"] {
    background: #101f32 !important;
    border: 1px solid var(--border) !important;
    border-radius: 13px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #edf3fa !important;
}

hr {
    border-color: var(--border) !important;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. ESTADO DE LA APLICACIÓN
# ============================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "modo_consulta" not in st.session_state:  
    st.session_state.modo_consulta = "Libre"
if "resultado_comparacion" not in st.session_state:
    st.session_state.resultado_comparacion = None
for _clave in ("ficha_moto", "recomendaciones", "costo_resultado", "asesoria"):
    if _clave not in st.session_state:
        st.session_state[_clave] = None  


# ============================================================
# 4. FUNCIONES DE CONTROL DE LA CONVERSACIÓN
# ============================================================

def seleccionar_modo(modo):
    st.session_state.modo_consulta = modo


def quitar_modo():
    st.session_state.modo_consulta = "Libre"


def nueva_conversacion():  
    st.session_state.mensajes = []  
    st.session_state.modo_consulta = "Libre"
    st.session_state.resultado_comparacion = None  


# ============================================================
# 5. FUNCIONES DE RECUPERACIÓN Y VISUALIZACIÓN DE IMÁGENES
# ============================================================

@st.cache_data(ttl=3600, max_entries=64, show_spinner=False)
def obtener_imagen_de_pagina(url):

    try:
        respuesta = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; MotoBotColombia/1.0)"
            },
            timeout=8,
        )

        respuesta.raise_for_status()

        if "html" not in respuesta.headers.get(
            "Content-Type", ""
        ).lower():
            return None

        soup = BeautifulSoup(respuesta.text, "html.parser")

        titulo = ""

        etiqueta = soup.find(
            "meta",
            attrs={"property": "og:title"}
        )

        if etiqueta:
            titulo = etiqueta.get("content", "")

        if not titulo and soup.title:
            titulo = soup.title.get_text(" ", strip=True)

        imagen = None

        for selector in (
            {"property": "og:image"},
            {"name": "twitter:image"},
            {"property": "og:image:url"},
        ):

            etiqueta = soup.find("meta", attrs=selector)

            if etiqueta and etiqueta.get("content"):
                imagen = etiqueta["content"]
                break

        if not imagen:
            return None

        imagen = urljoin(respuesta.url, imagen)

        if urlparse(imagen).scheme not in ("http", "https"):
            return None

        verificacion = requests.get(
            imagen,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8,
            stream=True,
        )

        tipo = verificacion.headers.get("Content-Type", "").lower()
        verificacion.close()

        if not tipo.startswith("image/"):
            return None

        return {
            "url": imagen,
            "titulo": titulo or urlparse(url).netloc,
        }

    except requests.RequestException:
        return None

    except Exception:
        return None


def extraer_enlaces_de_fuentes(respuesta):

    coincidencia = re.search(
        r"(?:\*\*)?Fuentes consultadas(?:\*\*)?\s*([\s\S]*)$",
        respuesta,
        flags=re.IGNORECASE,
    )

    if not coincidencia:
        return []

    enlaces = re.findall(
        r"https?://[^\s)\]>]+",
        coincidencia.group(1),
    )

    resultado = []
    vistos = set()

    for enlace in enlaces:

        enlace = enlace.rstrip(".,;:!?\"'`)")

        if enlace.startswith("https://") and enlace not in vistos:
            vistos.add(enlace)
            resultado.append(enlace)

    return resultado


def tipo_de_consulta(pregunta):

    texto = pregunta.lower()

    patrones_masivos = (
        r"\btodas\b",
        r"\btodos\b",
        r"cat[aá]logo",
        r"inventario",
        r"listado",
        r"lista completa",
        r"hasta\s*\d+\s*cc",
        r"identifica (las )?motocicletas",
    )

    if any(re.search(p, texto) for p in patrones_masivos):
        return "masiva"

    patrones_comparacion = (
        r"compar",
        r"\bvs\b",
        r"versus",
        r"diferencias",
        r"cu[aá]l es mejor",
        r"cu[aá]l conviene",
        r"mejor moto",
        r"entre .+ y .+",
    )

    if any(re.search(p, texto) for p in patrones_comparacion):
        return "comparacion"

    patrones_individual = (
        r"ficha t[eé]cnica",
        r"caracter[ií]sticas",
        r"especificaciones",
        r"informaci[oó]n de",
        r"qu[eé] tal es",
        r"consumo de",
        r"precio de",
    )

    if any(re.search(p, texto) for p in patrones_individual):
        return "individual"

    return "ninguna"


def recuperar_imagenes(pregunta, respuesta):

    tipo = tipo_de_consulta(pregunta)

    if tipo not in ("individual", "comparacion"):
        return []

    enlaces = extraer_enlaces_de_fuentes(respuesta)

    if not enlaces:
        return []

    limite = 4 if tipo == "comparacion" else 1

    imagenes = []
    urls_vistas = set()

    for enlace in enlaces[:8]:

        dato = obtener_imagen_de_pagina(enlace)

        if not dato:
            continue

        if dato["url"] in urls_vistas:
            continue

        urls_vistas.add(dato["url"])
        imagenes.append(dato)

        if len(imagenes) >= limite:
            break

    return imagenes


def mostrar_imagenes(imagenes):

    if not imagenes:
        return

    st.markdown("#### Imágenes encontradas en las fuentes")

    columnas = st.columns(min(len(imagenes), 3))

    for indice, dato in enumerate(imagenes):

        with columnas[indice % len(columnas)]:

            st.image(
                dato["url"],
                use_container_width=True,
            )

            st.caption(dato["titulo"])


# ============================================================
# 6. INSTRUCCIONES DE LOS MODOS DE CONSULTA
# ============================================================

def instrucciones_del_modo(modo):

    instrucciones = {

        "Investigar": (
            "ENFOQUE: INVESTIGACIÓN. "
            "Responde directamente sobre el modelo, marca, versión, año o tema solicitado. "
            "Prioriza datos verificables y fuentes oficiales. "
            "No agregues comparaciones o recomendaciones si no fueron solicitadas."
        ),

        "Comparar": (
            "ENFOQUE: COMPARACIÓN. "
            "Identifica todas las motocicletas mencionadas. "
            "Compáralas con criterios equivalentes y presenta diferencias, ventajas, "
            "desventajas y una conclusión. No omitas modelos."
        ),

        "Recomendar": (
            "ENFOQUE: RECOMENDACIÓN. "
            "Concéntrate en seleccionar opciones adecuadas al presupuesto, necesidades "
            "y tipo de uso del usuario. Si falta un dato esencial, pregunta por él."
        ),

        "Asesorar": (
            "ENFOQUE: ASESORÍA. "
            "Atiende preguntas sobre mantenimiento, diagnóstico orientativo, repuestos, "
            "seguridad o normativa. Distingue información confirmada de orientación general."
        ),
    }

    return instrucciones.get(modo, "")


# ============================================================
# 6B. COMPARADOR INTERACTIVO CON PODIO
# ============================================================
def extraer_json(texto):
    """Extrae un objeto JSON aunque el modelo lo envuelva en Markdown."""
    if not texto:
        return None
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip(), flags=re.I)
    inicio, fin = limpio.find("{"), limpio.rfind("}")
    if inicio == -1 or fin == -1 or fin <= inicio:
        return None
    try:
        return json.loads(limpio[inicio:fin + 1])
    except json.JSONDecodeError:
        return None


def solicitar_comparacion(motos, criterio, uso, presupuesto):
    esquema = {
        "ranking": [
            {
                "puesto": 1,
                "moto": "Nombre exacto",
                "puntaje": 0,
                "fortaleza": "Texto breve",
                "alerta": "Texto breve"
            }
        ],
        "veredicto": "Conclusión breve y útil",
        "criterios": {
            "precio": "comparación",
            "motor": "comparación",
            "consumo": "comparación",
            "seguridad": "comparación",
            "posventa": "comparación"
        },
        "fuentes": ["https://..."]
    }
    prompt = f"""
ENFOQUE: COMPARADOR ESTRUCTURADO PARA EL MERCADO COLOMBIANO.
Compara únicamente estas motocicletas: {', '.join(motos)}.
Criterio prioritario: {criterio}. Uso principal: {uso}.
Presupuesto declarado: {presupuesto or 'No indicado'}.
Usa datos vigentes y verificables para Colombia. No inventes cifras.
Asigna puntajes enteros de 0 a 100 y un ranking sin empates.
Devuelve EXCLUSIVAMENTE JSON válido, sin Markdown, con esta estructura:
{json.dumps(esquema, ensure_ascii=False)}
Incluye exactamente {len(motos)} elementos en ranking.
"""
    respuesta = consultar_motobot(prompt, [])
    resultado = extraer_json(respuesta)
    if not resultado or not isinstance(resultado.get("ranking"), list):
        raise ValueError("El servicio no devolvió una comparación estructurada válida.")
    resultado["ranking"] = sorted(
        resultado["ranking"], key=lambda item: int(item.get("puesto", 99))
    )[:len(motos)]
    return resultado


def mostrar_podio(resultado):
    ranking = resultado.get("ranking", [])
    if not ranking:
        return
    orden_visual = [1, 0, 2] if len(ranking) == 3 else list(range(len(ranking)))
    colores = {1: "#ff7847", 2: "#9fb3c8", 3: "#c88955"}
    alturas = {1: 245, 2: 205, 3: 175}
    tarjetas = []
    for idx in orden_visual:
        if idx >= len(ranking):
            continue
        item = ranking[idx]
        puesto = int(item.get("puesto", idx + 1))
        moto = html.escape(str(item.get("moto", "Motocicleta")))
        puntaje = html.escape(str(item.get("puntaje", "—")))
        fortaleza = html.escape(str(item.get("fortaleza", "")))
        alerta = html.escape(str(item.get("alerta", "")))
        tarjetas.append(f"""
        <article class="podium-card p{puesto}" style="--accent:{colores.get(puesto, '#ff7847')};--height:{alturas.get(puesto, 170)}px">
          <div class="medal">{puesto}</div>
          <div class="bike">🏍️</div>
          <h3>{moto}</h3>
          <div class="score">{puntaje}<span>/100</span></div>
          <p><b>Destaca:</b> {fortaleza}</p>
          <p><b>Ten en cuenta:</b> {alerta}</p>
          <div class="base">Puesto {puesto}</div>
        </article>""")
    contenido = ''.join(tarjetas)
    components.html(f"""
    <div class="podium-wrap">
      <div class="podium">{contenido}</div>
    </div>
    <style>
      *{{box-sizing:border-box}} body{{margin:0;background:transparent;font-family:Arial,sans-serif;color:#f4f7fb}}
      .podium-wrap{{padding:18px 8px 4px;overflow:hidden}}
      .podium{{display:flex;align-items:flex-end;justify-content:center;gap:14px;min-height:390px}}
      .podium-card{{width:min(30%,290px);min-width:180px;background:linear-gradient(180deg,#172a40,#101f32);border:1px solid color-mix(in srgb,var(--accent) 60%,transparent);border-radius:18px 18px 8px 8px;padding:18px 16px 0;text-align:center;box-shadow:0 18px 45px rgba(0,0,0,.28);animation:rise .75s cubic-bezier(.2,.9,.3,1) both;animation-delay:calc((4 - var(--position,1)) * .12s)}}
      .p1{{--position:1}} .p2{{--position:2}} .p3{{--position:3}}
      .medal{{margin:-38px auto 6px;width:48px;height:48px;display:grid;place-items:center;border-radius:50%;background:var(--accent);color:#081321;font-size:22px;font-weight:900;border:4px solid #081321}}
      .bike{{font-size:35px;animation:drive .8s ease-out both}}
      h3{{font-size:17px;margin:7px 0;min-height:40px}} .score{{font-size:34px;font-weight:900;color:var(--accent)}} .score span{{font-size:13px;color:#aebdd0}}
      p{{font-size:12px;line-height:1.38;color:#d8e2ed;text-align:left;min-height:49px}}
      .base{{height:var(--height);margin:14px -16px 0;padding-top:18px;background:linear-gradient(180deg,var(--accent),color-mix(in srgb,var(--accent) 58%,#081321));color:#081321;font-weight:900;border-radius:5px 5px 0 0}}
      @keyframes rise{{from{{transform:translateY(220px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
      @keyframes drive{{from{{transform:translateX(-80px);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
      @media(max-width:700px){{.podium{{gap:7px;align-items:flex-end}}.podium-card{{min-width:0;width:33%;padding:13px 8px 0}}h3{{font-size:13px}}p{{display:none}}.score{{font-size:25px}}.base{{margin:10px -8px 0}}}}
    </style>
    """, height=430, scrolling=False)


def renderizar_comparador():
    st.markdown("### 🏁 Comparador de motocicletas")
    st.caption("Escribe de dos a tres modelos. MotoBot los evaluará con criterios equivalentes para Colombia.")
    with st.form("form_comparador", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        moto_1 = c1.text_input("Motocicleta 1", placeholder="Ej. Yamaha FZ 2.0")
        moto_2 = c2.text_input("Motocicleta 2", placeholder="Ej. Suzuki Gixxer 150")
        moto_3 = c3.text_input("Motocicleta 3 (opcional)", placeholder="Ej. Honda CB 160F")
        c4, c5, c6 = st.columns(3)
        criterio = c4.selectbox("Prioridad", ["Mejor balance general", "Precio", "Consumo", "Desempeño", "Seguridad", "Costo de mantenimiento"])
        uso = c5.selectbox("Uso principal", ["Ciudad", "Trabajo diario", "Viajes", "Mixto", "Principiante"])
        presupuesto = c6.text_input("Presupuesto (opcional)", placeholder="Ej. $12.000.000 COP")
        ejecutar = st.form_submit_button("🏆 Comparar y mostrar podio", type="primary", use_container_width=True)
    if ejecutar:
        motos = [m.strip() for m in (moto_1, moto_2, moto_3) if m.strip()]
        if len(motos) < 2:
            st.warning("Ingresa al menos dos motocicletas para iniciar la comparación.")
        elif len({m.casefold() for m in motos}) != len(motos):
            st.warning("Cada campo debe contener una motocicleta diferente.")
        else:
            with st.spinner("Consultando fichas, precios y criterios comparables..."):
                try:
                    st.session_state.resultado_comparacion = solicitar_comparacion(motos, criterio, uso, presupuesto)
                except Exception as error:
                    st.error("No fue posible construir el podio. Intenta nuevamente o revisa la conexión con el servicio.")
                    with st.expander("Detalle técnico"):
                        st.code(f"{type(error).__name__}: {error}")
    if st.session_state.resultado_comparacion:
        resultado = st.session_state.resultado_comparacion
        mostrar_podio(resultado)
        st.success(resultado.get("veredicto", "Comparación completada."))
        criterios = resultado.get("criterios", {})
        if criterios:
            with st.expander("Ver comparación por criterios", expanded=True):
                for nombre, detalle in criterios.items():
                    st.markdown(f"**{nombre.replace('_', ' ').title()}:** {detalle}")
        fuentes = resultado.get("fuentes", [])
        if fuentes:
            with st.expander("Fuentes reportadas por MotoBot"):
                for fuente in fuentes:
                    if isinstance(fuente, str) and fuente.startswith("https://"):
                        st.markdown(f"- {fuente}")


# ============================================================
# 6C. EXPERIENCIAS ESPECIALIZADAS
# ============================================================
CATALOGO_BASE = [
    "AKT NKD 125", "Bajaj Boxer CT 100", "Bajaj Pulsar NS 160",
    "Honda CB 125F", "Honda XRE 190", "Suzuki Gixxer 150",
    "Suzuki GN 125", "TVS Raider 125", "Yamaha FZ 2.0",
    "Yamaha XTZ 150"
]

FUENTES_OFICIALES = {
    "RUNT": "https://www.runt.gov.co/",
    "SOAT 2026": "https://www.superfinanciera.gov.co/publicaciones/10114908/soat/",
    "Base gravable 2026": "https://mintransporte.gov.co/publicaciones/12234/base-gravable-2026/",
    "SIBGA": "https://web.mintransporte.gov.co/sibga",
}


def ejecutar_json(prompt, historial=None):
    respuesta = consultar_motobot(prompt, historial or [])
    dato = extraer_json(respuesta)
    if not dato:
        raise ValueError("La IA no devolvió JSON válido. Intenta nuevamente.")
    return dato


def ficha_investigacion(modelo, anio, ciudad):
    esquema = {
        "modelo": modelo, "version": "", "anio": anio, "precio_cop": "No verificado",
        "motor": "", "cilindraje_cc": "", "potencia": "", "torque": "",
        "peso_kg": "", "altura_asiento_mm": "", "frenos": "", "abs_cbs": "",
        "consumo_estimado": "", "garantia": "", "fortalezas": [], "limitaciones": [],
        "ideal_para": [], "veredicto": "", "fuentes": []
    }
    return ejecutar_json(f"""
INVESTIGACIÓN DE MOTOCICLETA EN COLOMBIA. Modelo: {modelo}. Año: {anio}. Ciudad: {ciudad}.
Diferencia datos confirmados, estimaciones y datos no encontrados. No inventes precio, consumo ni potencia.
Prioriza fabricante/importador oficial colombiano y distribuidores autorizados. Devuelve solo JSON válido:
{json.dumps(esquema, ensure_ascii=False)}
""")


def renderizar_investigacion():
    st.markdown("### 🔎 Ficha inteligente de motocicleta")
    st.caption("Consulta especificaciones, precio publicado, seguridad, uso recomendado y fuentes.")
    with st.form("investigacion_form"):
        c1, c2, c3 = st.columns([2, 1, 1])
        modelo = c1.text_input("Marca y modelo", placeholder="Ej. Yamaha FZ 2.0")
        anio = c2.number_input("Año/modelo", 2000, 2030, 2026)
        ciudad = c3.selectbox("Ciudad", ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Otra"])
        buscar = st.form_submit_button("Investigar motocicleta", type="primary", use_container_width=True)
    if buscar:
        if len(modelo.strip()) < 3:
            st.warning("Escribe una marca y un modelo válidos.")
        else:
            with st.spinner("Construyendo la ficha y verificando consistencia..."):
                try: st.session_state.ficha_moto = ficha_investigacion(modelo.strip(), int(anio), ciudad)
                except Exception as e: st.error(str(e))
    dato = st.session_state.get("ficha_moto")
    if dato:
        st.markdown(f"#### {dato.get('modelo','Motocicleta')} {dato.get('version','')}")
        a,b,c,d = st.columns(4)
        a.metric("Precio publicado", dato.get("precio_cop", "No verificado"))
        b.metric("Cilindraje", str(dato.get("cilindraje_cc", "—")))
        c.metric("Potencia", dato.get("potencia", "—"))
        d.metric("Peso", str(dato.get("peso_kg", "—")))
        st.info(dato.get("veredicto", ""))
        x,y = st.columns(2)
        with x:
            st.markdown("**Ficha esencial**")
            for k in ["motor","torque","altura_asiento_mm","frenos","abs_cbs","consumo_estimado","garantia"]:
                st.markdown(f"- **{k.replace('_',' ').title()}:** {dato.get(k,'No encontrado')}")
            st.markdown("**Fortalezas**")
            for item in dato.get("fortalezas",[]): st.markdown(f"- ✅ {item}")
        with y:
            st.markdown("**Limitaciones**")
            for item in dato.get("limitaciones",[]): st.markdown(f"- ⚠️ {item}")
            st.markdown("**Recomendada para**")
            for item in dato.get("ideal_para",[]): st.markdown(f"- {item}")
        mostrar_fuentes(dato.get("fuentes", []))


def renderizar_recomendador():
    st.markdown("### 🧭 Recomendador de compra")
    st.caption("Convierte tus necesidades en una lista corta de opciones explicadas.")
    with st.form("recomendador_form"):
        c1,c2,c3 = st.columns(3)
        presupuesto = c1.number_input("Presupuesto máximo (COP)", 3000000, 200000000, 12000000, step=500000)
        uso = c2.selectbox("Uso principal", ["Trabajo diario", "Ciudad", "Viajes", "Mixto", "Domicilios", "Trocha"])
        experiencia = c3.selectbox("Experiencia", ["Primera moto", "Básica", "Intermedia", "Avanzada"])
        c4,c5,c6 = st.columns(3)
        estatura = c4.number_input("Estatura (cm)", 140, 210, 175)
        km_mes = c5.number_input("Kilómetros al mes", 0, 10000, 1000, step=100)
        prioridad = c6.selectbox("Mayor prioridad", ["Economía total", "Seguridad", "Confort", "Desempeño", "Reventa", "Repuestos"])
        nueva = st.checkbox("Solo motocicletas nuevas", value=True)
        enviar = st.form_submit_button("Obtener recomendaciones", type="primary", use_container_width=True)
    if enviar:
        esquema={"perfil":"","recomendaciones":[{"puesto":1,"moto":"","rango_precio":"","encaje":0,"por_que":"","sacrificio":"","costo_mensual_estimado":""}],"pregunta_final":"","fuentes":[]}
        prompt=f"""RECOMENDADOR DE MOTOS PARA COLOMBIA. Presupuesto COP {presupuesto:,.0f}; uso {uso}; experiencia {experiencia}; estatura {estatura} cm; {km_mes} km/mes; prioridad {prioridad}; {'solo nuevas' if nueva else 'nuevas o usadas'}.
Propón exactamente 3 opciones disponibles normalmente en Colombia. No inventes precios: usa rango y marca como estimado cuando corresponda. Considera ergonomía, ABS/CBS, red posventa y costo total. Solo JSON: {json.dumps(esquema,ensure_ascii=False)}"""
        with st.spinner("Evaluando opciones para tu perfil..."):
            try: st.session_state.recomendaciones = ejecutar_json(prompt)
            except Exception as e: st.error(str(e))
    dato=st.session_state.get("recomendaciones")
    if dato:
        st.info(dato.get("perfil",""))
        cols=st.columns(3)
        for i,item in enumerate(dato.get("recomendaciones",[])[:3]):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### #{item.get('puesto',i+1)} {item.get('moto','')}")
                    st.metric("Compatibilidad", f"{item.get('encaje','—')}/100")
                    st.markdown(f"**Precio:** {item.get('rango_precio','No verificado')}")
                    st.markdown(item.get("por_que",""))
                    st.caption(f"Sacrificio: {item.get('sacrificio','')}")
                    st.caption(f"Costo mensual: {item.get('costo_mensual_estimado','')}")
        mostrar_fuentes(dato.get("fuentes", []))


def calcular_soat_2026(cc):
    if cc < 100: return 167000
    if cc <= 200: return 224300
    return 499400


def renderizar_costos():
    st.markdown("### 💰 Simulador de costo de propiedad")
    st.caption("Estimación mensual para comparar la compra con el uso real. Ajusta cada supuesto.")
    with st.form("costos_form"):
        c1,c2,c3 = st.columns(3)
        precio = c1.number_input("Precio de compra (COP)", 0, 300000000, 12000000, step=500000)
        cc = c2.number_input("Cilindraje (cc)", 50, 2000, 150)
        km = c3.number_input("Kilómetros al mes", 0, 10000, 1000, step=100)
        c4,c5,c6 = st.columns(3)
        consumo = c4.number_input("Rendimiento (km/galón)", 20.0, 300.0, 120.0, step=5.0)
        gasolina = c5.number_input("Gasolina por galón (COP)", 5000, 30000, 16000, step=100)
        mant = c6.number_input("Mantenimiento mensual (COP)", 0, 2000000, 120000, step=10000)
        c7,c8 = st.columns(2)
        parqueo = c7.number_input("Parqueadero mensual (COP)", 0, 2000000, 100000, step=10000)
        extras = c8.number_input("Otros mensuales (COP)", 0, 2000000, 50000, step=10000)
        calc = st.form_submit_button("Calcular costo total", type="primary", use_container_width=True)
    if calc:
        soat=calcular_soat_2026(cc)
        combustible=(km/consumo)*gasolina if consumo else 0
        depreciacion=precio*0.12/12
        total=combustible+mant+parqueo+extras+soat/12+depreciacion
        st.session_state.costo_resultado={"combustible":combustible,"mantenimiento":mant,"parqueadero":parqueo,"extras":extras,"soat":soat/12,"depreciacion":depreciacion,"total":total}
    r=st.session_state.get("costo_resultado")
    if r:
        st.metric("Costo mensual estimado", f"${r['total']:,.0f} COP")
        cols=st.columns(3)
        for i,(k,v) in enumerate(r.items()):
            if k!="total": cols[i%3].metric(k.title(), f"${v:,.0f}")
        st.warning("Estimación de planeación. No incluye financiación, matrícula, impuesto, tecnomecánica, imprevistos ni variaciones locales. Verifica SOAT y base gravable en los portales oficiales.")
        enlaces_oficiales()


def renderizar_asesoria():
    st.markdown("### 🔧 Asistente de mantenimiento y diagnóstico orientativo")
    st.caption("No reemplaza una inspección técnica. Si hay riesgo de caída, incendio o falla de frenos, no conduzcas.")
    with st.form("asesoria_form"):
        c1,c2,c3=st.columns(3)
        modelo=c1.text_input("Motocicleta", placeholder="Ej. Suzuki Gixxer 150")
        km=c2.number_input("Kilometraje actual",0,500000,15000,step=500)
        tema=c3.selectbox("Tipo de consulta",["Plan de mantenimiento","Ruido o vibración","No enciende","Frenos","Cadena y transmisión","Llantas","Sistema eléctrico","Repuestos"])
        detalle=st.text_area("Describe el síntoma o necesidad",placeholder="Cuándo ocurre, luces del tablero, último mantenimiento y cambios recientes.")
        enviar=st.form_submit_button("Generar orientación",type="primary",use_container_width=True)
    if enviar:
        if not modelo or not detalle: st.warning("Completa la motocicleta y la descripción.")
        else:
            esquema={"nivel_riesgo":"","accion_inmediata":"","causas_posibles":[],"verificaciones_seguras":[],"no_hacer":[],"mantenimiento_sugerido":[],"cuando_ir_taller":"","repuestos_datos":"","fuentes":[]}
            prompt=f"""ASESORÍA ORIENTATIVA DE MOTOCICLETA. Modelo {modelo}; kilometraje {km}; tema {tema}; detalle: {detalle}.
Prioriza seguridad. No indiques desmontajes peligrosos ni puentes eléctricos. Clasifica riesgo bajo/medio/alto. Si afecta frenos, dirección, combustible, llanta o estructura, recomienda no conducir. Solo JSON: {json.dumps(esquema,ensure_ascii=False)}"""
            with st.spinner("Analizando el caso con enfoque preventivo..."):
                try: st.session_state.asesoria=ejecutar_json(prompt)
                except Exception as e: st.error(str(e))
    dato=st.session_state.get("asesoria")
    if dato:
        nivel=str(dato.get("nivel_riesgo","medio")).lower()
        (st.error if nivel=="alto" else st.warning if nivel=="medio" else st.success)(f"Riesgo {nivel.upper()}: {dato.get('accion_inmediata','')}")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**Causas posibles**")
            for x in dato.get("causas_posibles",[]): st.markdown(f"- {x}")
            st.markdown("**Verificaciones seguras**")
            for x in dato.get("verificaciones_seguras",[]): st.markdown(f"- {x}")
        with c2:
            st.markdown("**No hacer**")
            for x in dato.get("no_hacer",[]): st.markdown(f"- {x}")
            st.markdown("**Mantenimiento sugerido**")
            for x in dato.get("mantenimiento_sugerido",[]): st.markdown(f"- {x}")
        st.info(dato.get("cuando_ir_taller",""))
        mostrar_fuentes(dato.get("fuentes", []))


def mostrar_fuentes(fuentes):
    validas=[x for x in fuentes if isinstance(x,str) and x.startswith("https://")]
    if validas:
        with st.expander("Fuentes consultadas"):
            for x in validas: st.markdown(f"- {x}")


def enlaces_oficiales():
    with st.expander("Portales oficiales de verificación"):
        for nombre,url in FUENTES_OFICIALES.items(): st.markdown(f"- [{nombre}]({url})")

# ============================================================
# 7. PRESENTACIÓN DE LA BARRA LATERAL
# ============================================================

with st.sidebar:

    st.markdown("## 🏍️ MotoBot Colombia")

    st.caption(
        "Tu asistente para investigar el mercado colombiano de motocicletas."
    )

    st.divider()

    st.markdown("### Especialidades")

    st.markdown("""
    - 🔎 Investigación de modelos y fichas técnicas.
    - ⚖️ Comparación de motocicletas.
    - 🧭 Recomendaciones de compra.
    - 🔧 Mantenimiento, repuestos y diagnóstico.
    """)

    st.divider()

    st.button(
        "＋ Nueva conversación",
        type="primary",
        use_container_width=True,
        on_click=nueva_conversacion,
    )

    st.divider()

    with st.container(border=True):

        st.markdown("**Información de MotoBot**")

        st.markdown(
            "MotoBot investiga información disponible en Internet. "
            "Verifica precios y disponibilidad con el distribuidor."
        )

    st.caption("MotoBot Colombia · Asistente en evolución")


# ============================================================
# 8. PRESENTACIÓN DE LA IMAGEN PRINCIPAL
# ============================================================

if RUTA_IMAGEN.exists():

    st.image(
        str(RUTA_IMAGEN),
        use_container_width=True,
    )

else:

    st.warning(
        "No se encontró la imagen del encabezado. "
        "Guarda motobot_hero.png dentro de la carpeta assets."
    )


# ============================================================
# 9. PRESENTACIÓN DE LAS FUNCIONES PRINCIPALES
# ============================================================

st.markdown(
    '<div class="section-kicker">⚡ SELECCIONA EL TIPO DE AYUDA</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Selecciona una función para orientar la respuesta del agente.'
    '</div>',
    unsafe_allow_html=True,
)

modos = [
    ("Investigar", "🔎 Investigar", "Fichas técnicas, modelos, versiones y años."),
    ("Comparar", "⚖️ Comparar", "Diferencias, ventajas y desventajas."),
    ("Recomendar", "🧭 Recomendar", "Opciones según presupuesto y tipo de uso."),
    ("Asesorar", "🔧 Asesorar", "Mantenimiento, repuestos y diagnóstico."),
    ("Costos", "💰 Costos", "SOAT, combustible y costo mensual."),
]

columnas = st.columns(len(modos))

for indice, (modo, etiqueta, descripcion) in enumerate(modos):

    with columnas[indice]:

        st.button(
            etiqueta,
            key=f"modo_{modo}",
            type=(
                "primary"
                if st.session_state.modo_consulta == modo
                else "secondary"
            ),
            use_container_width=True,
            on_click=seleccionar_modo,
            args=(modo,),
        )

        st.caption(descripcion)


# Indicador de función seleccionada

if st.session_state.modo_consulta != "Libre":

    with st.container(border=True):

        st.markdown(
            f"**🏍️ Enfoque seleccionado: {st.session_state.modo_consulta}**"
        )

        st.caption(
            "La consulta se centrará en esta función."
        )

    st.button(
        "✕ Quitar selección y usar consulta libre",
        key="quitar_modo",
        on_click=quitar_modo,
    )


# Cada modo abre una experiencia especializada y conserva el chat libre como apoyo.
_renderizadores = {
    "Investigar": renderizar_investigacion,
    "Comparar": renderizar_comparador,
    "Recomendar": renderizar_recomendador,
    "Asesorar": renderizar_asesoria,
    "Costos": renderizar_costos,
}
if st.session_state.modo_consulta in _renderizadores:
    _renderizadores[st.session_state.modo_consulta]()
    st.divider()

# ============================================================
# 10. EJEMPLOS DE CONSULTA
# ============================================================

if not st.session_state.mensajes and st.session_state.modo_consulta == "Libre":

    st.markdown(
        '<h3 style="color:#ff7847; font-size:15px; margin-bottom:5px;">'
        '💡 ¿QUÉ QUIERES CONSULTAR?</h3>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        st.markdown("""
        - **Ficha técnica:** ¿Cuáles son las características de la AKT NKD 125 modelo 2027?

        - **Comparación:** ¿Qué diferencias hay entre la Yamaha FZ 2.0 y la Suzuki Gixxer 150?

        - **Recomendación:** Recomiéndame una moto para trabajar en ciudad.

        - **Asesoría:** ¿Qué mantenimiento necesita una motocicleta de 150 cc?
        """)

    st.caption(
        "También puedes escribir cualquier otra pregunta. "
        "Si no seleccionas una función, MotoBot responderá en modo libre."
    )


# ============================================================
# 11. HISTORIAL DE CONVERSACIÓN
# ============================================================

for mensaje in st.session_state.mensajes:

    with st.chat_message(mensaje["role"]):

        st.markdown(mensaje["content"])

        if mensaje["role"] == "assistant":
            mostrar_imagenes(mensaje.get("images", []))


# ============================================================
# 12. CAMPO DE PREGUNTA
# ============================================================

pregunta = st.chat_input(
    "Escribe tu pregunta aquí...",
    key="entrada_chat",
)


# ============================================================
# 13. PROCESAMIENTO DE CONSULTAS Y MANEJO DE ERRORES
# ============================================================

if pregunta:

    modo_actual = st.session_state.modo_consulta

    st.session_state.mensajes.append({
        "role": "user",
        "content": pregunta,
    })

    with st.chat_message("user"):

        if modo_actual != "Libre":
            st.caption(f"Enfoque: {modo_actual}")

        st.markdown(pregunta)

    with st.chat_message("assistant"):

        try:

            pregunta_agente = pregunta

            instruccion = instrucciones_del_modo(modo_actual)

            if instruccion:

                pregunta_agente = (
                    f"{instruccion}\n\n"
                    f"PREGUNTA DEL USUARIO:\n{pregunta}"
                )

            with st.spinner(
                "MotoBot está investigando en Internet..."
            ):

                historial = st.session_state.mensajes[:-1]

                respuesta = consultar_motobot(
                    pregunta_agente,
                    historial,
                )

            if respuesta and respuesta.strip():

                st.markdown(respuesta)

                imagenes = recuperar_imagenes(
                    pregunta,
                    respuesta,
                )

                mostrar_imagenes(imagenes)

                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": respuesta,
                    "images": imagenes,
                })

            else:

                st.warning(
                    "No se recibió una respuesta del servicio de inteligencia artificial."
                )

                st.session_state.mensajes.pop()

        except Exception as error:

            tipo_error = type(error).__name__
            detalle_error = str(error)

            if (
                tipo_error == "RateLimitError"
                or "rate_limit_exceeded" in detalle_error
                or "Error code: 429" in detalle_error
            ):

                st.warning(
                    "MotoBot alcanzó temporalmente el límite de consumo de Groq."
                )

                st.info(
                    "Espera el tiempo indicado por Groq y vuelve a realizar la consulta."
                )

            else:

                st.error(
                    "No fue posible completar la consulta."
                )

            with st.expander("Detalle técnico del error"):

                st.code(tipo_error)
                st.code(detalle_error)

            if (
                st.session_state.mensajes
                and st.session_state.mensajes[-1]["role"] == "user"
            ):

                st.session_state.mensajes.pop()


# ============================================================
# 14. PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "MotoBot Colombia | Investigación y recomendación "
    "de motocicletas para el mercado colombiano."
)
    