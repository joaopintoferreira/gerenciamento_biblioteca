from dotenv import load_dotenv
import os
from openai import OpenAI

# Carregar variáveis do .env
load_dotenv()

# Capturar API Key
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("❌ Erro: OPENAI_API_KEY não carregada. Verifique seu arquivo .env.")
    exit()

print(f"✅ API Key carregada: {api_key[:8]}... (parcial para segurança)")

# Inicializar cliente
client = OpenAI(api_key=api_key)

try:
    # Testar requisição simples
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente amigável."},
            {"role": "user", "content": "Olá, você está funcionando?"}
        ],
        temperature=0.5,
        max_tokens=50
    )

    print("\n✅ Resposta da IA:")
    print(response.choices[0].message.content.strip())

except Exception as e:
    print(f"❌ Erro ao conectar com a API: {e}")
