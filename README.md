# Using seleium to authorizue untiy personal licenses

WIP project for a game jam
____________________________________________________

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
    docker build --build-arg USERNAME=someuser \
    --build-arg PASSWORD=somepassword \
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
