# Hugo Boilerplate

## Requirements

* [git](http://git-scm.com)
* [hugo](https://gohugo.io)
* [node](https://nodejs.org)
* [npm](https://www.npmjs.com/about)

## Installation

```bash
git clone --recursive https://github.com/enten/hugo-boilerplate awesome-site
```

## Configuration

```bash
# change directory to your awesome site
cd awesome-site

# building configuration
vi config.toml

# ftp deployement configuration
vi scripts/ftpconfig.json
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
    losh build
                Build site into <root>/public
    losh deploy
                Build and deploy on remote server
    losh server
                Build site and run test server
    losh update-losh
                Update losh
    losh [?|h|help]
                Print this help message


```
