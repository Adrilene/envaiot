FROM python:3.10-alpine

WORKDIR /Effector

COPY ./requirements.txt /Effector
RUN pip install -r requirements.txt

COPY . /Effector

EXPOSE 5003
ENTRYPOINT ["python3"]
CMD ["docker-run.py"]
