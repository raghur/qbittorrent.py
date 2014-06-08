import qbittorrent
import sys
import os
import argparse
import requests

import logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',)
def parse_args(argv):
    parser = argparse.ArgumentParser(description = """CLI remote control app for qbittorrent""",
                                     fromfile_prefix_chars='@')
    parser.add_argument('-s',
                        '--server',
                        dest='host',
                        default="localhost",
                        help="host name/ip of the server")
    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        default=8080,
                        help="Port number")
    parser.add_argument('-u',
                        '--user',
                        dest='user',
                        default="admin",
                        help="username ")
    parser.add_argument('--pass',
                        dest='password',
                        default="adminadmin",
                        help="password")
    #parser.add_argument('-t',
                        #'--token',
                        #dest='token',
                        #help="OAuth Token",
                        #required=True)
    #parser.add_argument('-r',
                        #'--repository',
                        #dest='repository',
                        #help="Repository in 'owner/repo' format")
    #parser.add_argument('-c',
                        #'--commit',
                        #dest='commit',
                        #help="commit SHA (usually first 5 chars are sufficient)")
    #parser.add_argument('recipients',
                        #nargs="+",
                        #help="Recipient email address(es)")
    parser.add_argument("-v",
                        "--verbose",
                        help="Log level: INFO,DEBUG,CRITICAL,WARNING",
                        dest = "verbosity",
                        default="INFO")
    config = os.path.expanduser("~/.qbittorrent.py")
    if (os.path.exists(config)):
        logger.debug("include config file", config)
        argv = ["@" + config] + argv
    args = parser.parse_args(argv)
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, args.verbosity.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.verbosity.upper())
    logger.info("Setting log level to: %s", args.verbosity)
    logger.setLevel(numeric_level)
    logger.debug(args)
    return args


def main(sysargv=sys.argv):
    """@todo: Docstring for main.

    :sysargv: @todo
    :returns: @todo

    """
    args = parse_args(sysargv[1:])
    qb = qbittorrent.QBitTorrent(args.user, args.password)
    try:
        print "List of torrents: ", qb.getTorrents()
        print "Active downloads: ", qb.activeDownloads()
        return 0
    except requests.ConnectionError,e:
        print e
        return -1

if __name__ == '__main__':
    v = main()
    exit(v)
