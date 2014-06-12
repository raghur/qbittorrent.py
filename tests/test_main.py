from qbittorrent.main import main
from pyassert import *
from mock import MagicMock, patch


@patch('qbittorrent.qbittorrent.QBitTorrent', autospec=True)
def test_should_show_help_with_no_params(mock):
    instance = mock.return_value
    instance.getTorrents.return_value = []
    instance.activeDownloads.return_value = []

    v = main([])
    print "v:", v
    instance.getTorrents.assert_called_with()
    instance.activeDownloads.assert_called_with()
