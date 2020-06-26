import json
import requests
import time
from datetime import date

class RateLimitException(Exception):
    pass

class ServerException(Exception):
    pass

class stackoverflow_engine:
    """
    The search engine to crawl stackoverflow and collects information about the tags and corresponding frequencies: ::

        Usage: >>> stackoverflow_engine().search()

    Be aware that too frequent invocation can lead to IP blockage because of the rate limit of stackoverflow.

    :param str stackoverflow_base: the base api of stackoverflow
    :param int today_epoch: the Unix timestamp of 00:00:00 of today
    :param session: request session to hold the connection for quering the following pages
    """
    stackoverflow_base = 'https://api.stackexchange.com'

    def query_page(self):
        api_url = '{0}/2.2/questions?pagesize=100&fromdate={1}&order=desc&sort=activity&site=stackoverflow'.format(self.stackoverflow_base, self.today_epoch)
        print(api_url)

        response = self.session.get(api_url)
        #only raise exception when first request
        if response.status_code == 400:
            raise RateLimitException('Stackoverflow reached rate limit')
        if response.status_code != 200:
            raise ServerException('Error when request stackoverflow server')

        nextpage = 2
        yield response.json()
        while nextpage <= 10 and response.json()['has_more']:
            response = self.session.get(api_url, params={'page': nextpage})
            nextpage += 1
            yield response.json()

    def search(self):
        """
        Search the most recent 1000 (10 pages * 100 max items per page) questions posted since the begin of today, then count the frequencies of each tag appeared in questions.
        Be aware that too frequent invocation can lead to IP blockage because of the rate limit of stackoverflow.

        :returns dict: the dict of (tag -> counts)
        """
        count = 1
        self.today_epoch = int(time.time()) - int(time.time())%86400
        self.session = requests.Session()
        languages = {}
        try:
            for page in self.query_page():
                if page is None :
                    break
                items = page.get('items')
                if items is None:
                    break
                for item in items:
                    for tag in item['tags']:
                        if tag in languages:
                            languages[tag] += 1
                        else:
                            languages[tag] = 1
                print('This is page {}, contains {} entries.'.format(count, len(items)))
                count += 1
        except Exception as re:
            if languages:
                return languages
            else:
                raise
        return languages



class github_engine:
    """
    The search engine to crawl github and collects information about the programming languages and corresponding frequencies in newly created repositories: ::

        Usage: >>> github_engine().search()

    Be aware that too frequent invocation can lead to IP blockage because of the rate limit of github.

    :param str github_base: the base api of github
    :param date today: the datetime.date object referring to today
    :param session: request session to hold the connection for quering the following pages
    """

    github_base = 'https://api.github.com'

    def query_page(self):
        api_url = '{0}/search/repositories?q=created:>={1}&per_page=100'.format(self.github_base, self.today.strftime("%Y-%m-%d"))
        print(api_url)
        response = self.session.get(api_url)

        #Github's error status for rate limit
        if response.status_code == 403:
            raise RateLimitException('Github reached rate limit')
        if response.status_code != 200:
            raise ServerException('Error when request Github server')
        nextpage = 2
        yield response.json()
        while 'next' in response.links.keys():
            response = self.session.get(api_url, params={'page': nextpage})
            if response.status_code != 200:
                return None
            nextpage += 1
            yield response.json()

    def search(self):
        """
        Search the most recent 1000 (10 pages * 100 max items per page) newly created repositories since the begin of today, then count the frequencies of each programming language marked in each repository.
        Be aware that too frequent invocation can lead to IP blockage because of the rate limit of github.

        :returns dict: the dict of (language -> counts)
        """

        self.session = requests.Session()
        self.today = date.today()
        count = 1
        languages = {}
        try:
            for page in self.query_page():
                if page is None :
                    break
                items = page.get('items')
                if items is None:
                    break
                for item in items:
                    lan = item['language']
                    if lan in languages:
                        languages[lan] += 1
                    else:
                        languages[lan] = 1
                print('This is page {}, contains {} entries.'.format(count, len(items)))
                count += 1
        except Exception as e:
            if languages:
                return languages
            else:
                raise
        return languages

class search_engine:
    """
    Wrap search engines of all websites and merge the search results.

    :param dict sites: website name and a corresponding search engine instance
    """
    sites = {'stackoverflow' : stackoverflow_engine(), 'github': github_engine()}
    def search(self):
        """
        :returns dict: merged search results. It contains the date of creation.
        """
        results = []
        for name, engine in self.sites.items():
            try:
                results.append(engine.search())
            except RateLimitException as re:
                raise
            except Exception as e:
                raise

        #'counts' -> accumulative counts; 'contained' -> which website contains it
        merged = {'created_time' : time.time(), 'items' : {}}
        for idx, individual_result in enumerate(results):
            for k, v in individual_result.items():
                if k is None:
                    continue
                kl = k.lower()
                if kl in merged['items']:
                    merged['items'][kl]['counts'] += v
                    if merged['items'][kl]['contained'][-1] != idx:
                        merged['items'][kl]['contained'].append(idx)
                else:
                    merged['items'][kl] = {'counts':v, 'contained':[idx]}
        return merged

if __name__ == '__main__':
    stackoverflow_engine().search()
    #search_engine().search()
