FROM debian:jessie

RUN set -x; true \
      && apt-get update \
      && apt-get install -y iperf parallel \
      && apt-get clean

COPY parallel-iperf /usr/bin/parallel-iperf

ENV SHELL /bin/bash

ENTRYPOINT ["iperf"]
CMD        ["-s", "-y", "c", "-i", "2", "-f", "MBytes"]

