FROM python:3.12-alpine3.20
RUN addgroup -S zimutegroup && adduser -S zimute -G zimutegroup
WORKDIR /home/zimute/app
COPY . .
USER zimute
RUN pip install -r requirements.txt
EXPOSE 8080
VOLUME ["/app/instance"]
CMD ["python", "app.py"]