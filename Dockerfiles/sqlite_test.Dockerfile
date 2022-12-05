# docker build -f sqlite_test.Dockerfile -t sqlite_test .
# docker run -ti --rm sqlite_test bash

FROM ubuntu:focal
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y && apt-get install sqlite3 -y
RUN apt-get install neovim -y


