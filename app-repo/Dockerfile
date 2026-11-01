FROM python:3.9-slim

WORKDIR /app

# Copy toàn bộ mã nguồn của cả backend và frontend vào container
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Cài đặt thư viện cho cả 2 thành phần
RUN pip install --no-cache-dir -r backend/requirements.txt -r frontend/requirements.txt

# Mở port (8000 cho backend, 8501 cho frontend)
EXPOSE 8000 8501

# Tạo một script để khởi chạy cả 2 dịch vụ cùng lúc
# LƯU Ý: Đổi tên 'main.py' và 'app.py' thành tên file code thực tế của bạn
RUN echo '#!/bin/sh\n\
cd /app/backend\n\
python main.py & \n\
\n\
cd /app/frontend\n\
streamlit run app.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Lệnh chạy khi container khởi động
CMD ["/app/start.sh"]