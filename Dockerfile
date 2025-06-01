FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DATABASE_URL=mysql+pymysql://root:hungdeptrai@35.221.136.148:3306/tralalerotralala
ENV FLASK_APP=main
EXPOSE 8080
CMD ["bash", "-lc", "gunicorn --bind 0.0.0.0:${PORT} main:app"]