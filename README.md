# eclipse-release-command-line-tool

Command-line-tools for Eclipse related release. It allow to automatize release at Eclipse with `erclt.py` and to emultate Eclipse file tree with `check.py`.

## Requirement
* Python > 2.5 (2.7 is recommended)

## Description

### erclt.py

It is the tool, which automatize releases. So far, it is _only able to release milestones_.

#### Usage

```shell
$ ./erclt.py -ap /tmp/tmpCzuqtS/artifactpath  -nv 1.0 -ov 0.8  -d /tmp/copyofeclipsedir -m
```

### check.py

`erclt.py` is supposed to deploy an artifact zip accross a specific file tree, this script recreate this arborescense. It is also able to _download last artifact from Eclipse contiuous integration_.

#### Usage

```shell
# This will download last artifact
$ ./check.py
```
or
```shell
# This will deploy given artifact
$ ./check.py -a /tmp/path/toartifact.zip
```
