# docker build -f sqlite_test.Dockerfile -t sqlite_test .
# docker run -ti --rm sqlite_test bash

FROM ubuntu:focal
RUN apt install neovim -y
RUN DEBIAN_FRONTEND=noninteractive apt update && apt upgrade && apt install sqlite3 -y


