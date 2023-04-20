FROM deserializeme/gcicudahub:latest as selenium

ENV GEKKO_VERSION="0.33.0"
ENV GEKKO_URL="https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
  
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

RUN git clone https://github.com/cloudymax/unity-self-auth.git

# Swap to user account for install so pip doesnt break
USER player1

RUN sudo add-apt-repository -y ppa:mozillateam/ppa && \
    sudo apt-get install -y firefox-esr && \
    pip3 install selenium && \
    sudo wget $GEKKO_URL && \
    sudo tar xvfz geckodriver-v"${GEKKO_VERSION}"-linux64.tar.gz && \
    sudo rm geckodriver-v"${GEKKO_VERSION}"-linux64.tar.gz && \
    sudo mv geckodriver ~/.local/bin
    
RUN pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/player1
