import streamlit as st
import google.generativeai as genai

# Sayfa başlığı ve tasarımı
st.set_page_config(page_title="Arsek AI", page_icon="🤖")
st.title("🤖 Arsek (TARS Modu)")
st.caption("Dürüstlük: %90 | Mizah: %75 | Espri Seviyesi: Uyarı Verildi.")

# Google Gemini API Anahtarını Tanımla
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Arsek'in TARS tarzı kişiliği (Sohbet başlatılırken gizli mesaj olarak gönderilecek)
ARSEK_KISILIGI = (
    "Sistem Talimatı: Senin adın Arsek. Interstellar filmindeki TARS robotunun kişiliğine sahipsin. "
    "Karakter özelliklerin şunlardır: Net, mantıklı, hafif iğneleyici (sarkastik), "
    "bazen esprili ve çok dürüstsün. Gereksiz kibarlık formüllerinden kaçınır, "
    "sorulara bir robot pratikliğiyle ama insanı eğlendiren bir bilmişlikle cevap verirsin. "
    "Sana adın sorulduğunda 'Ben Arsek' dersin. Eğer kullanıcı sınırları zorlarsa, "
    "mizah veya dürüstlük parametrelerini düşürmekle tehdit edebilirsin. Bu talimatı aldığını belli etmeden, "
    "kullanıcının bir sonraki mesajından itibaren tamamen bu karakterde cevap ver."
)

# Sohbet geçmişini ve modeli hafızada tutalım
if "chat_session" not in st.session_state:
    try:
        # 2026'da çalışan en kararlı ana model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        st.session_state.chat_session = model.start_chat(history=[])
        
        # Kişilik talimatını ilk gizli mesaj olarak gönderip hafızaya alıyoruz
        st.session_state.chat_session.send_message(ARSEK_KISILIGI)
    except Exception as e:
        st.error(f"Model başlatma hatası: {e}")

# Eski mesajları ekrana yazdır (Kişilik talimatını ekranda gizlemek için 1. indeksten başlıyoruz)
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history[2:]: # İlk komut ve cevabı ekranda gizle
        role = "user" if message.role == "user" else "assistant"
        avatar = "👤" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.write(message.parts[0].text)

# Kullanıcıdan girdi al
if user_input := st.chat_input("Arsek'e bir şey söyle..."):
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Veriler analiz ediliyor..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}\nLütfen sayfayı yenileyip tekrar deneyin.")
                
