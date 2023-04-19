# Setup Jenkins in docker on a local server

### Install Jenkins
1. Install docker - the easiest way to do this is from a script supplied by 
docker themselves - see https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script
and remove the dry-run flag once you're ready

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh --dry-run
```

2. Docker without sudo
    - Add the docker group
    - add the current user to the group

```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
```

log out and log back in before carrying on.

3. Check Docker works
```bash
docker run hello-world
```

4. Pull the dockerimage

```bash
docker pull jenkins/jenkins
```

5. Create a specific network for Jenkins to be in

```bash
docker network create jenkins
```

6. Start a new jenkins container
```bash
docker run -d --name jenkins \
  --network jenkins \
  -p 8080:8080 \
  -p 22:22 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins
```

Verify this with `docker ps`

7. In a web browser, direct to `http://IP_ADDR:8080`

### Setup Jenkins
1. Admin password - Run `docker logs jenkins` to get the password from the logs
2. Install suggested plugins
3. Follow the rest of the setup
4. Create a new Job and follow instructions
5. To use an SSH link to a repo, you need to create a custom SSH key and upload 
the private key to jenkins
    - `docker exec -ti jenkins bash` to enter the container
    - `ssh-keygen -t ed25519` to generate a key pair
    - add the public key to github
    - `ssh-keyscan github.com >> ~/.ssh/known_hosts` in the container tty to 
    add the github host key
