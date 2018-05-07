List all the init scripts related to docker
```
root@amqp1-c1:~# systemctl list-unit-files | grep -i docker
docker-container@ecs-agent.service         enabled
docker.service                             enabled
docker.socket                              enabled
```

Disable all the docker services from startup
```
root@amqp1-c1:~# systemctl disable docker.socket
Removed symlink /etc/systemd/system/sockets.target.wants/docker.socket.
root@amqp1-c1:~# systemctl list-unit-files | grep -i docker
docker-container@ecs-agent.service         enabled
docker.service                             enabled
docker.socket                              disabled
root@amqp1-c1:~# systemctl disable docker.service
Synchronizing state of docker.service with SysV init with /lib/systemd/systemd-sysv-install...
Executing /lib/systemd/systemd-sysv-install disable docker
insserv: warning: script 'sethosts' missing LSB tags and overrides
insserv: warning: current start runlevel(s) (empty) of script `docker' overrides LSB defaults (2 3 4 5).
insserv: warning: current stop runlevel(s) (0 1 2 3 4 5 6) of script `docker' overrides LSB defaults (0 1 6).
insserv: warning: script 'sethosts' missing LSB tags and overrides
root@amqp1-c1:~# systemctl disable docker-container@ecs-agent.service
Removed symlink /etc/systemd/system/default.target.wants/docker-container@ecs-agent.service.
```

List the status of the init scripts after disabling the docker services.
```
root@amqp1-c1:~# systemctl list-unit-files | grep -i docker
docker-container@ecs-agent.service         disabled
docker.service                             disabled
docker.socket                              disabled
```
