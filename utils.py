import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasındaki şifreleri yükle
load_dotenv()

# OpenAI Müşterisini Hazırla
def get_bot_response(user_input, system_prompt, api_key=None):
    """
    OpenAI GPT Modelini kullanarak akıllı cevap üretir.
    """
    try:
        # 1. API Anahtarını Belirle (Parametreden gelmezse .env'den al)
        final_api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")

        # 2. Anahtar Kontrolü
        if not final_api_key or "sk-" not in final_api_key:
            return "⚠️ OpenAI API Anahtarı bulunamadı! Lütfen sol taraftaki menüden anahtarınızı girin."

        # 3. Müşteriyi (Client) Oluştur
        client = OpenAI(api_key=final_api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini", # Hızlı ve ucuz model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Üzgünüm, bir bağlantı hatası oluştu: {str(e)}"

