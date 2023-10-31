FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
# RUN chown -R 999:999 /var/lib/postgresql/data



# WORKDIR src

# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000