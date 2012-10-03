# eclipse-release-command-line-tool

Command-line-tools for Eclipse related release. It allow to automatize release at Eclipse with `erclt.py` and to emultate Eclipse file tree with `check.py`.
The delivery process implemented is descibed on the [LDT wiki](http://wiki.eclipse.org/Koneki/Development#Milestones_versions).

## Requirement
* Python > 2.5 (2.7 is recommended)

## Description

### erclt.py

It is the tool, which automatize releases. So far, it is _only able to release milestones_.

#### Usage

```shell
$ ./erclt.py -ap /tmp/tmpCzuqtS/artifactpath  -nv 1.0 -ov 0.8  -d /tmp/copyofeclipsedir -m
```
```help
usage: erclt.py [-h] -ov version_number -nv version_number [-d dir]
                [-ap [path_to_artifacts]] (-m | -r)

Helps release an Eclipse based product.

optional arguments:
  -h, --help            show this help message and exit
  -ov version_number, --oldversion version_number
                        New version number, the one being released.
  -nv version_number, --newversion version_number
                        Previously released version number, used for archiving
                        it.
  -d dir, --directory dir
                        All directories used will be relative to this one,
                        defaults to `./`.
  -ap [path_to_artifacts], --artifactspath [path_to_artifacts]
                        Path to the artifacts to release, often last sucessful
                        build form continuous integration.
  -m, --milestone       Indicates that a milestone sould be delivred.
  -r, --release         Indicates that a release sould be delivred.

So far only milestones are implemented.
```

### check.py

As `erclt.py` is supposed to deploy an artifact zip accross a specific file tree, `check.py` script recreate this arborescense in a local tmp folder. The created arborescense can be filled with the _last artifact from Eclipse contiuous integration_ downloded in the nigtly folder.

#### Usage

```shell
# This will download last artifact
$ ./check.py
```
or
```help
usage: check.py [-h] [-a [artifacts_zip_path]]

Create the files properly to run deploy script.

optional arguments:
  -h, --help            show this help message and exit
  -a [artifacts_zip_path], --artifacts [artifacts_zip_path]
                        Artifacts zip file path
```
