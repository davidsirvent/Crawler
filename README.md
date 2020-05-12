<img src="https://github.com/xiribyte/Crawler/blob/master/crawler.png?raw=true" height="128px" alt="Crawler logo">

(Web) Crawler
=============

(Web) Crawler is a python script that (as you can imagine) crawl info from a web. The crawler extract (if available) title, description and all anchors storing in a sqlite database. If requested, the crawling is recursive on found Urls.

```
usage: crawler.py [-h] [-v] [-t SECONDS] [-n] [-r] [-e filename.csv]
                  [-d database.db] [-i]
                  url_list

positional arguments:
  url_list              Text file containing URLs to crawl. One per line.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Shows crawling info
  -t SECONDS, --timeout SECONDS
                        Timeout for non-responding requests (default: 5 seg).
  -n, --not-only-onion  Allow to crawl in not .onion domains.
  -r, --recursive       Performs recursive crawling on found URLs.
  -e filename.csv, --export filename.csv
                        File name to save crawling results in CSV format.
  -d database.db, --database database.db
                        Specifies name for database (.db) file to store
                        crawling results (default: database.db).
  -i, --init-db         Initialize an empty DB. Could be used to erase data
                        from an existing DB.
```


