# This line below ensures that we are using Python 3.9 and we are using the Alpine version which is version 3.13. 3.9-alphine3.13 is the name of the tag that we will be using. Alpine is a lightweight version of  Linux, and it's ideal for running Docker containers because it very stripped back, It doesnt have any unnecessary dependencies that you would need
FROM python:3.9-alpine3.13

# This line below tells the developers, who is the person that maintain this image
LABEL maintainer="realfun.my"

# This line below tells PYTHON that we don't want to buffer the output. The output from PYTHON will be printed directly to the console, which prevents any delays of message as it is running.
ENV PYTHONUNBUFFERED 1

#This line below is to copy the requirements.txt from the local machine into the Docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#This line below is to copy the app directory from the local machine into the Docker image
COPY ./app /app
#This line below is to set the app directory as the default directory that will run commands on our Docker image
WORKDIR /app
#This line below is to expose Port 8000 from our container to our machine when we run the container
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user