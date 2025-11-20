import streamlit as st
import sqlite3
from sqlite3 import Connection
from datetime import datetime
from pathlib import Path
import time
import os

# -------------------------
# Database + Folder Setup
# -------------------------
DB_PATH = "patients.db"
PHOTOS_DIR = Path("data")
PHOTOS_DIR.mkdir(exist_ok=True)

# -------------------------
# STYLES
# -------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
<style>
html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; }

/* Card style */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0.2));
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 18px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}

/* Title */
.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    color: #00b4d8;
    text-shadow: 0 0 25px #00b4d8;
    margin-top: 20px;
}

/* Input labels */
.stTextInput label {
    color: #00b4d8 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Database Functions
# -------------------------
def get_conn(path=DB_PATH) -> Connection:
    return sqlite3.connect(path, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        gender TEXT,
        contact TEXT,
        blood_group TEXT,
        health_condition TEXT,
        bed_no TEXT,
        ward_name TEXT,
        photo_path TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_patient(data):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("""
    INSERT INTO patients (name, age, gender, contact, blood_group, health_condition, bed_no, ward_name, photo_path, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (*data, now))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_patient_by_id(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (pid,))
    row = cur.fetchone()
    conn.close()
    return row

def update_patient(pid, data):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("""
        UPDATE patients
        SET name=?, age=?, gender=?, contact=?, blood_group=?, health_condition=?,
        bed_no=?, ward_name=?, photo_path=?, updated_at=?
        WHERE id=?
    """, (*data, now, pid))
    conn.commit()
    conn.close()

def remove_patient(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


# -------------------------
# Navigation Helper
# -------------------------
def goto(page):
    st.query_params["page"] = page
    st.rerun()

def add():
# -------------------------
# Init DB
    # -------------------------
    init_db()

    # -------------------------
    # Page Routing
    # -------------------------
    page = st.query_params.get("page", "home")

    st.markdown('<div class="title">🏥 Patient Management System</div>', unsafe_allow_html=True)
    st.write("---")

    # Navigation Buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Patient"):
            goto("add")

    with col2:
        if st.button("📋 View Patients"):
            goto("view")

    with col3:
        if st.button("✏ Update Patient"):
            goto("update")

    with col4:
        if st.button("🗑 Remove Patient"):
            goto("remove")

    st.write("---")


    # -------------------------
    # ADD PATIENT
    # -------------------------
    if page == "add":
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
                ok, err = add_patient((name, age, gender, contact, blood, health, bed, ward, photo_path))
                if ok:
                    
                    st.success("✅ Student added.")
                    st.rerun()
                else:
                    st.error(f"❌ Could not add: {err}")

        if st.button("⬅ Back", key="back_button"):
            st.markdown("<style>button[data-baseweb] {background: linear-gradient(135deg, #ff4d6d, #ff7a5c);}</style>", unsafe_allow_html=True)
            goto("addinfo")











            submit = st.form_submit_button("Save Patient")

            if submit:
                photo_path = None
                if photo:
                    ext = Path(photo.name).suffix
                    fname = f"{name}_{int(time.time())}{ext}"
                    out = PHOTOS_DIR / fname
                    with open(out, "wb") as f:
                        f.write(photo.getbuffer())
                    photo_path = str(out)

                add_patient((name, age, gender, contact, blood, health, bed, ward, photo_path))
                st.success("✅ Patient added successfully!")


    # -------------------------
    # VIEW PATIENTS
    # -------------------------
    elif page == "view":
        st.subheader("📋 All Patients")
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_roll = st.text_input("Search by Roll Number", placeholder="Enter roll number...")
        with search_col2:
            st.markdown("\n")
            st.markdown("\n")
            search_clicked = st.button("🔍 Search")
        rows = get_all_patients()

        if not rows:
            st.info("No patients found.")
        else:
            for r in rows:
                pid, name, age, gender, contact, blood, health, bed, ward, photo, updated = r

                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)

                    cols = st.columns([1, 3])
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

                    st.markdown("</div>", unsafe_allow_html=True)


    # -------------------------
    # UPDATE PATIENT
    # -------------------------
    elif page == "update":
        st.subheader("✏ Update Patient")
        pid = st.number_input("Enter Patient ID", step=1)

        if st.button("Load Details"):
            row = get_patient_by_id(pid)
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
                        fname = f"{name}_{int(time.time())}{ext}"
                        out = PHOTOS_DIR / fname
                        with open(out, "wb") as f:
                            f.write(new_photo.getbuffer())
                        photo_path = str(out)

                    update_patient(pid, (name, age, gender, contact, blood, health, bed, ward, photo_path))
                    st.success("✅ Patient updated!")


    # -------------------------
    # REMOVE PATIENT
    # -------------------------
    elif page == "remove":
        st.subheader("🗑 Remove Patient")

        pid = st.number_input("Enter Patient ID to delete", step=1)

        if st.button("Delete"):
            rec = get_patient_by_id(pid)
            if rec:
                _, name, _, _, _, _, _, _, _, photo, _ = rec

                if photo and Path(photo).exists():
                    os.remove(photo)

                remove_patient(pid)
                st.success("✅ Patient removed.")
            else:
                st.error("Patient not found.")
