#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd "$DIR"
./download-segment.sh bofm
git add bofm/*.mp3
git add rss/bofm.rss
git commit -m "daily update of bofm"
git push
popd
