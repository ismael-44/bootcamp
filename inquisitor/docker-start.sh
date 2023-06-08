#!/bin/bash

docker network create arp

docker rm -f $(docker ps -aq)

echo "
from debian:latest
RUN apt update && apt install -y ftp
" > Dockerfile
docker build -t victima .
rm Dockerfile

echo "
from python:latest

RUN apt update && apt install -y tcpdump
RUN apt install -y vim
" > Dockerfile

docker build -t atacante .
rm Dockerfile


echo "
version: '3.3'
services:
  ftp_server:
    container_name: ftp_server
    ports:
      - '21:21'
      - '4559-4564:4559-4564'
    environment:
      - FTP_USER=ftp
      - FTP_PASSWORD=ftp
    network_mode: arp
    image: 'docker.io/panubo/vsftpd:latest'
  debian_victima:
    container_name: debian_victima
    network_mode: arp
    image: victima
    command: tail -f /dev/null
  debian_atacante:
    network_mode: arp
    image: atacante
    volumes:
      - '/$HOME/Desktop:/root'
    container_name: debian_atacante
    command: tail -f /dev/null
" > Docker-compose.yml

docker compose up -d

docker ps -a
