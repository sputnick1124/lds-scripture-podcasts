# LDS Scripture Podcast with Daily Downloads
This provides a method to integrate scripture audio downloaded from [lds.org](lds.org/scriptures) into a podcast feed. Currently 
supports Book of Mormon, but there is no barrier to supporting all of the standard works.

## Adding to your podcast feed
Point your podcast to the rss feed located at:
`https://raw.githubusercontent.com/sputnick1124/lds-scripture-podcasts/master/rss/bofm.rss`
and it should behave just like a normal podcast.

## How it works
RSS is dead simple. Add a channel, put items in the channel, and point an RSS reader at the right spot. Knowing this, we just take
advantage of the (limitless?) storage that Github gives its users and automate the add/commit/push process to set up an automatic
podcast. Using BeautifulSoup, we scrape the chapter we want for the MP3 download tag and print the uri link to terminal. Digest
this link with `curl` to download the file. Repeat the process until all of the new files' lengths exceed 30 minutes and send the
names to another python script. This script parses the RSS file (using `xml.etree`), formats new item elements, and appends them to
the channel element. Once this is all done, add the new MP3s and the updated RSS file to the repo, commit and push. This process is
done every weekday at midnight (the idea being that the best time to digest the process is during your weekday commute).
