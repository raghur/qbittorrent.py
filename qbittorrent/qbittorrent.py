import requests
from requests.auth import HTTPDigestAuth
import urlparse
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

    def __POST__(self,  url, **kwargs):
        """@todo: Docstring for __POST.

        :**kwargs: @todo
        :returns: @todo

        """
        url = urlparse.urljoin(self._url, url)
        logger.debug("POST: %s", url)
        r = requests.post(url, kwargs, auth=self._auth)

    def __GET__(self, url):
        """@todo: Docstring for getRequest.

        :url: @todo
        :returns: @todo

        """
        url = urlparse.urljoin(self._url, url)
        logger.debug("GET: %s", url)
        r = requests.get(url, auth=self._auth)
        r.raise_for_status()
        return r.json()

    def resume(self, hash):
        """@todo: Docstring for resume.

        :hash: @todo
        :returns: @todo

        """
        return self.__POST__("/command/resume", hash=hash)

    def getTorrents(self, filter=None):
        """@todo: Docstring for getTorrentList.
        :returns: @todo

        """
        l = self.__GET__("/json/torrents")
        if callable(filter):
            return itertools.ifilter(filter, l)
        elif isinstance(filter, str):
            return itertools.ifilter(lambda x: x["state"] == filter, l)
        elif isinstance(filter, tuple):
            return itertools.ifilter(lambda x: x[filter[0]] == filter[1], l)
        else:
            return l

    def activeDownloads(self):
        """@todo: Docstring for hasActiveDownloads.
        :returns: @todo

        """
        try:
            f = self.getTorrents('downloading')
            return generator_len(f)
        except StopIteration, e:
            return 0

    def resumeDownloads(self):
        """@todo: Docstring for resumeDownloads.
        :returns: @todo

        """
        pausedDls = self.getTorrents('pausedDL')
        for torrent in pausedDls:
            self.resume(torrent.hash)

if __name__ == '__main__':
    qb = QBitTorrent("admin", "adminadmin")
    print qb.getTorrents()
