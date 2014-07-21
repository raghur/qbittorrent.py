from qbittorrent.main import main
from pyassert import assert_that
from mock import patch, ANY, DEFAULT


@patch('qbittorrent.main.listTorrentsCommand', autospec=True)
def test_should_run_list_command(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to("")
        return DEFAULT
    mock.side_effect = side_effect
    main(["list"])
    mock.assert_called_with(ANY)


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_listTorrents_should_call_qbittorrent_with_None(mock):
    instance = mock.return_value
    instance.getTorrents.return_value = []
    main(["list"])
    instance.getTorrents.assert_called_with(None)


@patch('qbittorrent.main.listTorrentsCommand', autospec=True)
def test_should_run_list_command_with_explicit_filter(mock):
    def side_effect(a):
        assert_that(a.state).is_equal_to(["uploading"])
        return DEFAULT
    mock.side_effect = side_effect
    main(["list", "uploading"])
    mock.assert_called_with(ANY)


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_pauseTorrentsCommand_should_call_with_state_array(mock):
    instance = mock.return_value
    instance.pauseTorrents.return_value = []
    main("pause -s stalledUP".split(" "))
    instance.pauseTorrents.assert_called_with(state=["stalledUP"])


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_pauseTorrentsCommand_should_call_with_torrent_list(mock):
    instance = mock.return_value
    instance.pauseTorrents.return_value = []
    main("pause -t 1 2 3 4".split(" "))
    instance.pauseTorrents.assert_called_with(hashes="1 2 3 4".split(" "))


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


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_resumeTorrentsCommand_should_call_with_state_array(mock):
    instance = mock.return_value
    instance.resumeTorrents.return_value = []
    main("resume -s stalledUP".split(" "))
    instance.resumeTorrents.assert_called_with(state=["stalledUP"])


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_resumeTorrentsCommand_should_call_with_torrent_list(mock):
    instance = mock.return_value
    instance.resumeTorrents.return_value = []
    main("resume -t 1 2 3 4".split(" "))
    instance.resumeTorrents.assert_called_with(hashes="1 2 3 4".split(" "))


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
