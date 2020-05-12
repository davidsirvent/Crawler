<img src="https://github.com/xiribyte/Crawler/blob/master/crawler.png?raw=true" height="128px" alt="Crawler logo">

(Web) Crawler
=============

(Web) Crawler is a python script that (as you can imagine) crawl info from a web. The crawler extracts (if available) title, description and all anchors, storing it in a sqlite database. If requested, the crawling is recursive on found Urls.

I started this script because I became tired of 'Tor wikis', 'Hidden wikis' and 'Onion links' with almost all his links broken. So I decided to crawl by my own. As a result this script is able to crawl recursively and store URL, title and description on a sqlite database which could be queried later. In addition, CSV export and custom database name features were added.

Before first use:

* (Optional) Configure a **virtual environment** like venv or virtualenv.
* Clone (or download) repository:
```
   git clone https://github.com/xiribyte/Crawler.git
```
* Install requirements:
```
   pip3 install -r requirements.txt
```

***

Built-in help menu:
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

***
F. A. Q.
--------
<dl>
  <dt>Is there a ready-to-run command for lazy hackers?</dt>
  <dd><code>python3 crawler.py -ri url_list.txt</code></dd>
  <dt>Why <code> --not-only-onion </code> option?</dt>
  <dd>All of this started for specifically crawl into onion sites, clearnet option (<code>--not-only-onion</code>) was added later.</dd>
  <dt>Always get <code> 'no such table: urls' </code> message.</dt>
  <dd>When using a database file for first time, you need to invoke <code> --init-db </code> feature.</dd>
  <dt>I'm unable to crawl any .onion site.</dt>
  <dd>
    <ul>
      <li>First, check that url_list.txt is well formed: One url per line, must include 'http://' or 'https://.</li>
      <li>Second, ensure you are behind a Tor node (anonsurf or nipe.pl do the trick).</li>
      <li>Third, try to increase timeout.</li>
    </ul>
  </dd>
  <dt>This really works?</dt>
  <dd>As a sample, you can find a full database of onion sites crawled on [Torlinks](https://github.com/xiribyte/torlinks) repository.</dd>
</dl>



