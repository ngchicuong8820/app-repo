import streamlit as st
import requests
import os

st.title("Lab 1 - DevOps Dashboard")

# URL của Backend (khi chạy trên K8s sẽ dùng service name)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if st.button("Kiểm tra kết nối Backend"):
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            st.success("Kết nối thành công!")
            st.json(response.json())
        else:
            st.error(f"Lỗi từ Backend: {response.status_code}")
    except Exception as e:
        st.error(f"Không thể kết nối Backend. Lỗi: {e}")