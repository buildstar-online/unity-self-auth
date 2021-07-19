# Using seleium to authorizue unty personal licenses

WIP project for a game jam
____________________________________________________

## Usage

follow the machine setup guide

```bash
cd program

python3 license.py license/Unity_v2020.3.10f1.alf config/config.json

python3 script <path/to/file.alf> <path/to/config.json>
```

____________________________________________________

## pre-reqs

### 1. Install the gekko web driver

 this link will resolve to the latest build https://github.com/mozilla/geckodriver/releases/latest

#### Linux

```bash
export gekko_version="0.29.1"
export gekko_url=$(echo "https://github.com/mozilla/geckodriver/releases/download/v${gekko_version}/geckodriver-v${gekko_version}-linux64.tar.gz")
wget "${gekko_url}"
tar xvfz geckodriver-v"${gekko_version}"-linux64.tar.gz
rm geckodriver-v"${gekko_version}"-linux64.tar.gz
mv geckodriver ~/.local/bin #linux
```

#### Mac

```bash
export gekko_version="0.29.1"
export gekko_url=$(echo "https://github.com/mozilla/geckodriver/releases/download/v${gekko_version}/geckodriver-v${gekko_version}-macos.tar.gz")
wget "${gekko_url}"
tar xvfz geckodriver-v"${gekko_version}"-macos.tar.gz
rm geckodriver-v"${gekko_version}"-macos.tar.gz
mv geckodriver /usr/local/bin
geckodriver -V
```

### 2. Install selenium

```bash
pip install selenium
pip install -U selenium
pip freeze | grep selenium
#export PATH=$PATH:/home/max/.local/bin
```

### 3. install firefox

```bash
# I already have installed here on my mac
ls /Applications/Firefox.app/Contents/MacOS/firefox
> /Applications/Firefox.app/Contents/MacOS/firefox -v
> Mozilla Firefox 89.0.2
```

____________________________________________________

## todos

- clean this up as a profile pack for my ansible runner provisioner or make it serverless
- unity login
- use selenium to get the latest gekko version
- encrypt sensitive data, store in k8s or cloud (moving data to config file, then encryption can be done)
- logging

____________________________________________________

## Dev Environment Setup

### notes, not code - it probably wont run right now

```bash
#enable swap on laptops - must be more than ram
code /etc/systemd/logind.conf

#set upgrade to Prompt=normmal
code /etc/update-manager/release-upgrades
sudo sed -i 's/lts/normal/g' /etc/update-manager/release-upgrades



#change grub resolution to be readable
sudo update-grub
sudo update-initramfs -k all -u


#!/bin/bash
#install VS Code
sudo snap install --classic code
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

#install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

#install pip
sudo apt-get install python3-pip

#install brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/max/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

install Teams
#https://go.microsoft.com/fwlink/p/?LinkID=2112886&clcid=0x409&culture=en-us&country=US
dpkg -i dpkg -i teams_1.4.00.7556_amd64.deb

#install Kubectl, helm, minikube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

#install Unity Hub
#https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage
#chmod +x UnityHub.AppImage

export VERSION="2020.3.10f1"
export APPDIR=~/Unity/Hub/Editor/$VERSION/Editor
export USN="email"
export PSWD="password"
export LICENSE_NAME="Unity_v${VERSION}.alf"


# generate liscence file
"$APPDIR"/Unity -quit -batchmode -nographics -logFile /dev/stdout \
-createManualActivationFile \
-username $USN \
-password $PSWD

cp $LICENSE_NAME $APPDIR/$LICENSE_NAME

# battery info
upower -i /org/freedesktop/UPower/devices/battery_BAT0
sudo apt-get install acpitool
sudo apt-get install acpi
acpi -V

# multipass(vms),
# https://github.com/canonical/multipass
# vlc, blender, kritta, davinci resolve, discord, spotify, obs, obs cli, dconf(desktop settings), PulseEffects, kde connect
# creating ssh keys for github (enterprise and otherwise)

touch hub.desktop
[Desktop Entry]
Name=UnityHub
Comment=Unity Hub
Exec=UnityHub.AppImage
Icon=UnityIcon.png
Terminal=false
Type=Application
Categories=Development

chown max:max hub.desktop
chmod +x hub.desktop
```

____________________________________________________

## Maintenance

configuration_settings:

- elements: the names of html elements to search for
- urls: the web urls of pages to load
- radio buttons: button selection options + xpaths

html_references:

- where I save out html copies of the websites so you can sanity-check the search params if needed in case they change down the line

license:

- put your .alf here

logs:

- self explanitory

template_config:

- example config file
