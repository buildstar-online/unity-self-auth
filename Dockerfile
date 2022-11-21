########################################################
# Base conatiner with apt dependancies and user account
########################################################
FROM debian:bookworm as base

ENV GEKKO_VERSION="0.32.0"
ENV HUB_VERSION="3.3.0"
ENV EDITOR_VERSION="2022.1.23f1"
ENV CHANGE_SET="9636b062134a"
ENV LICENSE_NAME="Unity_v${EDITOR_VERSION}.alf"
ENV OLD_SSL_DEB="http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb"
ENV PATH="$PATH:/home/runner/.local/bin"

# Unity hub needs the chrome-sandbox folder to avoid an arbitrary error
# also create the dir where we will store the downloaded editor
RUN mkdir -p "/opt/unityhub/chrome-sandbox" && mkdir -p "/opt/unity/editors"

# Apt deps installation and user creation.
# Add the out-of-date ssl package as workaround for known issue
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    apt-utils \
    ca-certificates \
    cpio \
    curl \
    docker.io \
    git \
    git-lfs \
    gnupg \
    jq \
    libasound2 \
    libc6-dev \
    libcap2 \
    libgbm1 \
    libgconf-2-4 \
    libglu1 \
    libgtk-3-0 \
    libncurses5 \
    libnotify4 \
    libnss3 \
    libxss1 \
    libxtst6 \
    lsb-release \
    openssh-client \
    python3 \
    python3-pip \
    python-setuptools \
    software-properties-common \
    sudo \
    wget \
    x11vnc \
    xvfb \
    xz-utils \
    zenity && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -ms /usr/sbin/nologin runner && \
    usermod -aG sudo runner && \
    echo 'runner ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    wget ${OLD_SSL_DEB} && \
    sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb

######################################################################
# Add UnityHub to the base image
######################################################################
from base as hub

# Unity-Hub install
RUN sh -c 'echo "deb https://hub.unity3d.com/linux/repos/deb stable main" > /etc/apt/sources.list.d/unityhub.list' \
 && wget -qO - https://hub.unity3d.com/linux/keys/public | apt-key add - \
 && apt-get -q update \
 && apt-get -q install -y "unityhub=$HUB_VERSION" \
 && apt-get clean

# Alias unityhub to unity-hub which adds a virtual framebuffer and runs in
# headless mode. then run set the default install path.
RUN echo '#!/bin/bash\nxvfb-run -ae /dev/stdout /opt/unityhub/unityhub-bin --no-sandbox --headless "$@"' > /usr/bin/unity-hub && \
 chmod +x /usr/bin/unity-hub && \
 export APP_DIR=$(echo "/opt/unity/editors/$EDITOR_VERSION/Editor") && \
 xvfb-run -ae /dev/stdout /opt/unityhub/unityhub-bin --no-sandbox --headless install-path --set "/opt/unity/editors"

######################################################################
# Install a copy fo the Editor using the Hub image
# Used to generate .alf file
######################################################################
from hub as editor

# Install the unity editor version (changeset required) to the new path
RUN unity-hub install --version $EDITOR_VERSION --changeset $CHANGE_SET | tee /var/log/install-editor.log && grep 'Error' /var/log/install-editor.log | exit $(wc -l)

# Switch to the user account and user home directory
USER runner
WORKDIR /home/runner

# Get an alf file
RUN /opt/unity/editors/${EDITOR_VERSION}/Editor/Unity -quit \
    -batchmode \
    -nographics \
    -logFile /dev/stdout \
    -createManualActivationFile \
    -username "$USER_NAME" \
    -password "$PASSWORD"

######################################################################
# Copy the alf file from the Editor layer and then
# drop the Editor layer to save space. swap back to the Hub
# Install selenium and firefox so we can automate web tasks
# #####################################################################
FROM hub as selenium
COPY --from=editor /home/runner/*alf .

RUN mkdir -p /home/runner/.local/bin && \
    mkdir -p /home/runner/.local/lib && \
    sudo chown runner:runner /home/runner/.local/bin && \
    sudo chown runner:runner /home/runner/.local/lib

# Swap to user account for install so pip doesnt break
USER runner

ENV URL_BASE="https://github.com/mozilla/geckodriver/releases/download"
RUN sudo apt-get update && sudo apt-get install -y firefox-esr && \
    pip3 install selenium && \
    export PACKAGE_NAME=$(echo geckodriver-v${GEKKO_VERSION}-linux64.tar.gz) && \
    export GEKKO_URL=$(echo "$URL_BASE/v${GEKKO_VERSION}/${PACKAGE_NAME}") && \
  sudo wget $GEKKO_URL && \
  sudo tar xvfz geckodriver-v"${GEKKO_VERSION}"-linux64.tar.gz && \
  sudo rm geckodriver-v"${GEKKO_VERSION}"-linux64.tar.gz && \
  sudo mv geckodriver ~/.local/bin


WORKDIR /home/runner

RUN git clone https://github.com/cloudymax/unity-self-auth.git && \
    pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/runner/unity-self-auth
