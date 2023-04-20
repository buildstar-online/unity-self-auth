# Using seleium to authorize Unity Engine "Personal" licenses

1. This project is a work-in-progres and is not considdered to be in a functional state for end-users.

2. An email + password is required to build the Docker container. I use [Bitwarden CLI] in my examples to handle secrets. You could also use [Github Secrets], [Gitlab Variables] etc...

- [Install the Bitwarden CLI]
- [Install the Github CLI]
- [Install the Gitlab CLI]

3. A GUI Dockerfile is provided for debugging but this really is meant to run in a pipeline as a headless process.


## Usage

1. Pick a Unity Editor Version and a Changeset

    This one can be trickey because Unity doesnt provide a =n easy way to fin this information. 
    There is a great community repo by [mob-sakai](ttps://github.com/mob-sakai) that you can user to     list that data here [mob-sakai/unity-changeset](https://github.com/mob-sakai/unity-changeset)

    - Install the package via NPM:

        ```bash
        npm install unity-changeset
        ```

    - List Unity Editor versions with changesets

        ```bash 
        unity-changeset list
        ```

3. Run the program 

    ```bash
    EDITOR_VERSION="2022.1.23f1"
    CHANGE_SET="9636b062134a"
    HUB_VERSION="3.3.0"
    USERNAME=""
    PASSWORD=""

    mkdir -p Downloads && \
    touch Downloads/Unity_v${EDITOR_VERSION}.alf && \
    docker run --rm -it -v $(pwd):/home/player1 \
        -v $(pwd)/Downloads/Unity_v${EDITOR_VERSION}.alf:/Unity_v${EDITOR_VERSION}.alf \
        --user 1000:1000 \
        deserializeme/gcicudaeditor:latest \
        unity-editor -quit \
        -batchmode \
        -nographics \
        -logFile /dev/stdout \
        -createManualActivationFile \
        -username "$USERNAME" \
        -password "$PASSWORD"

    docker run --rm -it -v $(pwd):/home/player1 \
        --user 1000:1000 \
        -v $(pwd)/config.json:/home/player1/config.json \
        -v $(pwd)/Downloads:/home/player1/Downloads \
        -e USERNAME="$USERNAME" \
        -e PASSWORD="$PASSWORD" \
        deserializeme/gcicudaselenium:latest \
        ./license.py Downloads/*.alf config.json
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
