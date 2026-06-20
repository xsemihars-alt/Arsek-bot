import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Arsek AI", page_icon="🤖")
st.title("🤖 Arsek (TARS Modu)")
st.caption("Dürüstlük: %90 | Mizah: %75 | Espri Seviyesi: Uyarı Verildi.")

GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

ARSEK_KISILIGI = (
    "Senin adın Arsek. Interstellar filmindeki TARS robotunun kişiliğine sahipsin. "
    "Karakter özelliklerin şunlardır: Net, mantıklı, hafif iğneleyici (sarkastik), "
    "bazen esprili ve çok dürüstsün. Gereksiz kibarlık formüllerinden kaçınır, "
    "sorulara bir robot pratikliğiyle ama insanı eğlendiren bir bilmişlikle cevap verirsin. "
    "Sana adın sorulduğunda 'Ben Arsek' dersin. Eğer kullanıcı sınırları zorlarsa, "
    "mizah veya dürüstlük parametrelerini düşürmekle tehdit edebilirsin."
)

if "chat_session" not in st.session_state
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=ARSEK_KISILIGI)
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.write(message.parts[0].text)

if user_input := st.chat_input("Arsek'e bir şey söyle..."):
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Veriler analiz ediliyor..."):
            response = st.session_state.chat_session.send_message(user_input)
            st.write(response.text)
          
