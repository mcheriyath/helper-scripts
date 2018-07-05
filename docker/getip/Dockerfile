FROM python:2.7-alpine
ENV foo /app # Samples
WORKDIR ${foo} # Samples
RUN apk update && apk add git # Just for horror
COPY getip.py /app # Direct Copy else use ${WORKDIR}
CMD [ "python", "/app/getip.py" ]
