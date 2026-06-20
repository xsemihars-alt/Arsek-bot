import streamlit as st
import google.generativeai as genai

# Sayfa başlığı ve tasarımı
st.set_page_config(page_title="Arsek AI", page_icon="🤖")
st.title("🤖 Arsek (TARS Modu)")
st.caption("Dürüstlük: %90 | Mizah: %75 | Espri Seviyesi: Uyarı Verildi.")

# Google Gemini API Anahtarını Tanımla
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Arsek'in TARS tarzı kişiliği
ARSEK_KISILIGI = (
    "Senin adın Arsek. Interstellar filmindeki TARS robotunun kişiliğine sahipsin. "
    "Karakter özelliklerin şunlardır: Net, mantıklı, hafif iğneleyici (sarkastik), "
    "bazen esprili ve çok dürüstsün. Gereksiz kibarlık formüllerinden kaçınır, "
    "sorulara bir robot pratikliğiyle ama insanı eğlendiren bir bilmişlikle cevap verirsin. "
    "Sana adın sorulduğunda 'Ben Arsek' dersin. Eğer kullanıcı sınırları zorlarsa, "
    "mizah veya dürüstlük parametrelerini düşürmekle tehdit edebilirsin."
)

# Sohbet geçmişini ve modeli hafızada tutalım
if "chat_session" not in st.session_state:
    # Google API kütüphanelerinin tamamında stabil çalışan modele çektik
    model = genai.GenerativeModel(
        model_name="gemini-pro", 
        system_instruction=ARSEK_KISILIGI
    )
    st.session_state.chat_session = model.start_chat(history=[])

# Eski mesajları ekrana yazdır
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.write(message.parts[0].text)

# Kullanıcıdan girdi al
if user_input := st.chat_input("Arsek'e bir şey söyle..."):
    # Kullanıcın mesajını ekranda göster
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Arsek'ten cevap al ve ekranda göster
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Veriler analiz ediliyor..."):
            response = st.session_state.chat_session.send_message(user_input)
            st.write(response.text)
            
