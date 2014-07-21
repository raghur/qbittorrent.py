import requests
from requests.auth import HTTPDigestAuth
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import itertools
import logging
logger = logging.getLogger()


def generator_len(gen):
    return sum(1 for _ in gen)


class QBitTorrent(object):

    """Docstring for QBitTorrent. """

    def __init__(self, user, password, host="localhost", port=8080):
        """@todo: to be defined1.

        :user: @todo
        :password: @todo
        :url: @todo

        """
        self._user = user
        self._password = password
        self._url = "http://%s:%s" % (host, port)
        self._auth = HTTPDigestAuth(self._user, self._password)

    def __POST__(self, url, **kwargs):
        """@todo: Docstring for __POST.

        :**kwargs: @todo
        :returns: @todo

        """
        url = urljoin(self._url, url)
        logger.debug("POST: %s", url)
        requests.post(url, kwargs, auth=self._auth)

    def __GET__(self, url):
        """@todo: Docstring for getRequest.

        :url: @todo
        :returns: @todo
        """

        url = urljoin(self._url, url)
        logger.debug("GET: %s", url)
        r = requests.get(url, auth=self._auth)
        r.raise_for_status()
        return r.json()

    def resume(self, *args):
        for hash in args:
            self.__POST__("/command/resume", hash=hash)

    def pause(self, *args):
        for hash in args:
            self.__POST__("/command/pause", hash=hash)

    def delete(self, deleteData=False, *args):
        print(args)
        if deleteData:
            uri = "/command/deletePerm"
        else:
            uri = "/command/delete"
        return self.__POST__(uri, hashes="|".join(args))

    def increasePriority(self, hashes):
        return self.__POST__("/command/increasePrio", hashes="|".join(hashes))

    def decreasePriority(self, action, hashes):
        return self.__POST__("/command/decreasePrio", hashes="|".join(hashes))

    def maxPriority(self, hashes):
        return self.__POST__("/command/topPrio", hashes="|".join(hashes))

    def minPriority(self, hashes):
        return self.__POST__("/command/bottomPrio", hashes="|".join(hashes))

    def getTorrents(self, filter=None):
        """@todo: Docstring for getTorrentList.
        :returns: @todo
        """
        l = self.__GET__("/json/torrents")
        if callable(filter):
            return itertools.ifilter(filter, l)
        elif isinstance(filter, list):
            return itertools.ifilter(lambda x: x["state"] in filter, l)
        elif isinstance(filter, str):
            return itertools.ifilter(lambda x: x["state"] == filter, l)
        elif isinstance(filter, tuple):
            return itertools.ifilter(lambda x: x[filter[0]] == filter[1], l)
        else:
            return l

    def resumeTorrents(self, state=None, hashes=None):
        """@todo: Docstring for resumeTorrents.
        :returns: @todo

        """
        if (hashes):
            self.resume(*hashes)
        elif (state):
            torrents = self.getTorrents(state)
            hashes = map(lambda x: x["hash"], torrents)
            self.resume(*hashes)

    def pauseTorrents(self, state=None, hashes=None):
        if (hashes):
            self.pause(*hashes)
        elif(state):
            torrents = self.getTorrents(state)
            hashes = map(lambda x: x["hash"], torrents)
            self.pause(*hashes)

if __name__ == '__main__':
    qb = QBitTorrent("admin", "adminadmin")
    print(qb.getTorrents())
