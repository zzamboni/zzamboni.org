# Hugo Boilerplate

## [Demo](http://enten.github.io/hugo-boilerplate/)

## Requirements

* [git](http://git-scm.com)
* [hugo](https://gohugo.io)
* [node](https://nodejs.org)
* [npm](https://www.npmjs.com/about)

## Installation

```bash
git clone https://github.com/enten/hugo-boilerplate awesome-site
```

## Configuration

```bash
# change directory to your awesome site
cd awesome-site

# building configuration
vi config.toml

# ftp deployement configuration
echo '{
  "host": "ftp.example.com",
  "port": 21,
  "dest": "/www",
  "username": "*****",
  "password": "*****"
}' > ./scripts/ftp-config.json
vi scripts/ftp-config.json
```

## Workflow

```bash
# change directory to your awesome site
cd awesome-site

# one script to rule them all..
./scripts/losh

NAME:
    losh - Lord of the shell scripts (one script to rull them all)

VERSION:
    0.0.2

USAGE:
    losh [command] [arg...]

COMMANDS:
    losh build [hugo options...]
                Build site into <root>/public
    losh deploy [hugo options...]
                Build and deploy on remote server
    losh deploy-gh [hugo options...]
                Build and deploy on Github Pages
    losh server [hugo options...]
                Build site and run test server
    losh update-losh
                Update losh
    losh [?|h|help]
                Print this help message


```
