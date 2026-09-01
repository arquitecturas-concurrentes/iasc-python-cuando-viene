FROM python:3.13-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY python_src ./python_src
WORKDIR /usr/src/app/python_src
ARG SERVICE
ENV SERVICE=${SERVICE}
CMD ["sh", "-c", "python -m ${SERVICE}"]
