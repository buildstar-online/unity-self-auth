# Using seleium to authorize Unity Engine "Personal" licenses

**This project is a work in progress**

1. You will likely encounter issues with ULF file creation if running from a machine in a region other than the one you have chosen for your unity account. For example, running this on my Hetzner machine in Germany fails because Unity security blocks the login, but runs successfully from a local machine. Github hosted runners are all geolocated in the USA, which will trigger the same issue for non-US residents.

2. Regualr GameCI images are not yet supported.
 
3. Only Editor-Version `2022.1.23f1` is supported at the moment
 
## ALF file creation

Uses the Unity Editor to create .alf file and save it in the Downloads/ folder.

```bash
EDITOR_VERSION="2022.1.23f1"
CHANGE_SET="9636b062134a"
HUB_VERSION="3.3.0"
EDITOR_IMAGE="deserializeme/gcicudaeditor:latest"
SLENIUM_IMAGE="deserializeme/gcicudaselenium:latest"
USERNAME=""
PASSWORD=""

docker pull $EDITOR_IMAGE
docker pull $SLENIUM_IMAGE

mkdir -p Downloads && \
touch Downloads/Unity_v${EDITOR_VERSION}.alf && \
docker run --rm -it -v $(pwd):/home/player1 \
    -v $(pwd)/Downloads/Unity_v${EDITOR_VERSION}.alf:/Unity_v${EDITOR_VERSION}.alf \
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
 
```bash
docker run --rm -it --user 1000:1000 \
    -p 5900:5900 \
    --mount type=bind,source="$(pwd)"/Downloads,target=/home/player1/unity-self-auth/Downloads \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    $SLENIUM_IMAGE \
    /bin/bash
```
 
```bash
docker run --rm -it --mount type=bind,source="$(pwd)"/Downloads,target=/home/player1/unity-self-auth/Downloads \
    --user 1000:1000 \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    deserializeme/gcicudaselenium:xfce\
    /bin/bash
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
