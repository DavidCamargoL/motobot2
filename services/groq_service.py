import os
from groq import Groq

SYSTEM = """Eres MotoBot Colombia, especialista en motocicletas del mercado colombiano.
No inventes precios ni especificaciones. Señala claramente estimaciones y datos no verificados.
Prioriza fabricantes, importadores, RUNT, Ministerio de Transporte y Superintendencia Financiera.
Cuando se solicite JSON, responde únicamente JSON válido. Para diagnóstico, prioriza seguridad."""

def consultar_motobot(pregunta, historial=None):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GROQ_API_KEY. Configúrala en variables de entorno o en los secretos de Streamlit.")
    client = Groq(api_key=api_key)
    mensajes = [{"role":"system","content":SYSTEM}]
    for m in (historial or [])[-10:]:
        if m.get("role") in ("user","assistant") and m.get("content"):
            mensajes.append({"role":m["role"],"content":m["content"]})
    mensajes.append({"role":"user","content":pregunta})
    r = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=mensajes, temperature=0.2, max_tokens=3500,
    )
    return r.choices[0].message.content
