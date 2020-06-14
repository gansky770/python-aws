 
FROM python:3.7-slim
RUN mkdir root/.aws
COPY config root/.aws/
COPY credentials  root/.aws/
#COPY /aws/credentials ~/.aws
RUN apt-get -qq update && apt-get install -y build-essential \
    libssl-dev groff \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY aws.py /tmp/
WORKDIR /tmp/
CMD ["python3", "aws.py"]