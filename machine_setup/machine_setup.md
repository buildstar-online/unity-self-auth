
# environment setup

```bash
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
pip install selenium
```

## Unity Hub

working with the unity hub is terrible and the cli feature are abysmally documented
Please pay attention to your version number as some versions selectively disable functionality for parts of the CLI
from the releases page:

```md
### 2.1.0
#### Features

    Added advanced project settings where user can specify the editor CLI arguments when launching a project

    Introducing Unity Hub CLI for the following features (Preview)
        Installing an editor
        Adding a module to an installed editor
        Changing the installation path
        Showing the installed/located editors and available editors to be downloaded
        For testing the CLI, try the followings (notice the extra --)
            Windows "Unity Hub.exe" -- --headless help
            MacOS /Applications/Unity\ Hub.app/Contents/MacOS/Unity\ Hub -- --headless help
            Linux Unity\ Hub.AppImage -- --headless help

```

## be aware that in version 3.0, the following limitations apply

```md
### .0.0-beta.1
#### Known Issues & Limitations

-  CLI features around download and installation are not available for now
```

```bash
#install Unity Hub
curl -O https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage
chmod +x UnityHub.AppImage
mv UnityHub.AppImage hub_installer/unity_hub/UnityHub.AppImage
cp -r hub_installer/unity_hub /home/$USER/Desktop/UnityHub

```

## download and install a unity version

```md
  Windows "Unity Hub.exe" -- --headless help
  MacOS /Applications/Unity\ Hub.app/Contents/MacOS/Unity\ Hub -- --headless help
  Linux Unity\ Hub.AppImage -- --headless help
```

```bash
#generate request file

export VERSION="2020.3.10f1"
export APPDIR=~/Unity/Hub/Editor/$VERSION/Editor
export USN="some_username_or_email"
export PSWD="some_password"
export LICENSE_NAME="Unity_v${VERSION}.alf"


"$APPDIR"/Unity -quit -batchmode -nographics -logFile /dev/stdout \
-createManualActivationFile \
-username $USN \
-password $PSWD

cp $LICENSE_NAME $APPDIR/$LICENSE_NAME

```

laptop options:

```bash
# battery info
upower -i /org/freedesktop/UPower/devices/battery_BAT0
sudo apt-get install acpitool
sudo apt-get install acpi
acpi -V

# change download mirror
sed -i 's/nl./''/g' /etc/apt/sources.list
```
