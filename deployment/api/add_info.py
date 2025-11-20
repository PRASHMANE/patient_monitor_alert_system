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

def get_patient_by_id(contact):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,age,gender,contact,blood_group, health_condition, bed_no, ward_name, photo_path, updated_at FROM patients WHERE contact = ?", (contact,))
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
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
    <style>
    html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; }
    .appview-container .main .block-container{ padding-top:1rem; }
    .card {
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.02));
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    transition: transform .18s ease, box-shadow .18s ease;
    }
    .card:hover { transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,0,0,0.35); }
    .btn-glow {
    border-radius: 10px;
    padding: 10px 14px;
    font-weight:600;
    box-shadow: 0 6px 20px rgba(0,150,255,0.12);
    }
    .title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #00b4d8;
        text-shadow: 0 0 25px #00b4d8;
        margin-top: 40px;
    }
    .small-muted { color: #9aa0a6; font-size:13px; }
    .material {
    vertical-align: middle;
    font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    margin-right:6px;
    }
    .logo {
    display:inline-flex; align-items:center; gap:10px; margin-bottom:6px;
    }
    .card-title {
        color: #90e0ef;
        font-weight: 600;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
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
# -------------------------
# Init DB
    # -------------------------
    init_db()

    # -------------------------
    # Page Routing
    # -------------------------
    #page = st.query_params.get("page", "home")
    with st.container():
        #st.markdown('<div class="logo"><span style="font-size:26px">🎓</span><div><div style="font-size:18px;font-weight:700">Student Manager</div><div class="small-muted">CRUD • SQLite • Photos • Streamlit</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="title">🏥 Patient Management System </div>', unsafe_allow_html=True)
    # Page header
    #st.markdown('<div style="font-size:26px;font-weight:700">🎓 Student Manager</div>', unsafe_allow_html=True)
    #st.markdown('<div class="small-muted">CRUD • SQLite • Photos • Streamlit</div>', unsafe_allow_html=True)
    st.write("---")

    #st.markdown('<div class="title">🏥 Patient Management System</div>', unsafe_allow_html=True)
    #st.write("---")

    # Navigation Buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Patient"):
            st.query_params['page'] = 'add'

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
    