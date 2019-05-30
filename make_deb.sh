#!/bin/bash

# Requires: apt-get install libmysqlclient-dev libffi-dev python-dev libjpeg-dev
CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LAST_COMMIT_HASH=`git rev-parse HEAD`

rm -Rf debian/usr/
rm -Rf debian/etc/

mkdir -p debian/usr/share/openalpr-hotlist/
mkdir -p debian/etc/openalpr/
mkdir -p debian/etc/cron.d/


mkdir -p debian/usr/share/openalpr-hotlist/parsers
cp $CUR_DIR/hotlistimport.py debian/usr/share/openalpr-hotlist/
cp $CUR_DIR/print_alert_lists.py debian/usr/share/openalpr-hotlist/
cp $CUR_DIR/parsers/*.py debian/usr/share/openalpr-hotlist/parsers/
cp $CUR_DIR/config/hotlist.yaml.sample debian/etc/openalpr/hotlist.yaml.sample
cp $CUR_DIR/deploy/openalpr-hotlistimport.cron  debian/etc/cron.d/openalpr-hotlist
chmod 644 debian/etc/cron.d/openalpr-hotlist

# Insert the git hash into settings.py
echo "$LAST_COMMIT_HASH" > debian/usr/share/openalpr-hotlist/githash

VERSION=`dpkg-parsechangelog -ldebian/DEBIAN/changelog --show-field Version`
VERSION_WITHOUT_BUILD=`echo $VERSION | sed 's/\-.*$//'`
#Swap in a build number based on the current date/time.
if [ -z "$BUILD_NUMBER" ]; then
    BUILD_NUMBER=`date "+%Y%m%d%H%M%S"`
fi
VER_WITH_BUILD="${VERSION_WITHOUT_BUILD}-${BUILD_NUMBER}"
sed -i "s/$VERSION/$VER_WITH_BUILD/" debian/DEBIAN/changelog
sed -i "s/^Version:.*/Version: $VER_WITH_BUILD/" debian/DEBIAN/control

fakeroot dpkg-deb --verbose --build debian || exit 1

DEB_FILE=openalpr-hotlist_${VER_WITH_BUILD}.deb

mkdir -p out/

mv debian.deb out/$DEB_FILE || exit 1


