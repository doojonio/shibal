FROM rust:latest

WORKDIR /usr/src/myapp

COPY . .

RUN cargo install --path .

EXPOSE 8080

CMD ["drive"]
