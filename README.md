# Using seleium to authorize Unity Engine "Personal" licenses (WiP)

- Create a unity `ALF` then convert it to a `ULF` file automatically. 
- Save your license file as a repo secret.
- Built with Docker so it can be easily run on your local machine or in a pipeline.
- Works with the standard GameCI Editor images on [Dockerhub](https://hub.docker.com/r/unityci/editor/tags)

## This project is a work in-progress, specifically regarding:
- Documentation is still being actively tested for accuracy
- Tests for the python code still need to be written
- Rotating the License automatically via Github Actions is still in testing due to challenges properly obscuring sensitive data in the worflow logs.
- Selenium script uses explicit sleep/wait calls between page loads which need to be replaces with some smarter "while/until" logic.

## Known Issues:
- ULF file creation will fail if login is blocked by a 2factor challange. Running from a machine in a region other than the one you have chosen for your unity account will trigger such an event. 

  > For example, running this on my Hetzner machine in Germany fails because Unity security blocks the login, but runs successfully from a local machine. Github hosted runners are all geolocated in the USA, which will trigger the same issue for non-US residents.

## Running in a pipeline:

1. Choose an editor image from GameCi's [Dockerhub](https://hub.docker.com/r/unityci/editor/tags), or bring your own.

    <img width="1491" alt="Screenshot 2023-04-23 at 15 33 11" src="https://user-images.githubusercontent.com/84841307/233842940-050d475f-2ce6-406e-a2d5-a54d17f8db9c.png">

2. Copy and add the [example workflow](https://raw.githubusercontent.com/cloudymax/unity-self-auth/main/.github/workflows/example-licenses-pipeline.yml) to your own repo.

4. Add the following secrets to the repo:
  - `UNITY_USERNAME`: The email address or username for your Unity account
  - `UNITY_PASSWORD`: Password for your Unity account.
  - `PAT`: A personal access token that will be used to store the license as a repo secret.

3. Run the workflow with your desired Editor Image and Editor Version (leave the selenium image as is).

    <img width="375" alt="Screenshot 2023-04-23 at 15 33 43" src="https://user-images.githubusercontent.com/84841307/233842892-349c1318-eb9e-4942-aacb-01f29b8107b2.png">

## Run from the command line
```bash
# Create a temporary directoy to work in
mkdir -p /tmp/scratch
cd /tmp/scratch

# Export important variables
EDITOR_VERSION="2022.1.23f1"
EDITOR_IMAGE="deserializeme/gcicudaeditor:latest"
SLENIUM_IMAGE="deserializeme/gcicudaselenium:latest"
USERNAME="YOUR_EMAIL_HERE"
PASSWORD="YOUR_PASSWORD_HERE"

# Change ownership of local dir so the container user can save data to mounted volumes
chown 1000:1000 .
touch Unity_v${EDITOR_VERSION}.alf

# Generate the ALF file using the Editor 
docker run --rm -it -v $(pwd)/Unity_v${EDITOR_VERSION}.alf:/home/player1/Unity_v${EDITOR_VERSION}.alf \
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
    --mount type=bind,source="$(pwd)",target=/home/player1/unity-self-auth/Downloads \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="True" \
    $SLENIUM_IMAGE \
    ./license.py ../Downloads/Unity_v${EDITOR_VERSION}.alf
```

## You can also run graphical session over VNC if desired

```bash
docker run --rm -it --mount type=bind,source="$(pwd)",target=/home/player1/Downloads \
    --user 1000:1000 \
    -p 5900:5900 \
    -e USERNAME="$USERNAME" \
    -e PASSWORD="$PASSWORD" \
    -e HEADLESS="False" \
    deserializeme/gcicudaseleniumxfce:latest \
    x11vnc --loop --create
```

## Testing activation

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


