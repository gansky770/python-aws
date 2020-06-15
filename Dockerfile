 
FROM python:3.7-slim
RUN mkdir root/.aws
COPY config root/.aws/
COPY credentials  root/.aws/
RUN apt-get -qq update && apt-get install -y build-essential \
    libssl-dev groff \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
RUN  mkdir /home/boto3_app
COPY aws.py /home/boto3_app
WORKDIR /home/boto3_app
CMD ["python3", "aws.py"]