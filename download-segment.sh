#!/usr/bin/env bash
CHAP_FILE="$1.txt"
TOT_LENGTH=0
DOWNLOADS=""

if [ -f .ln ]; then
	LINENUM=$(cat .ln)
else
	LINENUM=0
fi

tail -n +"$LINENUM" "$CHAP_FILE" | \
while read line; do
	((LINENUM++))
	echo "Downloading $line"
	uri=$(python3 mp3-geturi.py $(echo "$line" | xargs))
	FN=$(echo "$line" | tr -d '[:space:]')".mp3"
	curl "$uri" -o "$FN"
	DOWNLOADS="$DOWNLOADS $FN"
	echo "$DOWNLOADS"
	LENGTH=$(mp3info -p "%S" "$FN")
	((TOT_LENGTH+=LENGTH))
	if (( TOT_LENGTH > 1800 )); then
		echo "$LINENUM" > .ln
		echo "Adding new files to RSS feed"
		./add_item.py $1$DOWNLOADS
		break
	fi
done

