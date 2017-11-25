#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CHAP_FILE="$1/$1.txt"
TOT_LENGTH=0
LINE_CACHE="$1/.ln"
DOWNLOADS=""

if [ -f "$LINE_CACHE" ]; then
	LINENUM=$(cat "$LINE_CACHE")
else
	LINENUM=1
fi

tail -n +"$LINENUM" "$CHAP_FILE" | \
while read line; do
	((LINENUM++))
	echo "Downloading $line"
	uri=$(python3 mp3-geturi.py $(echo "$line" | xargs))
	FN=$(echo "$line" | tr -d '[:space:]')".mp3"
	curl "$uri" -o "$1/$FN"
	DOWNLOADS="$DOWNLOADS $FN"
	LENGTH=$(mp3info -p "%S" "$1/$FN")
	((TOT_LENGTH+=LENGTH))
	if (( TOT_LENGTH > 1800 )); then
		echo "$LINENUM" > "$LINE_CACHE"
		echo "Adding new files to RSS feed"
		./add_item.py $1$DOWNLOADS
		break
	fi
done
