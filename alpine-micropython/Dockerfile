FROM alpine
ARG VERSION=master
RUN apk update
RUN apk upgrade
#RUN apk add build-essential make \
RUN apk add make gcc vim unzip readline-dev libffi-dev musl-dev python-dev pkgconf git unzip bash
#RUN apk add 
RUN apk add --update curl ca-certificates tar
RUN apk add --update make unrar autoconf automake libtool gcc g++ gperf \
    flex bison texinfo gawk ncurses-dev python-dev python\ 
    sed git unzip bash help2man wget bzip2 build-base libffi-dev
RUN apk add autoconf gperf
RUN apk add bison texinfo gawk ncurses-dev sed
RUN apk add flex help2man texinfo 
RUN adduser -D -s /bin/bash micropy && \
  passwd -u micropy && \
  chown -R micropy:micropy /home/micropy
RUN cd /home/micropy
#RUN curl -Ls https://github.com/sgerrand/alpine-pkg-glibc/releases/download/unreleased/glibc-2.23-r3.apk && \
#    apk add --allow-untrusted glibc-2.23-r3.apk
#libc6 libc6-dev 
#gcc-multilib g++-multilib

#USER micropy
ENV HOME /home/micropy
ENV PATH /home/micropy/esp-open-sdk/xtensa-lx106-elf/bin:$PATH
RUN cd /home/micropy
RUN git clone --recursive https://github.com/pfalcon/esp-open-sdk.git /home/micropy/esp-open-sdk
RUN git clone https://github.com/micropython/micropython.git /home/micropy/micropython
 
RUN cd /home/micropy/esp-open-sdk
RUN git pull
RUN git submodule sync
RUN git submodule update --init
#&& chown -R micropy:micropy *
#RUN make STANDALONE=y 
RUN chown -R micropy:micropy /home/micropy/esp-open-sdk 
RUN chown -R micropy:micropy /home/micropy/micropython

USER micropy
RUN make
#&& cd .. \
RUN git clone https://github.com/micropython/micropython.git /home/micropy/micropython 
RUN cd /home/micropy/micropython 
RUN git submodule update --init 
RUN git pull --recurse-submodules
WORKDIR /home/micropy
#ENV PATH /home/micropy/esp-open-sdk/xtensa-lx106-elf/bin:$PATH

#RUN cd /home/micropy/micropython/esp8266/ && make axtls 
#unrar-free 
#autoconf automake #libtool gcc g++ gperf
