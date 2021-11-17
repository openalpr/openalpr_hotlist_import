# Hotlist Import Artifact Builder
The Dockerfile included in this folder can be used to build release artifacts from any machine where Docker installed.
Built artifacts will be available outside the build container for distribution.

## Setup
- Install Docker
  - https://docs.docker.com/get-docker/
- Build the builder image
  - At the root of the repository, run
    - `cd builder`
    - `docker build -t hotlist_import_builder .`

## Versioning
- If you need to make an official version, do this beforehand!!

in ./installer.cfg
```
[Application]
name=OpenALPR Hotlist Import
version=1.2.2   <- from 1.2.1
```

in ./debian/control
```
Package: openalpr-hotlistimport
Version: 1.2.2    <- from 1.2.1-20210119085126
Section: web
```

in ./debian/changelog
```
openalpr-hotlistimport (1.2.2) unstable; urgency=low

  * Add Kansas Topeka PD parser

 -- Addison Klinke <addison@openalpr.com>  Tue, 27 Sept 2021 00:00:00 +0000
```

## Build the artifacts
- At the root of the repository, run
  - `docker run --rm -it -v$(pwd):/hotlist_import hotlist_import_builder`
    - this will mount the entire repository into the container
  - `cd /hotlist_import`
    - this will place you in the root of the repository folder

You are now in the build container ready to build the artifacts.

## Create the .deb package:
Inside a `hotlist_import_builder` container:
- `cd /hotlist_import`
- `./make_deb.sh`

Debian package should be out on `{project_root}/out/openalpr-hotlist_{{version}}.deb`

## Create the .exe package:
Inside a `hotlist_import_builder` container:
  - `cd /hotlist_import`
  - `./build_installer.sh`

Windows package should be out on `{project_root}/build/nsis/OpenALPR_Hostlist_Import_{{version}}.exe`

