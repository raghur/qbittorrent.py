import requests
from requests.auth import HTTPDigestAuth
import urlparse
import itertools

class QBitTorrent(object):

    """Docstring for QBitTorrent. """

    def __init__(self, user, password, url = "http://localhost:8080"):
        """@todo: to be defined1.

        :user: @todo
        :password: @todo
        :url: @todo

        """
        self._user = user
        self._password = password
        self._url = url
        self._auth = HTTPDigestAuth(self._user, self._password)

    def __GET(self, url):
        """@todo: Docstring for getRequest.

        :url: @todo
        :returns: @todo

        """
        url = urlparse.urljoin(self._url, url)
        r = requests.get(url, auth = self._auth )
        r.raise_for_status()
        return r.json()

    def getTorrentList(self):
        """@todo: Docstring for getTorrentList.
        :returns: @todo

        """
        return self.__GET("/json/torrents")

    def hasActiveDownloads(self):
        """@todo: Docstring for hasActiveDownloads.
        :returns: @todo

        """
        try:
            r = self.getTorrentList()
            f = itertools.ifilter(lambda o: o["state"] == 'downloading', r)
            next(f)
            return True
        except StopIteration, e:
            return False

if __name__ == '__main__':
    qb = QBitTorrent("admin", "adminadmin")
    print qb.hasActiveDownloads()
