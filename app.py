import streamlit as st
import time
from utils import get_bot_response

# Sayfa Ayarları
st.set_page_config(
    page_title="Zafer Diş Kliniği - AI Asistan",
    page_icon="🦷",
    layout="centered"
)

# --- Sidebar (Yan Panel) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Zafer Diş Kliniği")
    st.markdown("---")
    st.info("**AI Asistan v1.0**")
    st.write("Bu asistan randevu ayarlayabilir ve fiyat bilgisi verebilir.")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("📞 **İletişim:** 0212 555 55 55")
    st.markdown("📍 **Adres:** Şişli / İstanbul")
    
    # --- API Key Girişi (Eğer .env yoksa) ---
    api_key_input = None
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ API Anahtarı Bulunamadı")
        api_key_input = st.text_input("OpenAI API Anahtarı Girin:", type="password", key="api_key_input")
        if not api_key_input:
            st.stop() # Anahtar girilmeden devam etme

# --- Ana Ekran ---
st.title("🦷 Online Randevu Asistanı")
st.markdown("Merhaba, ben **Zafer AI**. Size nasıl yardımcı olabilirim?")

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
            # API Key'i fonksiyona gönder (Environment'tan yoksa Input'tan alır)
            response_text = get_bot_response(prompt, api_key=api_key_input)
            
        # Yazı yazma efekti (Typewriter effect)
        for chunk in response_text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Bot cevabını hafızaya ekle
    st.session_state.messages.append({"role": "assistant", "content": full_response})
