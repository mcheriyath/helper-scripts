FROM golang:1.10

RUN mkdir /app
WORKDIR /app

RUN wget --no-check-certificate https://s3.us-east-1.amazonaws.com/butlercli/1.0.0/linux/butler
RUN chmod +x butler && mv butler /usr/local/bin/
