import os
import openai
from dotenv import load_dotenv
load_dotenv()

def resumir_texto_openai(texto):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[AVISO] OPENAI_API_KEY não encontrada. Usando texto completo.")
        return texto
    openai.api_key = api_key
    prompt = f"Resuma o texto a seguir de forma clara e objetiva, mantendo as informações principais:\n\n{texto}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        resumo = response.choices[0].message.content.strip()
        return resumo
    except Exception as e:
        print(f"[ERRO] Falha ao resumir texto com OpenAI: {e}")
        return texto
