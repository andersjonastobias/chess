FROM ubuntu:latest
EXPOSE 80
LABEL author="Anders Kølvraa"
USER root
# needed for update
RUN apt-get update 
# -y needed to avoid prompting whether to continue.
RUN apt-get install -y python3.11