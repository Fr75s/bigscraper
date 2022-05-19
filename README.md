# bigscraper

Bigscraper is a metadata scraper for launchbox. It directly scrapes launchbox's website, as in, it finds the games needed and gets metadata through reading the Launchbox website content.

To use bigscraper, [check out the tutorial](USAGE.md)

## How it works

Bigscraper directly downloads the contents of Launchbox's game database website. It reads these contents, and attempts to find matches for the games that are being scraped for. If it finds them, then it gets the content of the games' details and images pages through reading their respective sites.

The above reveals why this is **big**scraper. As bigscraper needs to download many pages for launchbox, as well as downloading all the images, bigscraper requires a good internet connection and plenty of storage. Many games on the launchbox database have many different images, which quickly fill up storage.  **Do not use bigscraper if you have a poor internet connection or low storage.**
