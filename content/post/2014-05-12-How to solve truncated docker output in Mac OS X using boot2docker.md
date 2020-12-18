---
tags:
- howto
- macosx
date: '2014-05-12'
description: ''
keywords: []
title: How to solve truncated docker output in Mac OS X using boot2docker
aliases:
- /new/blog/how-to-solve-truncated-docker-output-in-mac-os-x-using-boot2docker
slug: how-to-solve-truncated-docker-output-in-mac-os-x-using-boot2docker
---


If you are using docker on Mac OS X using boot2docker (<a href='http://docs.docker.io/installation/mac/'>http://docs.docker.io/installation/mac/</a>), you may see truncated output from `docker run`, and also may have noticed that `docker attach` does not work properly, producing only some output and then exiting. This bug is documented here: <a href='https://github.com/boot2docker/boot2docker/issues/150'>https://github.com/boot2docker/boot2docker/issues/150</a>, where I also found the following workaround. Documenting it here in case anyone finds it useful:


Instead of using the default value of `DOCKER_HOST` provided by `boot2docker up`, establish the docker connection through an ssh tunnel:


```
    $ boot2docker ssh -L 14243:127.0.0.1:4243 -N
    docker@localhost's password: <type password>
    [press Ctrl-z to suspend the command]
    $ bg
    $ export DOCKER_HOST=localhost:14243
```


Now all docker connections will go through the ssh tunnel instead of through VirtualBox port forwarding, and things will work fine.




