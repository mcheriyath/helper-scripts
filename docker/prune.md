#### Cleanup exited processes:

```docker rm $(docker ps -q -f status=exited)```

#### Cleanup dangling volumes:

```docker volume rm $(docker volume ls -qf dangling=true)```

#### Cleanup dangling images:

```docker rmi $(docker images --filter "dangling=true" -q --no-trunc)```

