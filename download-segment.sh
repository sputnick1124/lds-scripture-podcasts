#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CHAP_FILE="$1/$1.txt"
TOT_LENGTH=0
LINE_CACHE="$1/.ln"
LINE_CNT=$(wc "$CHAP_FILE" | awk '{$1=$1};1' | cut -d" " -f1)

if [ -f "$LINE_CACHE" ]; then
	LINENUM=$(cat "$LINE_CACHE")
else
	LINENUM=1
fi

if ((LINENUM>=LINE_CNT)); then
	LINENUM=1
fi

tail -n +"$LINENUM" "$CHAP_FILE" | \
while read line; do
	((LINENUM++))
	echo "Downloading $line"
	uri=$(python update-podcast.py $(echo "$line" | cut -d" " -f1,2 | xargs))
	LENGTH=$(echo "$line" | cut -d" " -f3)
	((TOT_LENGTH+=LENGTH))
	if (( TOT_LENGTH > 1800 )); then
		echo "Adding new files to RSS feed"
		break
	fi
	echo "$LINENUM" > "$LINE_CACHE"
done
