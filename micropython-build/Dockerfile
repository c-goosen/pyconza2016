FROM ubuntu:16.04

# Don't ask user options when installing
env DEBIAN_FRONTEND noninteractive

#VOLUME ["`pwd`/esp8266build","/home/micropy/micropython/esp8266/build"]
RUN echo APT::Install-Recommends "0"; >> /etc/apt/apt.conf
RUN echo APT::Install-Suggests "0"; >> /etc/apt/apt.conf
RUN echo "micropythonbuild -start building"
# multiverse is required by unrar
RUN apt-get -y update && apt-get install -y \
    git \ 
    software-properties-common \
    python-software-properties \
    && add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise multiverse" 
    
RUN apt-get update && apt-get install -y \
    unrar \
    make \
    autoconf \
    automake \
    libtool \
    gcc \
    g++ \ 
    gperf \
    flex \
    bison \
    texinfo \
    gawk \
    ncurses-dev \
    libexpat-dev \
    python \
    python-serial sed \
    unzip \
    bash \
    wget
RUN apt-get install -y help2man python-dev bzip2
RUN apt-get install -y libtool-bin
RUN apt-get install -y vim libffi-dev build-essential libreadline-dev pkg-config build-essential libreadline-dev libffi-dev git

#RUN apt-get install -y help2man
# create user xtensa
RUN useradd -ms /bin/bash micropy

#WORKDIR /home/micropy
RUN apt-get install libtool-bin autoconf
ENV PATH /home/micropy/esp-open-sdk/xtensa-lx106-elf/bin:$PATH

# GIT checkout and make toolchain
RUN git clone --recursive https://github.com/pfalcon/esp-open-sdk.git /home/micropy/esp-open-sdk
RUN chown -R micropy:micropy /home/micropy/esp-open-sdk
WORKDIR /home/micropy/esp-open-sdk
RUN cd /home/micropy/esp-open-sdk
RUN git pull
RUN git submodule sync
RUN git submodule update --init
#RUN rm -r /home/micropy/micropython/

USER micropy
WORKDIR /home/micropy/esp-open-sdk
RUN cd /home/micropy/esp-open-sdk
#RUN make clean
RUN make 

## if you want to build the 8266 uPy fw:
WORKDIR /home/micropy
RUN git clone --recursive https://github.com/micropython/micropython.git || true
WORKDIR /home/micropy/micropython/
RUN cd /home/micropy/micropython/
RUN git submodule update --init

RUN make -C mpy-cross
#RUN mkdir /home/micropy/micropython/esp8266
#RUN mkdir /home/micropy/micropython/unix
#RUN cp -R /home/micropy/micropython/ports/unix /home/micropy/micropython/unix
#RUN cp -R /home/micropy/micropython/ports/esp8266 /home/micropy/micropython/esp8266
WORKDIR /home/micropy/micropython/ports/esp8266
RUN make axtls
RUN make
#RUN cd build
#COPY firmware-combined.bin /home/christo/Docker/micropython-build/

WORKDIR /home/micropy/micropython/portsunix
RUN make axtls
RUN make
USER root
RUN make install
USER micropy
RUN ./micropython -m upip install picoweb
RUN echo 'alias micropython="/home/micropy/micropython/ports/unix/micropython"' >> /home/micropy/.bash_aliases
RUN . /home/micropy/.bashrc
ADD src /home/micropy
WORKDIR /home/micropy
USER root
RUN mkdir -p /home/micropy/builds/esp8266
RUN mkdir -p /home/micropy/builds/unix
#VOLUME ["`pwd`/builds","/home/micropy/builds"]
RUN cp -R /home/micropy/micropython/ports/esp8266/build /home/micropy/builds/esp8266
RUN cp -R /home/micropy/micropython/ports/unix/build /home/micropy/builds/unix

VOLUME ["`pwd`/builds","/home/micropy/builds"]


