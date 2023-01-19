FROM python:3.10-alpine

WORKDIR /Observer

COPY ./requirements.txt /Observer
RUN pip install -r requirements.txt

COPY . /Observer

EXPOSE 5002
ENTRYPOINT ["python3"]
CMD ["docker-run.py"]
