from qbittorrent.qbittorrent import QBitTorrent
from pyassert import assert_that
from mock import MagicMock, patch, ANY, DEFAULT
from requests.auth import HTTPDigestAuth


def test_get_torrents_should_call_get():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')

    sut.getTorrents()

    sut.__GET__.assert_called_with("/json/torrents")


def test_resume_should_call_post():

    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.resume("ahash")

    sut.__POST__.assert_called_with("/command/resume", hash="ahash")


@patch('requests.get', autospec=True)
def test_get_torrents_should_call_the_correct_endpoint(mock):
    sut = QBitTorrent("admin", "adminadmin")

    def side_effect(*args, **kwargs):
        """@todo: Docstring for side_effect.

        :**kwargs: @todo
        :returns: @todo
        """
        assert_that(len(kwargs)).is_equal_to(1)
        assert_that(kwargs["auth"]).is_instance_of(HTTPDigestAuth)
        assert_that(len(args)).is_equal_to(1)
        assert_that(args[0]).ends_with("/json/torrents")
        return DEFAULT

    mock.side_effect = side_effect
    rv = mock.return_value
    rv.json.return_value = ["test"]

    sut.getTorrents()

    rv.raise_for_status.assert_called_with()
    mock.assert_called_with(ANY, auth=ANY)
