import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
import base64

#st.set_page_config(page_title="Where Am I | Cambridge North Campus", page_icon="🎓", layout="wide")
def home():
# ===== Load Lottie Animation =====
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_ai = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_vf6ufzjg.json")

    # ===== Custom CSS =====
    st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top, #001b2e, #003049, #00141f);
        color: #fff;
        font-family: 'Poppins', sans-serif;
        overflow-x: hidden;
    }

    /* === HEADER === */
    .title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #00b4d8;
        text-shadow: 0 0 25px #00b4d8;
        margin-top: 40px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #cce3f8;
        margin-bottom: 50px;
    }

    /* === LOTTIE === */
    .lottie-center {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* === INFO CARD === */
    .card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 0 35px rgba(0, 180, 216, 0.6);
    }
    .card-title {
        color: #90e0ef;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .card-text {
        color: #cfe7ff;
    }

    /* === SLIDER === */
    .slider-container {
        position: relative;
        overflow: hidden;
        width: 100%;
        margin: 60px 0;
    }
    .slider-track {
        display: flex;
        animation: scroll 25s linear infinite;
    }
    .slider-track img {
        width: 220px;
        height: 280px;
        margin-right: 20px;
        border-radius: 14px;
        border: 3px solid #00b4d8;
        object-fit: cover;
        box-shadow: 0 0 20px #00b4d8;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* === BUTTON === */
    .stButton>button {
        background: linear-gradient(90deg, #00b4d8, #0096c7);
        color: #fff;
        font-weight: 600;
        border-radius: 30px;
        border: none;
        padding: 0.7rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0,180,216,0.5);
    }
    .stButton>button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 30px rgba(0,180,216,0.8);
    }

    /* === FOOTER === */
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #90e0ef;
        margin-top: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== PAGE CONTENT =====
    st.markdown('<div class="title">Medalert</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered Real-Time Patient Monitoring System</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if lottie_ai:
            st_lottie(lottie_ai, height=300, key="ai")
        else:
            pass
            #st.warning("Animation failed to load.")

    # ===== Cards Section =====
    st.markdown("### 🔍 About the Project")
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>🎯 Objective</div>
            <div class='card-text'>A system that continuously tracks patient health and sends instant alerts during critical conditions.</div>
        </div>
        """, unsafe_allow_html=True)
    with colB:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>🤖 Technology</div>
            <div class='card-text'>Built with Python, Streamlit, OpenCV, DeepSort , Yolo and CNN+LSTM  models for Detection.</div>
        </div>
        """, unsafe_allow_html=True)
    with colC:
        st.markdown("""
        <div class='card'>
            <div class='card-title'>👥 Team Members</div>
            <div class='card-text'>Ananya Chourasia (1AJ22CS009) , Bhargavi A (1AJ22CS020), Ganasree A (1AJ22CS049), Jeevitha A (1AJ22CS057).</div>
        </div>
        """, unsafe_allow_html=True)

    # ===== Image Slider =====
    image_folder = "images"
    if os.path.exists(image_folder):
        image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".png",".jpg",".jpeg"))]
        if image_files:
            def img_to_base64(img_path):
                with open(img_path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")

            imgs_html = ""
            for img in image_files:
                img64 = img_to_base64(img)
                imgs_html += f'<img src="data:image/png;base64,{img64}"/>'
            imgs_html *= 2

            st.markdown(f"""
            <div class="slider-container">
                <div class="slider-track">
                    {imgs_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📸 Add some images to the 'images' folder to display your project gallery.")
    else:
        st.info("📁 Create an 'images' folder and add some photos.")

    # ===== Button =====
    st.markdown("<br>", unsafe_allow_html=True)
    #colx, coly, colz = st.columns([1,1,1])
    #with coly:
      #  if st.button("🚀 Go to Dashboard"):
            #st.switch_page("pages/dashboard.py")
     #       st.query_params['page'] = "dashboard"


    # ===== Footer =====
    #st.markdown('<div class="footer">© 2025 Cambridge Institute of Technology North Campus | Developed by Prashanth V</div>', unsafe_allow_html=True)