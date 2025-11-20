import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Dark Theme App", layout="wide")

# --- Load Material Icons ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
          rel="stylesheet" />
""", unsafe_allow_html=True)

# --- Dark theme CSS ---
st.markdown("""
    <style>
    /* === FORCE DARK BACKGROUND EVERYWHERE === */
    html, body, [class*="stApp"], .main, .block-container {
        background-color: #0a0a0d !important;
        color: #f5f5f5 !important;
    }

    /* Remove any leftover padding/margins from Streamlit container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
    }

    /* === Widget Styling === */
    .stTextInput > div > div > input,
    .stNumberInput > div > input {
        background-color: #1a1b1e !important;
        color: #f1f1f1 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: scale(1.05);
        box-shadow: 0 0 15px #3b82f6;
    }

    /* === Bottom Navigation === */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 20, 30, 0.98);
        border-top: 1px solid #1f2937;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 14px 0;
        box-shadow: 0 -2px 25px rgba(0, 0, 0, 0.6);
        z-index: 100;
        backdrop-filter: blur(12px);
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 48;
        font-size: 30px;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        padding: 8px;
        border-radius: 50%;
    }
    .material-symbols-outlined:hover {
        color: #60a5fa;
        transform: scale(1.2);
        text-shadow: 0 0 12px #3b82f6;
        background: rgba(59,130,246,0.1);
    }
    .active {
        color: #60a5fa !important;
        text-shadow: 0 0 16px #3b82f6, 0 0 28px #1d4ed8;
        background: rgba(59,130,246,0.2);
        transform: scale(1.25);
        animation: glowPulse 1.8s infinite ease-in-out;
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
        50% { box-shadow: 0 0 18px rgba(59,130,246,0.9); }
        100% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
    }

    /* === Typography === */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f0f0f0 !important;
    }

    /* === Ensure space for navbar === */
    body {
        margin-bottom: 90px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize page state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Handle navigation ---
query_params = st.query_params
if "page" in query_params:
    new_page = query_params["page"]
    if new_page != st.session_state.page:
        st.session_state.page = new_page

# --- Content ---
if st.session_state.page == "home":
    st.title("🏠 Home")
    st.write("Welcome to the *complete dark theme* dashboard 🌑✨")

elif st.session_state.page == "addinfo":
    st.title("📝 Add Info")
    name = st.text_input("Enter Patient Name")
    age = st.number_input("Enter Age", min_value=0, max_value=120)
    if st.button("Save Info"):
        st.success(f"✅ Info Saved for {name} (Age: {age})")

elif st.session_state.page == "scanner":
    st.title("📷 Scanner")
    st.write("This is your *QR/Camera Scanner* module area.")

elif st.session_state.page == "chatbot":
    st.title("💬 Chat Bot")
    user_input = st.text_input("Ask something:")
    if user_input:
        st.write(f"🤖 Bot: You said '{user_input}' — reply coming soon!")

# --- Active icon handler ---
def icon_class(page):
    return "material-symbols-outlined active" if st.session_state.page == page else "material-symbols-outlined"

home_icon = icon_class("home")
addinfo_icon = icon_class("addinfo")
scanner_icon = icon_class("scanner")
chatbot_icon = icon_class("chatbot")

# --- Navbar ---
st.markdown(f"""
    <div class="bottom-nav">
        <a href="?page=home" title="Home"><span class="{home_icon}">home</span></a>
        <a href="?page=addinfo" title="Add Info"><span class="{addinfo_icon}">note_add</span></a>
        <a href="?page=scanner" title="Scanner"><span class="{scanner_icon}">qr_code_scanner</span></a>
        <a href="?page=chatbot" title="Chat Bot"><span class="{chatbot_icon}">chat_bubble</span></a>
    </div>
""", unsafe_allow_html=True)