""" Web Crawling """

import argparse
import requests
import datetime
import sqlite3
from sqlite3 import Error
from requests import urllib3
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup

# Request timeout
_TIMEOUT = 5

# Not only onion domains flag
_NOT_ONLY_ONION = False

# File to export results
_EXPORT = None

# Database file
_DATABASE = None

# Verbose
_VERBOSE = False

# Disable insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class database:
    """ Database handling """

    # Database file
    _DATABASE = "database.db"

    # Return values for save()
    updated = "updated"
    inserted = "inserted"

    def __init__(self, database: str = None):
        if database is not None:
            _DATABASE = database

    def connect(self):
        """Database connection"""

        try:
            con = sqlite3.connect(_DATABASE)
            return con
        except Exception as e:
            print("ERROR on DB connection:")
            print(" " + str(e))
            print("* * * * * * * * * * * * * * * *")


    def _init_db(self):
        """ Init DB """

        con = self.connect()
        cursor = con.cursor()

        cursor.execute("DROP TABLE IF EXISTS urls")
        cursor.execute(
            """
            CREATE TABLE urls(
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT,
                description TEXT,
                last_date TEXT NOT NULL
            );
            """
        )

        con.commit()
        con.close()


    def get_list(self, ):
        """ Get URL list """

        con = self.connect()
        cursor = con.cursor()

        cursor.execute("SELECT url FROM urls")
        rows = cursor.fetchall()

        con.close()
        
        return rows


    def save(self, url: [str]):
        """ Save URL on database """
        # url[0]: url
        # url[1]: title
        # url[2]: description
        # url[3]: last_date

        return_value = ""

        con = self.connect()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM urls WHERE url = '{0}';".format(url[0]))
        rows = cursor.fetchall()

        if len(rows) > 0:
            cursor.execute(
                "UPDATE urls SET title='{0}', description='{1}', last_date='{2}' WHERE url='{3}';".format(
                    url[1], url[2], url[3], url[0]
                )
            )
            return_value = self.updated

        else:
            cursor.execute(
                "INSERT INTO urls(url, title, description, last_date) VALUES ('{0}','{1}','{2}', '{3}');".format(
                    url[0], url[1], url[2], url[3]
                )
            )
            
            return_value = self.inserted

        con.commit()
        con.close()

        return return_value


def crawl(url_list: []):
    """ Web Crawling for a given URL array """

    url_list_parsed = []
    for item in url_list:        
        url_list_parsed.append(item[0])

    crawled_urls = []
    for url in url_list_parsed:
        try:
            r = requests.get(url, verify=False, timeout=_TIMEOUT)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")

                for link in soup.find_all("a"):
                    href = link.get("href")

                    if href.startswith('/'):
                        if url.endswith('/'):
                            href = url[:-1] + href
                        else:
                            href = url + href

                    # URL form checking
                    split_href = urlsplit(href)                    
                    well_formed = False
                    if "http" not in split_href.scheme:
                        well_formed = False
                    elif not _NOT_ONLY_ONION and not split_href.netloc.endswith(".onion"):                        
                        well_formed = False
                    else:
                        well_formed = True

                    # Test reachable
                    if well_formed == True:
                        try:
                            r_test = requests.get(href, verify=False, timeout=_TIMEOUT)

                            if r_test.status_code == 200:
                                msg("Found URL: Well formed and reachable\n         : {0}\n - - - - - - - - - - - - - - - - - - - - - -".format(href), 'o')
                                
                                soup_test = BeautifulSoup(r_test.text, "html.parser")                                

                                title_tag = soup_test.head.find("title")          
                                if title_tag is None:
                                    title = ""
                                else:
                                    title = title_tag.contents[0]
                                    title = title.replace("'","''") # TODO Change quotes parsing

                                description_tag = soup_test.head.find(name='meta', attrs={'name':'description'})
                                if description_tag is None:
                                    description = ""
                                else:
                                    description = description_tag.get('content')
                                    description = description.replace("'","''") # TODO change quotes parsing

                                last_date = datetime.datetime.now().now().strftime("%Y-%m-%d")
                                
                                candidate_url = [href, title, description, last_date]
                                
                                if _EXPORT is not None:                              
                                        export_csv(candidate_url)

                                db = database(_DATABASE)
                                if db.save(candidate_url) == db.inserted:                                    
                                    crawled_urls.append(candidate_url)                                    

                                
                                


                        except TimeoutError:
                            msg("ERROR: " + " is not responding\n     : {0}\n - - - - - - - - - - - - - - - - - - - - - - ".format(href), 'x')
                            
                        except Exception as General_Error:
                            msg("ERROR: URL generated a general error...\n     : {0}\n     : {1}\n - - - - - - - - - - - - - - - - - - - - - - ".format(href, str(General_Error)), 'x')
                            
                    else:
                        msg("ERROR: not a valid URL\n     : {0}\n - - - - - - - - - - - - - - - - - - - - - - ".format(href), 'x')                        

        except TimeoutError:
            msg("ERROR: " + " is not responding\n     : {0}\n - - - - - - - - - - - - - - - - - - - - - - ".format(url), 'x')

        except KeyboardInterrupt:
            print("\n(Ctrl + C) Terminated by user...\n")
            raise SystemExit

        except Exception as General_Error:
            msg("ERROR: URL generated a general error...\n     : {0}\n     : {1}\n - - - - - - - - - - - - - - - - - - - - - - ".format(url, str(General_Error)), 'x')            

    return crawled_urls


def export_csv(url: []):
    """ Export to file """
    try:
        f = open(_EXPORT, 'a')
    except FileNotFoundError:
        f = open(_EXPORT, 'w')
    finally:
        f.write('"{0}", "{1}", "{2}", "{3}"\n'.format(url[0], url[1], url[2], url[3]))
        f.close()


def recursion(urls: []):
    """ Crawl Recursively """
   
    new_urls = []

    for url in crawl(urls):
        msg("\n** NEW CRAWLING BRANCH *************\n** {0}\n************************************".format(url[0]), '|')
        new_urls = crawl([url])

        if len(new_urls) > 0:            
            crawl(new_urls)
        else:
            msg("**********************************\n BRANCH TRAVERSED UNTIL LAST URL *\n**********************************", '|')
        
    msg("\n\n******************************\n** NO MORE BRANCHES TO CRAWL *\n******************************", '|')


def msg(msg: str, ico: str):
    """ Shows info according to Verbosity """
    if _VERBOSE:
        print(msg)
    else:
        print(ico, end='', flush=True)


def main():
    """ Main """

    global _TIMEOUT, _DATABASE, _NOT_ONLY_ONION, _EXPORT, _VERBOSE

    parser = argparse.ArgumentParser()
    parser.add_argument('list', help="Text file containing URLs to crawl. One per line.", type=str, metavar='url_list')
    parser.add_argument('-v', '--verbose', help="Shows crawling info", action="store_true")    
    parser.add_argument('-t', '--timeout', help="Timeout for non-responding requests (default: 5 seg).", type=int, default=5, metavar='SECONDS')    
    parser.add_argument('-n', '--not-only-onion', help="Allow to crawl in not .onion domains.", action="store_true")    
    parser.add_argument('-r', '--recursive', help="Performs recursive crawling on found URLs.", action="store_true")
    parser.add_argument('-e', '--export', help="File name to save crawling results in CSV format.", type=str, metavar='filename.csv')
    parser.add_argument('-d', '--database', help="Specifies name for database (.db) file to store crawling results (default: database.db).", metavar='database.db', default='database.db')
    parser.add_argument('-i', '--init-db', help="Initialize an empty DB. Could be used to erase data from an existing DB.", action="store_true")
    args = parser.parse_args()
    
    # Extract urls from file
    urls = []
    try:
        f = open(args.list, "r") 
        for line in f:
            urls.append([line[0:-1], "", ""])  # line[0:-1] removes last '\n' char
       
    except FileNotFoundError:
        print("ERROR: File {0} not found".format(args.list))        
        raise SystemExit
    
    # Set Verbose    
    _VERBOSE = args.verbose

    # Set timeout
    if args.timeout is not None:
        _TIMEOUT = args.timeout

    # Set Not Only Onion
    _NOT_ONLY_ONION = args.not_only_onion

    # Set export file
    if args.export is not None:
        _EXPORT = args.export
        f = open(_EXPORT, 'w')
        f.write('"URL", "TITLE", "DESCRIPTION", "LAST_DATE"\n')
        f.close()

    # Set database file
    _DATABASE = args.database
    
    if args.init_db is True:
        db = database(_DATABASE)
        db._init_db()

    # Start recursive or simple crawling
    if args.recursive is True:
        recursion(urls)
    else:
        crawl(urls)    
    

# Entry point
if __name__ == "__main__":
    main()