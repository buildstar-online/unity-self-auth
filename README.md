# Using seleium to authorize Unity Engine "Personal" licenses

very much WIP
____________________________________________________

!: this project requires an email + password. I will use [Bitwarden CLI] in my examples but since this really is meant to run in a pipeline, using a [Github Secret], [Gitlab variable] etc... is strongly advised.

- [Install the Bitwarden CLI]
- [Install the Github CLI]
- [Install the Gitlab CLI]



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


2. Build the docker container

    The dockerfile takes a username and password as build args, which are used to create the .alf file we need to request a license.
    
    ```bash
    docker build --build-arg USER_NAME=$(bw get username unity3d-login) \
    --build-arg PASSWORD=$(bw get password unity3d-login) \
    --build-arg EDITOR_VERSION="2022.1.23f1" \
    --build-arg CHANGE_SET="9636b062134a" \
    --build-arg HUB_VERSION="3.3.0" \
    -t auther .
    ```

3. Run the program 

    ```bash
    docker run -it auther python3 license.py ~/*alf ../config/template_config.json
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
[Github Secret]: https://cli.github.com/manual/gh_secret "Use gh cli to set, list, and delete secrets"
[Gitlab Variable]: https://gitlab.com/gitlab-org/cli/-/tree/main/docs/source "Use the gitlab cli to add, remove, and list Gitlab Variables"
[Install the Bitwarden CLI]: https://bitwarden.com/help/cli/ "Visit the Bitwarden installation docs"
[Install the Gitlab CLI]: https://gitlab.com/gitlab-org/cli "Visit the Gitlab CLI docs"
[Install the Github CLI]: https://cli.github.com/ "Visit the Githubcli homepage"
