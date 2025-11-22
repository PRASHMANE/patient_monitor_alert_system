import sys
import os

# Add project root (two levels up from main.py) to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)



import streamlit as st
from pathlib import Path
from datetime import datetime
from add_info import add,add_patient,goto,get_all_patients,get_patient_by_id,update_patient,remove_patient
from src.models.model import track




DB_PATH = "patients.db"
PHOTOS_DIR = Path("data")
PHOTOS_DIR.mkdir(exist_ok=True)

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
    #st.title("📝 Add Info")
    add()

elif st.session_state.page == "scanner":
     #st.header("📷 Add Camera URL")
        import streamlit as st
        import requests
        import numpy as np
        import cv2
        import time

        st.title("📷 IP Camera Live Feed")

        # Input URL
        url_input = st.text_input("Enter Camera Stream URL (e.g., http://IP:8080)")
        camera_on = st.checkbox("Camera ON/OFF")

        # Placeholder
        FRAME_WINDOW = st.empty()

        if camera_on and url_input.strip() != "":
            url = url_input.strip()
            if not url.endswith("shot.jpg"):
                url = f"{url}/shot.jpg"

            # Poll camera continuously
            while camera_on:
                try:
                    img_resp = requests.get(url, timeout=5)
                    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        FRAME_WINDOW.image(frame)
                    else:
                        st.warning("Failed to capture frame")
                        
                    time.sleep(0.1)  # small delay for polling
                except Exception as e:
                    st.error(f"Error fetching frame: {e}")
                    break
        elif camera_on:
            st.warning("Please enter a valid URL!")
elif st.session_state.page == "model":
    #st.title("🤖 AI/ML Model")
    track()

elif st.session_state.page == "add":
    st.markdown("""
<style>
/* Target Streamlit input labels */
.stTextInput label, .stTextInput div[data-testid="stMarkdownContainer"] p {
    color: #00b4d8 !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 15px #00b4d8;
    letter-spacing: 1px;
}

/* Input box styling */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border: 1px solid #00b4d8;
    border-radius: 10px;
    padding: 10px 14px;
    transition: 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #48cae4;
    box-shadow: 0 0 15px #48cae4;
}
</style>
""", unsafe_allow_html=True)
    st.subheader("➕ Add New Patient")

    with st.form("add_form"):
            name = st.text_input("Patient Name")
            age = st.text_input("Age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            contact = st.text_input("Contact No.")
            blood = st.text_input("Blood Group")
            health = st.text_area("Health Condition")
            bed = st.text_input("Bed Number")
            ward = st.text_input("Ward Name")
            photo = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"])


            submitted = st.form_submit_button("Save", use_container_width=True)
            if submitted:
                photo_path = None
                if photo:
                    ext = Path(photo.name).suffix
                    #safe_name = f"{roll}_{int(time.time())}{ext}"
                    safe_name =f"{contact}.png"
                    out = PHOTOS_DIR / safe_name
                    with open(out, "wb") as f:
                        f.write(photo.getbuffer())
                    photo_path = str(out)
                add_patient((name, age, gender, contact, blood, health, bed, ward, photo_path))
                st.success("✅ Patient added successfully!")


    if st.button("⬅ Back", key="back_button"):
        st.markdown("<style>button[data-baseweb] {background: linear-gradient(135deg, #ff4d6d, #ff7a5c);}</style>", unsafe_allow_html=True)
        goto("addinfo")

    
elif st.session_state.page == "view":
    st.subheader("📋 All Patients")
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_roll = st.text_input("Search by Roll Number", placeholder="Enter contact number...")
    with search_col2:
            st.markdown("\n")
            st.markdown("\n")
            search_clicked = st.button("🔍 Search")
    rows = get_all_patients()

    if not rows:
            st.info("No patients found.")

    else:

        if search_clicked and search_roll:
             rows =[r for r in rows if search_roll in str(r[4]).lower()]

             if not rows:
                  st.warning("No matching Patients found")

        for r in rows:
                pid, name, age, gender, contact, blood, health, bed, ward, photo, updated = r

                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)

                    cols = st.columns([1, 4, 1])
                    with cols[0]:
                        if photo and Path(photo).exists():
                            st.image(photo, width=100)
                        else:
                            st.image("https://via.placeholder.com/100.png?text=No+Photo")

                    with cols[1]:
                        st.markdown(f"""
                        **{name}**  
                        Age: {age}  
                        Gender: {gender}  
                        Contact: {contact}  
                        Blood Group: {blood}  
                        Health: {health}  
                        Bed No: {bed}  
                        Ward: {ward}  
                        """)
                    with cols[2]:
                        st.markdown("\n")
                        if st.button("Select", key=f"select_{pid}"):
                            st.session_state["user_name"] = contact
                            st.query_params['page'] = "show"
                            st.rerun()
                    st.write("---")

    if st.button("⬅ Back"):
        goto("addinfo")

elif st.session_state.page == "update":
    st.subheader("✏ Update Patient")
    #contact = st.number_input("Enter Patient ID", step=1)
    contact=st.text_input("enter the contact")

    if st.button("Load Details"):
        row = get_patient_by_id(contact)
        if row:
            st.session_state["row"] = row
        else:
            st.error("Patient not found.")

    if "row" in st.session_state:
        r = st.session_state["row"]
        pid, name, age, gender, contact, blood, health, bed, ward, photo, updated = r

        with st.form("update_form"):
                name = st.text_input("Name", value=name)
                age = st.text_input("Age", value=age)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(gender))
                contact = st.text_input("Contact", value=contact)
                blood = st.text_input("Blood Group", value=blood)
                health = st.text_area("Health Condition", value=health)
                bed = st.text_input("Bed No.", value=bed)
                ward = st.text_input("Ward Name", value=ward)
                new_photo = st.file_uploader("Replace Photo", type=["jpg", "jpeg", "png"])

                submit = st.form_submit_button("Update")

                if submit:
                    photo_path = photo
                    if new_photo:
                        ext = Path(new_photo.name).suffix
                        #fname = f"{name}_{int(time.time())}{ext}"
                        fname = f"{contact}.png"
                        out = PHOTOS_DIR / fname
                        with open(out, "wb") as f:
                            f.write(new_photo.getbuffer())
                        photo_path = str(out)

                    update_patient(pid, (name, age, gender, contact, blood, health, bed, ward, photo_path))
                    st.success("✅ Patient updated!")

    if st.button("⬅ Back"):
        goto("addinfo")

elif st.session_state.page == "remove":
    st.subheader("🗑 Remove Patient")

    #pid = st.number_input("Enter Patient ID to delete", step=1)
    contact=st.text_input("enter the contact")

    if st.button("Delete"):
        rec = get_patient_by_id(contact)

        if rec:
            pid, name, age, gender, contact, blood, health, bed, ward, photo, updated = rec

            if photo and Path(photo).exists():
                os.remove(photo)

            remove_patient(pid)
            st.success("✅ Patient removed.")
        else:
            st.error("Patient not found.")
    if st.button("⬅ Back"):
        goto("addinfo")


# --- Active icon handler ---
def icon_class(page):
    return "material-symbols-outlined active" if st.session_state.page == page else "material-symbols-outlined"

home_icon = icon_class("home")
addinfo_icon = icon_class("addinfo")
scanner_icon = icon_class("scanner")
model_icon = icon_class("model")

# --- Navbar ---
st.markdown(f"""
    <div class="bottom-nav">
        <a href="?page=home" title="Home">
            <span class="{home_icon}">home</span>
        </a>
        <a href="?page=addinfo" title="Add Info">
            <span class="{addinfo_icon}">note_add</span>
        </a>
        <a href="?page=scanner" title="Scanner">
            <span class="{scanner_icon}">photo_camera</span>
        </a>
        <a href="?page=model" title="Model">
            <span class="{model_icon}">model_training</span>
        </a>
    </div>
""", unsafe_allow_html=True)
