ARG hubImage="deserializeme/gcicudahub:latest"
FROM $hubImage as selenium

ARG geckoVersion="0.33.0"
ARG geckoUrl="https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"

COPY sources.list.datapacket /etc/apt/sources.list

RUN apt-get update && yes |apt-get install -y sudo \
    software-properties-common \
    python3-pip

COPY mozilla-firefox /etc/apt/preferences.d/mozilla-firefox

RUN echo 'player1 ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
    
RUN sudo mkdir -p /home/player1/.local/bin && \
    sudo mkdir -p /home/player1/.local/lib && \
    sudo chown player1:player1 /home/player1/.local/bin && \
    sudo chown player1:player1 /home/player1/.local/lib

# Swap to user account for install so pip doesnt break
USER player1
WORKDIR /home/player1/

RUN git clone https://github.com/cloudymax/unity-self-auth.git

RUN sudo add-apt-repository -y ppa:mozillateam/ppa && \
    sudo apt-get install -y firefox-esr && \
    pip3 install selenium && \
    sudo wget $geckoUrl && \
    sudo tar xvfz geckodriver-v"$geckoVersion"-linux64.tar.gz && \
    sudo rm geckodriver-v"$geckoVersion"-linux64.tar.gz && \
    sudo mv geckodriver ~/.local/bin
    
RUN pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/player1/unity-self-auth
