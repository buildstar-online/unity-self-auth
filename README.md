# Using seleium to authorizue untiy personal licenses

WIP project for a game jam
____________________________________________________

## Usage

0. Pick a unity version


1. Build the docker file

```bash
docker build -t auther .
```

2. Run the program 

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
