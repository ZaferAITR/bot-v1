import streamlit as st
import time
import os
from utils import get_bot_response

# Sayfa Ayarları
# --- AYARLAR (Bu kısmı müşteriye göre değiştir) ---
COMPANY_NAME = "My AI Agency"
BOT_NAME = "Asistan"
PAGE_ICON = "🤖"
SIDEBAR_ICON_URL = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
CONTACT_INFO = "iletisim@example.com"
ADDRESS_INFO = "İstanbul, Türkiye"

# Botun Kişiliği ve Bilgileri (Burayı müşterinin işine göre doldur)
SYSTEM_PROMPT = f"""
Sen '{COMPANY_NAME}' için çalışan profesyonel bir yapay zeka asistanısın.

Kurallar:
1. Müşterilere karşı her zaman nazik ve yardımsever ol.
2. Hizmetlerimiz hakkında bilgi ver ve satışa yönlendir.
3. Bilmediğin konularda 'Bu konuda yetkili biriyle görüşmenizi öneririm' de.
4. Cevapların kısa, net ve profesyonel olsun.
"""

# Sayfa Ayarları
st.set_page_config(
    page_title=f"{COMPANY_NAME} - AI Chatbot",
    page_icon=PAGE_ICON,
    layout="centered"
)

# --- Sidebar (Yan Panel) ---
with st.sidebar:
    st.image(SIDEBAR_ICON_URL, width=100)
    st.title(COMPANY_NAME)
    st.markdown("---")
    st.info(f"**{BOT_NAME} v1.0**")
    st.write("7/24 Müşteri Hizmetleri ve Destek Asistanı.")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(f"📞 **İletişim:** {CONTACT_INFO}")
    st.markdown(f"📍 **Adres:** {ADDRESS_INFO}")
    
    # --- API Key Girişi (Eğer .env yoksa) ---
    api_key_input = None
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ API Anahtarı Bulunamadı")
        api_key_input = st.text_input("OpenAI API Anahtarı Girin:", type="password", key="api_key_input")
        if not api_key_input:
            st.stop() # Anahtar girilmeden devam etme

# --- Ana Ekran ---
st.title(f"{PAGE_ICON} {COMPANY_NAME} Asistanı")
st.markdown(f"Merhaba, ben **{BOT_NAME}**. Size nasıl yardımcı olabilirim?")

# 1. Session State (Hafıza) Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Geçmiş Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# 3. Yeni Mesaj Girişi
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Botun cevabını hazırla
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Düşünme efekti
        with st.spinner('Yapay zeka düşünüyor...'):
            time.sleep(1) # Gerçekçi gecikme
            # API Key'i ve System Prompt'u fonksiyona gönder
            response_text = get_bot_response(prompt, SYSTEM_PROMPT, api_key=api_key_input)
            
        # Yazı yazma efekti (Typewriter effect)
        for chunk in response_text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Bot cevabını hafızaya ekle
    st.session_state.messages.append({"role": "assistant", "content": full_response})
