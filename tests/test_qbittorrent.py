from qbittorrent.qbittorrent import QBitTorrent, generator_len
from pyassert import assert_that
from mock import MagicMock, patch, ANY, DEFAULT
from requests.auth import HTTPDigestAuth


def test_get_torrents_should_call_get():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')

    sut.getTorrents()

    sut.__GET__.assert_called_with("/json/torrents")


def test_get_torrents_should_filter_by_func():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')
    sut.__GET__.return_value = list([
        {"state": "downloading"},
        {"state": "pausedDL"}
    ])

    torrents = sut.getTorrents(lambda x: x["state"] == "downloading")
    assert_that(generator_len(torrents)).is_equal_to(1)
    sut.__GET__.assert_called_with("/json/torrents")


def test_get_torrents_should_filter_by_state():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')
    sut.__GET__.return_value = [
        {"state": "downloading"},
        {"state": "pausedDL"}
    ]

    torrents = sut.getTorrents("downloading")

    assert_that(generator_len(torrents)).is_equal_to(1)
    sut.__GET__.assert_called_with("/json/torrents")


def test_get_torrents_should_filter_by_multiple_states():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')
    sut.__GET__.return_value = [
        {"state": "downloading"},
        {"state": "pausedDL"}
    ]

    torrents = sut.getTorrents(["downloading", "pausedDL"])

    assert_that(generator_len(torrents)).is_equal_to(2)
    sut.__GET__.assert_called_with("/json/torrents")


def test_get_torrents_should_filter_by_tuple():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__GET__ = MagicMock(name='__GET__')
    sut.__GET__.return_value = [
        {"state": "downloading", "name": "nameA"},
        {"state": "pausedDL", "name": "nameB"}
    ]

    torrents = sut.getTorrents(("name", "nameA"))

    assert_that(generator_len(torrents)).is_equal_to(1)
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


def test_pause_should_call_post():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.pause("ahash")

    sut.__POST__.assert_called_with("/command/pause", hash="ahash")


def test_pauseTorrents_by_state():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")
    sut.getTorrents = MagicMock(name="getTorrents")
    sut.getTorrents.return_value = [
        {"hash": "a"}, {"hash": "b"}, {"hash": "c"}
    ]

    sut.pauseTorrents(state="downloading")

    sut.getTorrents.assert_called_with("downloading")
    assert_that(sut.__POST__.call_count).is_equal_to(3)


def test_pauseTorrents_by_hashlist():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.pauseTorrents(hashes=["2", "3", "4"])

    assert_that(sut.__POST__.call_count).is_equal_to(3)


def test_resumeTorrents_by_state():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")
    sut.getTorrents = MagicMock(name="getTorrents")
    sut.getTorrents.return_value = [
        {"hash": "a"}, {"hash": "b"}, {"hash": "c"}
    ]

    sut.resumeTorrents(state="downloading")

    sut.getTorrents.assert_called_with("downloading")
    assert_that(sut.__POST__.call_count).is_equal_to(3)


def test_resumeTorrents_by_hashlist():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.resumeTorrents(hashes=["2", "3", "4"])

    assert_that(sut.__POST__.call_count).is_equal_to(3)


def test_delete_should_call_post():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.delete(False, "ahash", "another")

    sut.__POST__.assert_called_with("/command/delete", hashes="ahash|another")


def test_deleteperm_should_call_post():
    sut = QBitTorrent("admin", "adminadmin")
    sut.__POST__ = MagicMock(name="post")

    sut.delete(True, "ahash", "another")

    sut.__POST__.assert_called_with("/command/deletePerm", hashes="ahash|another")
