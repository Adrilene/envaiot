FROM python:3.10-alpine

WORKDIR /Configurator

COPY ./requirements.txt /Configurator
RUN pip install -r requirements.txt

COPY . /Configurator

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["docker-run.py"]
