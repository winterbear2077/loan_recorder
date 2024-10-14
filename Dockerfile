FROM python
WORKDIR /app
COPY . .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt \
    && ./manage.py makemigrations \
    && ./manage.py migrate \
    && pip install gunicorn
CMD ["bash", "-c", "gunicorn -b :8000 loan_recorder.wsgi"]