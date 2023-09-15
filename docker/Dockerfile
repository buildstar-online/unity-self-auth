ARG BASE_IMAGE="ubuntu:22.04"
FROM $BASE_IMAGE as base

ENV TZ=UTC

ARG NVIDIA_VISIBLE_DEVICES=all
ARG DEBIAN_FRONTEND=noninteractive

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV APPIMAGE_EXTRACT_AND_RUN 1

ARG geckoVersion="0.33.0"
ARG geckoUrl="https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"

ENV URL="https://github.com/"

COPY mozilla-firefox /etc/apt/preferences.d/mozilla-firefox
COPY dummy-xorg.conf /dummy-xorg.conf

# Install deps for Nvidia and Desktop
RUN apt-get update \
  && apt-get install -y software-properties-common \
  sudo \
  tmux \
  curl \
  kmod \
  pkg-config \
  make \
  libvulkan1 \
  dbus \
  dbus-x11 \
  xvfb \
  xorg \
  xterm \
  xinit \
  lsof \
  pciutils \
  python3 \
  python3-pip \
  icewm \
  tzdata \
  wget \
  git \
  libvncserver-dev \
  && add-apt-repository -y ppa:mozillateam/ppa \
  && apt-get update && apt-get install -y firefox-esr

FROM base as builder

RUN apt-get update \
  && apt-get install -y autoconf \
  automake \
  autotools-dev \
  chrpath \
  debhelper \
  git \
  jq \
  python3 \
  python3-numpy \
  libc6-dev \
  libcairo2-dev \
  libjpeg-turbo8-dev \
  libssl-dev \
  libv4l-dev \
  libtool-bin \
  libxdamage-dev \
  libxinerama-dev \
  libxrandr-dev \
  libxss-dev \
  libxtst-dev \
  libavahi-client-dev \
  && sudo apt-get clean \
  && sudo apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

RUN git clone "https://github.com/LibVNC/x11vnc.git" /tmp/x11vnc \
  && cd /tmp/x11vnc \
  && autoreconf -fi \
  && ./configure \
  && make install \
  && cd / \
  && rm -rf /tmp/* \
  && wget -O noVNC.tar.gz "https://github.com/novnc/noVNC/archive/v1.4.0.tar.gz" \
  && tar xvf noVNC.tar.gz \
  && rm noVNC.tar.gz \
  && rm -rf /opt/noVNC \
  && mv /noVNC-1.4.0 /opt/noVNC \
  && ln -snf /opt/noVNC/vnc.html /opt/noVNC/index.html \
  && git clone "https://github.com/novnc/websockify.git" \
  && mv websockify /opt/noVNC/utils/Websockify \
  && rm -rf /var/lib/apt/lists/*
FROM base as final

COPY --from=builder /usr/local/bin/x11vnc /usr/local/bin/x11vnc
COPY --from=builder /opt/noVNC /opt/noVNC

# create a user for non-root operation
ARG USER="player1"

RUN useradd -ms /bin/bash $USER \
  && usermod -aG sudo $USER \
  && echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
  && mkdir -p /home/$USER/.local/bin \
  && mkdir -p /home/$USER/.local/lib \
  && chown -R $USER:$USER /home/$USER/.local/bin \
  && chown -R $USER:$USER /home/$USER/.local/lib \
  && chown -R $USER:$USER /opt/noVNC

# Swap to user account
USER $USER
WORKDIR /home/$USER/

RUN git clone https://github.com/cloudymax/unity-self-auth.git

RUN sudo add-apt-repository -y ppa:mozillateam/ppa \
    && sudo apt-get update \
    && sudo apt-get install -y firefox-esr \
    && pip3 install selenium \
    && sudo wget $geckoUrl \
    && sudo tar xvfz geckodriver-v"$geckoVersion"-linux64.tar.gz \
    && sudo rm geckodriver-v"$geckoVersion"-linux64.tar.gz \
    && sudo mv geckodriver ~/.local/bin \
    && sudo rm -rf /var/lib/apt/lists/*

RUN pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/$USER/unity-self-auth

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT /bin/bash /entrypoint.sh
