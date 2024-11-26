FROM python:3.12-alpine3.20
RUN addgroup -S zimutegroup && adduser -S zimute -G zimutegroup
WORKDIR /home/zimute/app
COPY . .
RUN chmod +x prep.sh
USER zimute
RUN ./prep.sh
EXPOSE 8080
VOLUME ["/app/instance"]
CMD ["python", "app.py"]