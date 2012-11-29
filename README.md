# eclipse-release-command-line-tool

Command-line-tools for Eclipse related release. It allows to automatize release at Eclipse with `erclt.py` and to emultate Eclipse file tree with `check.py`.

## Requirement

* Python 2.6

## Description

### erclt.py

It is the tool, which automatizes releases. So far, it is _only able to release milestones_.

#### Usage

```shell
$ ./erclt.py -nv 1.0 -ov 0.8 -d /tmp/copyofeclipsedir -m
```

### check.py

`erclt.py` is supposed to deploy artifacts and products archives accross a specific file tree, `check.py` recreates this arborescense. It is also able to _download last artifacts and products from Eclipse contiuous integration_.

#### Usage

```shell
# This will download last artifact
$ ./check.py
```
or
```shell
# This will deploy given artifact, /d/koneki.ldt contains LDT sources.
$./check.py -p /d/koneki.ldt/product/target/products/*.tar.gz -a /d/koneki.ldt/product/target/repository.zip
```
