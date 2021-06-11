## Compose sample application
### Python/Flask with Nginx proxy and MySQL database

Project structure:
```
.
├── docker-compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── nginx
    └── nginx.conf

```

[_docker-compose.yaml_](docker-compose.yaml)
```
services:
  backend:
    build: backend
    ...
  db:
    image: mysql:8.0.19
    ...
  proxy:
    build: proxy
    ...
```
The compose file defines an application with three services `proxy`, `backend` and `db`.
When deploying the application, docker-compose maps port 80 of the proxy service container to port 80 of the host as specified in the file.
Make sure port 80 on the host is not already being in use.

## Deploy with docker-compose

```
$ docker compose up -d
Creating network "nginx-flask-mysql_default" with the default driver
Pulling db (mysql:8.0.19)...
5.7: Pulling from library/mysql
...
...
WARNING: Image for service proxy was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker compose up --build`.
Creating nginx-flask-mysql_db_1 ... done
Creating nginx-flask-mysql_backend_1 ... done
Creating nginx-flask-mysql_proxy_1   ... done
```

## Expected result

Listing containers must show three containers running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED       STATUS                 PORTS                                                  NAMES
8a21aa87a357   a264a129f394   "nginx -g 'daemon of…"   3 hours ago   Up 3 hours             0.0.0.0:80->80/tcp, :::80->80/tcp                      foot_stats_compose_proxy_1
be0300a8c35a   f98372fea04f   "/bin/sh -c 'flask r…"   3 hours ago   Up 3 hours             0.0.0.0:5000->5000/tcp, :::5000->5000/tcp              foot_stats_compose_backend_1
2c595f4f72c1   0c27e8e5fcfa   "docker-entrypoint.s…"   3 hours ago   Up 3 hours (healthy)   33060/tcp, 0.0.0.0:6603->3306/tcp, :::6603->3306/tcp   foot_stats_compose_db_1


```

After the application starts, navigate to `http://localhost:80` in your web browser or run:
```
$ curl localhost:80

```

Stop and remove the containers
```
$ docker compose down
```
