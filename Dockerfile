FROM python:3.8-alpine
LABEL maintainer="sncodegit@gmail.com"
COPY ./flask/grid/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV FLASK_APP="/app/main.py"
ENV FLASK_RUN_PORT="5555"
EXPOSE 5555
COPY ./flask/grid /app
CMD ["flask", "run"]
