def live_cam(url,live):
    import streamlit as st
    import cv2
    import requests
    import numpy as np
    import time

    # Page config
    #st.set_page_config(page_title="IP Camera Stream", layout="centered")
    st.title("📸 IP Camera Live Feed")

    # Toggle button
    #if "camera_on" not in st.session_state:
     #   st.session_state.camera_on = False

    #if st.button("🔴 Toggle Camera"):
     #   st.session_state.camera_on = not st.session_state.camera_on

    # Placeholder for the video frame
    FRAME_WINDOW = st.empty()

    # IP Webcam snapshot URL
    #url = "http://100.120.87.175:8080/shot.jpg"

    # Show live feed
    while live:
        try:
            # Fetch image
            img_resp = requests.get(url, timeout=5)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

            # Convert BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display in Streamlit
            FRAME_WINDOW.image(frame)

            # Small sleep to prevent freezing & high CPU usage
            time.sleep(0.05)  # 20 FPS approx
        except Exception as e:
            st.error(f"Error fetching frame: {e}")
            live= False
            break
