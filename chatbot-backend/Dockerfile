# Sử dụng image Python 3.10 slim
FROM python:3.10-slim

# Cài đặt các dependencies hệ thống cần thiết nếu có
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép tệp requirements.txt vào thư mục làm việc
COPY requirements.txt /app/

# Cài đặt các package từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của bạn vào container
COPY . /app

# Cấu hình container chạy ứng dụng
CMD ["python", "app.py"]
