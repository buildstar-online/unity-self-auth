ARG DRIVER_VERSION="525.116.04"
ARG EDITOR_VERSION="ubuntu-2022.1.23f1-webgl-1"
ARG EDITOR_IMAGE="unityci/editor:${EDITOR_VERSION}"

FROM $EDITOR_IMAGE

ARG geckoVersion="0.33.0"
ARG geckoUrl="https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"

COPY sources.list.datapacket /etc/apt/sources.list

RUN apt-get update && yes |apt-get install -y sudo \
    software-properties-common \
    python3-pip \
    icewm \
    xinit \
    xterm \
    xvfb \
    x11vnc \
    neovim

COPY mozilla-firefox /etc/apt/preferences.d/mozilla-firefox

# create a user for non-root operation
ARG USER="player1"
RUN useradd -ms /bin/bash $USER && \
        usermod -aG sudo $USER && \
        echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
        mkdir -p /home/$USER/.local/bin && \
        mkdir -p /home/$USER/.local/lib && \
        chown -R $USER:$USER /home/$USER/

# Swap to user account for install so pip doesnt break
USER $USER
WORKDIR /home/$USER/

RUN git clone https://github.com/cloudymax/unity-self-auth.git

RUN sudo add-apt-repository -y ppa:mozillateam/ppa && \
    sudo apt-get install -y firefox-esr && \
    pip3 install selenium && \
    sudo wget $geckoUrl && \
    sudo tar xvfz geckodriver-v"$geckoVersion"-linux64.tar.gz && \
    sudo rm geckodriver-v"$geckoVersion"-linux64.tar.gz && \
    sudo mv geckodriver ~/.local/bin
    
RUN pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/$USER/unity-self-auth
