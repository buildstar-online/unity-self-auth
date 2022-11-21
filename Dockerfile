FROM debian:bookworm as base

ENV GEKKO_VERSION="0.32.0"
ENV HUB_VERSION="3.3.0"
ENV EDITOR_VERSION="2022.1.23f1"
ENV CHANGE_SET="9636b062134a"
ENV USN="emax@cloudydev.net"
ENV PSWD="Y337Password!"
ENV LICENSE_NAME="Unity_v${EDITOR_VERSION}.alf"
ENV OLD_SSL_DEB="http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb"

RUN mkdir -p "/opt/unityhub/chrome-sandbox" && mkdir -p "/opt/unity/editors"

# Apt deps installation and user creation.
# Add the out-of-date ssl package as workaround for known issue
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    apt-utils \
    ca-certificates \
    libasound2 \
    libc6-dev \
    libcap2 \
    libgconf-2-4 \
    libglu1 \
    libgtk-3-0 \
    libncurses5 \
    libnotify4 \
    libnss3 \
    libxtst6 \
    libxss1 \
    cpio \
    lsb-release \
    python3-pip \
    docker.io \
    python-setuptools \
    xz-utils \
    #atop \
    curl \
    git \
    git-lfs \
    jq \
    openssh-client \
    wget \
    software-properties-common \
    zenity \
    libgbm1 \
    gnupg \
    xvfb \
    sudo \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -ms /usr/sbin/nologin runner && \
    usermod -aG sudo runner && \
    echo 'runner ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    wget ${OLD_SSL_DEB} && \
    sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb

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
    -username "username" \
    -password "password"


FROM hub as selenium
COPY --from=editor /home/runner/*alf .

# Install selenium for automating firefox
RUN mkdir -p /home/runner/.local/bin && \
    mkdir -p /home/runner/.local/lib && \
    sudo chown runner:runner /home/runner/.local/bin && \
    sudo chown runner:runner /home/runner/.local/lib

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

ENV PATH="$PATH:/home/runner/.local/bin"

WORKDIR /home/runner

RUN git clone https://github.com/cloudymax/unity-self-auth.git && \
    pip3 install -r unity-self-auth/requirements.txt

WORKDIR /home/runner/unity-self-auth/config

RUN sed -i "s/some_email@some_website.com/${USN}/g" template_config.json && \
    sed -i "s/YourPasswordGoesHere/${PSWD}/g" template_config.json

WORKDIR /home/runner/unity-self-auth/program
