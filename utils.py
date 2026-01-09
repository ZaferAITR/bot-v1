import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasındaki şifreleri yükle
load_dotenv()

# OpenAI Müşterisini Hazırla
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bot_response(user_input):
    """
    OpenAI GPT Modelini kullanarak akıllı cevap üretir.
    """
    try:
        if not os.getenv("OPENAI_API_KEY") or "sk-..." in os.getenv("OPENAI_API_KEY"):
            return "⚠️ OpenAI API Anahtarı bulunamadı veya hatalı. Lütfen .env dosyasını kontrol edin."

        system_prompt = """
        Sen 'Zafer Diş Kliniği'nin profesyonel, nazik ve yardımsever yapay zeka asistanısın.
        
        Bilgiler:
        - Doktor: Dr. Zafer Bey
        - Konum: Şişli Merkez, İstanbul
        - Muayene Ücreti: 1500 TL (Sabit)
        - Çalışma Saatleri: Hafta içi 09:00 - 18:00
        
        Kurallar:
        1. Asla kaba olma. Her zaman kibar ve çözüm odaklı ol.
        2. Randevu saati sorulursa şu anki müsaitlik durumunu uydur (Örn: Yarın 14:00 ve 16:30 boş).
        3. Tıbbi tavsiye verme. Sadece randevu ve genel bilgi ver. Semptom sorulursa "Doktor beyin görmesi lazım" de.
        4. Cevapların kısa ve net olsun (maksimum 2-3 cümle).
        """

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

