# FROM python:3.8-alpine
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD python app.py


FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y libgomp1 libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
