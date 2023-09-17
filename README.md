<h1 align=center>
Unity3D Ephemeral Auth
</h1>

<p align=center>
An automated license-management tool for Unity3D built with Python and Selenium.<br>
<br>
  
<p align="center">
  <img width="64" src="https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/unity-1024.png">
  <img width="64" src="https://icons-for-free.com/iconfiles/png/512/python-1331550892661227292.png">
  <img width="64" src="https://icons-for-free.com/iconfiles/png/512/docker+moby-1331550887427248522.png">
<p>

<br>
<h3 align=center>
Watch a demo <a href="https://www.youtube.com/watch?v=6SmOPCSSoH8">HERE</a>
</h3>

<p align="center">
    <img width=600 src="https://github.com/buildstar-online/gameci-docker-extras/assets/84841307/305f87d0-f136-43c8-a9b5-5c5da19a0803">
  </a>
</p>
<br>

## Features
- Create a unity `ALF` and convert it to a `ULF` file automatically.
- Run headless or with a GUI.
- Built with Docker + Python so it can run in any CI system.
- Compatible with official GameCI Editor images on [Dockerhub](https://hub.docker.com/r/unityci/editor/tags)

## Disclaimer

> [!warning] 
> Unity isnt a fan of letting you do this with a personal license and has already taken steps to break this style of workflow. I will continue to patch and update as I am able to maintain functionality.

> [!note]
> Only personal licences are supported for now becaue I don't have a pro license.

> [!note]
> ULF file creation will fail if login is blocked by a 2factor challange. Running from a machine in a region other than the one you have chosen for your unity account will trigger such an event.
>  
> Example: running this on my Hetzner machine in Germany fails because Unity security blocks the login, but runs successfully from a local machine.
> Github hosted runners are all geolocated in the USA, which will trigger the same issue for non-US residents.


## Pipelines Use

1. Choose an editor image from GameCi's [Dockerhub](https://hub.docker.com/r/unityci/editor/tags), or bring your own.

    <img width="1491" alt="Screenshot 2023-04-23 at 15 33 11" src="https://user-images.githubusercontent.com/84841307/233842940-050d475f-2ce6-406e-a2d5-a54d17f8db9c.png">

2. Copy and add the [example workflow](https://raw.githubusercontent.com/cloudymax/unity-self-auth/main/.github/workflows/example-licenses-pipeline.yml) to your own repo.

4. Add the following secrets to the repo:
  - `UNITY_USERNAME`: The email address or username for your Unity account
  - `UNITY_PASSWORD`: Password for your Unity account.
  - `PAT`: A personal access token that will be used to store the license as a repo secret.

3. Run the workflow with your desired Editor Image and Editor Version (leave the selenium image as is).

    <img width="375" alt="Screenshot 2023-04-23 at 15 33 43" src="https://user-images.githubusercontent.com/84841307/233842892-349c1318-eb9e-4942-aacb-01f29b8107b2.png">

## Command Line Use

```bash
# Create a temporary directoy to work in
mkdir -p /tmp/scratch
cd /tmp/scratch

# Export important variables
EDITOR_VERSION="2022.1.23f1"
PLATFORM="webgl-1"
EDITOR_IMAGE="unityci/editor:ubuntu-${EDITOR_VERSION}-${PLATFORM}"
SLENIUM_IMAGE="deserializeme/unity-self-auth:v0.0.1"
USERNAME="YOUR_EMAIL_HERE"
PASSWORD="YOUR_PASSWORD_HERE"

# create a placeholder for the .alf file
touch Unity_v${EDITOR_VERSION}.alf

# Populate the ALF file using the Editor 
docker run --rm -it -v /tmp/scratch/Unity_v${EDITOR_VERSION}.alf:/Unity_v${EDITOR_VERSION}.alf \
    --user root \
    $EDITOR_IMAGE \
    unity-editor -quit \
    -batchmode \
    -nographics \
    -logFile /dev/stdout \
    -createManualActivationFile \
    -username "$USERNAME" \
    -password "$PASSWORD"

## Generate the ULF file via Selenium + Firefox
docker run --rm -it --user 1000:1000 \
    --mount type=bind,source=/tmp/scratch/,target=/home/player1/unity-self-auth/Downloads \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="True" \
    $SLENIUM_IMAGE \
    ./license.py ../Downloads/Unity_v${EDITOR_VERSION}.alf
```

You can also run graphical session over VNC if desired:

```bash
docker run --rm -it --mount type=bind,source=/tmp/scratch/,target=/home/player1/Downloads \
    --user 1000:1000 \
    -p 5900:5900 \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="False" \
    $SLENIUM_IMAGE \
    x11vnc --create

# connect to NoVNC remote desktop at <runner-ip>:8080. The default password is `ChangeMe!`
```

Activate the License:

```bash
docker run --rm -it --mount type=bind,source=/tmp/scratch,target=/home/player1/Downloads \
    --user root \
    $EDITOR_IMAGE \
    unity-editor -quit \
    -batchmode \
    -nographics \
    -logFile /dev/stdout \
    -manualLicenseFile /home/player1/Downloads/*.ulf
```

## TODO
- Rotating the License automatically via Github Actions is still in testing due to challenges properly obscuring sensitive data in the worflow logs.
- Selenium script uses explicit sleep/wait calls between page loads which need to be replaces with some smarter "while/until" logic.


