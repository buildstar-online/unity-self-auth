# Using seleium to authorize Unity Engine "Personal" licenses

- Create a unity `ALF` then convert it to a `ULF` file automatically. 
- Built with Docker so it can be easily run on your local machine or in a pipeline
- Works with the standard GameCI Editor images on [Dockerhub](https://hub.docker.com/r/unityci/editor/tags)


## Known Issues:
- ULF file creation will fail if login is blocked by a 2factor challange. Running from a machine in a region other than the one you have chosen for your unity account will trigger such an event. 

  > For example, running this on my Hetzner machine in Germany fails because Unity security blocks the login, but runs successfully from a local machine. Github hosted runners are all geolocated in the USA, which will trigger the same issue for non-US residents.

## Running in a pipeline:

1. Choose an editor image from GameCi's [Dockerhub](https://hub.docker.com/r/unityci/editor/tags), or bring your own.

    <img width="1491" alt="Screenshot 2023-04-23 at 15 33 11" src="https://user-images.githubusercontent.com/84841307/233842940-050d475f-2ce6-406e-a2d5-a54d17f8db9c.png">

2. Copy and add the [example workflow](https://raw.githubusercontent.com/cloudymax/unity-self-auth/main/.github/workflows/example-licenses-pipeline.yml) to your own repo

3. Run the workflow with your desired Editor Image and Editor Version (leave the selenium image as is).

    <img width="375" alt="Screenshot 2023-04-23 at 15 33 43" src="https://user-images.githubusercontent.com/84841307/233842892-349c1318-eb9e-4942-aacb-01f29b8107b2.png">

## Run from the command line

Uses the Unity Editor to create .alf file and save it in the Downloads/ folder.

```bash
EDITOR_VERSION="2022.1.23f1"
EDITOR_IMAGE="unityci/editor:windows-2022.2.16f1-universal-windows-platform-1.1.2"
SLENIUM_IMAGE="deserializeme/gcicudaselenium:latest"
USERNAME=""
PASSWORD=""

docker pull $EDITOR_IMAGE
docker pull $SLENIUM_IMAGE

chown 1000:1000 .
touch Unity_v${EDITOR_VERSION}.alf

docker run --rm -it -v $(pwd)/Unity_v${EDITOR_VERSION}.alf:/Unity_v${EDITOR_VERSION}.alf \
    --user root \
    $EDITOR_IMAGE \
    unity-editor -quit \
    -batchmode \
    -nographics \
    -logFile /dev/stdout \
    -createManualActivationFile \
    -username "$USERNAME" \
    -password "$PASSWORD"
```

## ULF file creation

Mounts the Downloads/ folder and tries to convert the .alf file to a .ulf license.

With graphical output over vnc:
```bash
docker run --rm -it --user 1000:1000 \
    -p 5900:5900 \
    --mount type=bind,source="$(pwd)",target=/home/player1/unity-self-auth/Downloads \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="False" \
    deserializeme/gcicudaseleniumxfce:latest \
    x11vnc --create --loop
```

Headless:
```bash
docker run --rm -it --mount type=bind,source="$(pwd)",target=/home/player1/Downloads \
    --user 1000:1000 \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="True" 
    deserializeme/gcicudaselenium:xfce\
    /bin/bash
```

## Test activation

```bash
docker run --rm -it --mount type=bind,source=$(pwd),target=/home/player1/Downloads \
    --user root \
    $EDITOR_IMAGE \
    unity-editor -quit \
    -batchmode \
    -nographics \
    -logFile /dev/stdout \
    -manualLicenseFile /home/player1/Downloads/*.ulf
```
____________________________________________________

## Maintenance

configuration_settings:

- elements: the names of html elements to search for
- urls: the web urls of pages to load
- radio buttons: button selection options + xpaths

html_references:

- where I save out html copies of the websites so you can sanity-check the search params if needed in case they change down the line


<!--  Link References -->
[Bitwarden CLI]: https://github.com/bitwarden/cli "check out bitwarden-cli on github"
[Github Secrets]: https://cli.github.com/manual/gh_secret "Use gh cli to set, list, and delete secrets"
[Gitlab Variables]: https://gitlab.com/gitlab-org/cli/-/tree/main/docs/source "Use the gitlab cli to add, remove, and list Gitlab Variables"
[Install the Bitwarden CLI]: https://bitwarden.com/help/cli/ "Visit the Bitwarden installation docs"
[Install the Gitlab CLI]: https://gitlab.com/gitlab-org/cli "Visit the Gitlab CLI docs"
[Install the Github CLI]: https://cli.github.com/ "Visit the Githubcli homepage"
