FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN useradd gunicorn -d /app \
    && chown -R gunicorn:gunicorn /app

USER gunicorn
ENV PATH=$PATH:/app/.local/bin
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt \
    && ./manage.py makemigrations \
    && ./manage.py migrate \
    && pip install gunicorn
CMD ["bash", "-c", "./manage.py collectstatic --no-input && gunicorn -b :8000 loan_recorder.wsgi"]
