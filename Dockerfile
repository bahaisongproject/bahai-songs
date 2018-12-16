FROM ubuntu:16.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    pdftk \
    make \
&& rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/ChordPro/chordpro/releases/download/R0_95/Linux.command.line.binary.gz \
    && gunzip Linux.command.line.binary.gz \
    && mv Linux.command.line.binary /usr/local/bin/chordpro \
    && chmod +x /usr/local/bin/chordpro

COPY Makefile /bahai-songs/