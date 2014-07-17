from qbittorrent.main import main
from pyassert import assert_that
from mock import patch


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_should_run_with_default_params(mock):
    instance = mock.return_value
    instance.getTorrents.return_value = []
    instance.activeDownloads.return_value = []

    v = main([])
    instance.getTorrents.assert_called_with()
    instance.activeDownloads.assert_called_with()
    assert_that(v).is_equal_to(0)
