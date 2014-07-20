from qbittorrent.main import main
from pyassert import assert_that
from mock import patch, ANY, DEFAULT


@patch('qbittorrent.main.listTorrentsCommand', autospec=True)
def test_should_run_list_command(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to("downloading")
        return DEFAULT
    mock.side_effect = side_effect
    main(["list"])
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.listTorrentsCommand', autospec=True)
def test_should_run_list_command_with_explicit_filter(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to(["uploading"])
        return DEFAULT
    mock.side_effect = side_effect
    main(["list", "uploading"])
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.pauseTorrentsCommand', autospec=True)
def test_should_run_pause_by_state(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to(["stalledUP"])
        return DEFAULT
    mock.side_effect = side_effect
    main("pause -s stalledUP".split(" "))
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.pauseTorrentsCommand', autospec=True)
def test_should_run_pause_by_torrentlist(mock):
    def side_effect(a):
        assert_that(a.torrents).is_equal_to(["1", "2", "3"])
        return DEFAULT
    mock.side_effect = side_effect
    main("pause -t 1 2 3".split(" "))
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.resumeTorrentsCommand', autospec=True)
def test_should_resume_by_state(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to(["stalledUP"])
        return DEFAULT
    mock.side_effect = side_effect
    main("resume -s stalledUP".split(" "))
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.resumeTorrentsCommand', autospec=True)
def test_should_resume_by_torrentlist(mock):
    def side_effect(a):
        assert_that(a.torrents).is_equal_to(["1", "2", "3"])
        return DEFAULT
    mock.side_effect = side_effect
    main("resume -t 1 2 3".split(" "))
    mock.assert_called_with(ANY)


@patch('qbittorrent.main.manageQueueCommand', autospec=True)
def test_should_manage_queue(mock):
    def side_effect(a):
        assert_that(a.torrent).is_equal_to(["1"])
        assert_that(a.action).is_equal_to("up")
        return DEFAULT
    mock.side_effect = side_effect
    main("queue -a up 1".split(" "))
    mock.assert_called_with(ANY)
