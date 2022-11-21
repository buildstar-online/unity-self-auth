# Using seleium to authorizue untiy personal licenses

WIP project for a game jam
____________________________________________________

## Usage

1. How to pick a Unity Editor Version and a Changeset

This one can be trickey because Unity doesnt provide a =n easy way to fin this information. 
There is a great community repo by [mob-sakai](ttps://github.com/mob-sakai) that you can user to list that data here [mob-sakai/unity-changeset](https://github.com/mob-sakai/unity-changeset)

Install the package via NPM:

```bash
npm install unity-changeset
```

List Unity Editor versions with changesets

```bash
unity-changeset list
```

Now edit the Dockerfile to use the values you want


2. Build the docker file

```bash
docker build -t auther .
```

3. Run the program 

```bash
docker run -it auther license.py Unity_v2020.3.10f1.alf config/config.json

python3 script <path/to/file.alf> <path/to/config.json>
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
