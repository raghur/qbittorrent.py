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
        assert_that(a.state).is_equal_to("uploading")
        return DEFAULT
    mock.side_effect = side_effect
    main(["list", "--state", "uploading"])
    mock.assert_called_with(ANY)
