# eclipse-release-command-line-tool

Command-line-tools for Eclipse related release. It allows to automatize release at Eclipse with `erclt.py`.

## Requirement

* Python 2.6

## Description

### erclt.py

It is the tool, which automatizes releases. So far, it is _only able to release milestones, and stable version (maintenance version not yet implemented)_.

#### Usage

```shell
# Release milestone v0.9RC2
$ ./erclt.py -m -mv 0.9RC2

# Release milestone v0.9RC2 as stable v0.9 
$ ./erclt.py -s -mv 0.9RC2 -sv 0.9

# Use custom path for local tests
$ ./erclt.py -d /tmp/copyofeclipsedir -m -mv 0.9RC2
```