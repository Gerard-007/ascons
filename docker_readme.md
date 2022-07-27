### Basic dockr commands

* download package from docker
`docker pull name`

* Display docker images
`docker images`

* Running an image to a container
`docker run image:tag` <!--  please dont do this it may hang -->

* Running an image to a container in detached mode
`docker run -d image:tag`

* Display all running container
`docker container ls`
`docker ps`

* Stopping running docker container
`docker stop container ID`

* Mapping port from 8080 to 80
`docker run -d -p  8080:80 image:tag`

* Mapping two ports to image port
`docker run -d -p 8080:80 -p 3000:80 image:tag`

* Stopping running containers
`docker stop <container id> or <container name>`

* List all container both used and unused containers
`docker ps --all` or `docker ps -a`
`docker ps -aq` <!-- displays onliy list of containers id -->
`docker rm $(docker ps -a)` <!-- deletes all containers except running containers -->
`docker rm -f $(docker ps -a)` <!-- deletes all containers including running containers -->

* Remove container
`docker rm <container id> or <container name>`

* Naming a container with <--name website>
`docker run --name website -d -p 8080:80 -p 3000:80 image:tag`
`docker stop website` <!-- stops cntainer -->
`docker start website` <!-- starts container -->

### VOLUME in Docker
<!-- This helps us to share files between host and container -->
<!-- docker run <name> <volume from:to:read only> <-d> <-p 9000:80> <image:tag> -->
`docker run --name nginx -v $(pwd):/usr/share/nginx/html:ro -d -p 9000:80 nginx`

### VOLUME copy from one container to another
`docker run --name websitecopy --volumes-from website -d -p 8000:80 nginx`

* Formatting docker container list display
### Example
`docker ps --format="ID\t{{.ID}}\nNAME\t{{.Names}}\nIMAGE\t{{.Image}}\nPORTS\t{{.Ports}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.CreatedAt}}\nSTATUS\t{{.Status}}"` <!--Excempts running container -->
`docker ps -a --format="ID\t{{.ID}}\nNAME\t{{.Names}}\nIMAGE\t{{.Image}}\nPORTS\t{{.Ports}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.CreatedAt}}\nSTATUS\t{{.Status}}"` <!--includes non running containers -->

* Running contianer bash shell
`docker exec -it <container name> bash`


* Building Image
`docker build --tag website:latest .`

* Remove docker image
`docker image rm <IMAGE ID>`

* Removing <none> dangling image
`docker rmi $(docker images -f "dangling=true" -q)`

* Pulling Alpine Image version (low sized image)...
`docker pull <image>:alpine`

* Install multiple node packages...
`npm i -S react webpack gulp grunt`

* Updating to latest using tag.
`docker tag <latest-image>:<tag> <new-image>:<new tag>`

* Pushing images to docker repo...
1 `docker tag <Image>:<tag> <username>/<Image>:<tag>`
2 `docker push <username>/<Image>:<tag>`

* To Inspect a container
`docker inspect <Container-ID> or <container name>`

* To view container logs
`docker logs <Container-ID> or <container name>`

* Execute command line
`docker exec it <container name> <shell dir>`