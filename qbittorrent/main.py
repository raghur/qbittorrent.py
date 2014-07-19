import qbittorrent
import sys
import os
import argparse
import requests
import json

import logging
logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="""CLI remote control app for qbittorrent""",
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
    parser.add_argument("-v",
                        "--verbose",
                        help="Log level: INFO,DEBUG,CRITICAL,WARNING",
                        dest="verbosity",
                        default="CRITICAL")

    subparsers = parser.add_subparsers(help="sub command help")
    listCommand = subparsers.add_parser("list", help="lists torrents")
    add_state_argument(listCommand)
    listCommand.add_argument("-f", "--format", choices=["json", "csv"],
                             default="csv")
    listCommand.set_defaults(func=listTorrentsCommand)

    pauseCommand = subparsers.add_parser("pause", help="pause torrent")
    g = pauseCommand.add_mutually_exclusive_group(required=True)
    g.add_argument("-t",
                   "--torrents",
                   nargs="+")
    add_state_argument(g)
    pauseCommand.set_defaults(func=pauseTorrentsCommand)

    resumeCommand = subparsers.add_parser("resume", help="resume torrent")
    g = resumeCommand.add_mutually_exclusive_group(required=True)
    g.add_argument("-t",
                   "--torrents",
                   nargs="+")
    add_state_argument(g)
    resumeCommand.set_defaults(func=resumeTorrentsCommand)

    queueCommand = subparsers.add_parser("queue", help="manage queue")
    queueCommand.add_argument("torrent", nargs=1)
    queueCommand.add_argument("-a",
                              "--action",
                              required=True,
                              choices=["up", "down", "top", "bottom"])
    queueCommand.set_defaults(func=manageQueueCommand)

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


def add_state_argument(command, default=None):
    command.add_argument("-s",
                         "--state",
                         choices=[
                             "error",
                             "pausedUP",
                             "pausedDL",
                             "queuedUP",
                             "queuedDL",
                             "uploading",
                             "stalledUP",
                             "stalledDL",
                             "checkingUP",
                             "checkingDL",
                             "downloading"
                         ],
                         default=default)


def main(arglist):
    """@todo: Docstring for main.

    :sysargv: @todo
    :returns: @todo

    """
    args = parse_args(arglist)
    return args.func(args)


def sysmain():
    return main(sys.argv[1:])


def resumeTorrentsCommand(args):
    logger.debug(args)
    if args.state:
        return doQbitTorrentCall(
            args,
            lambda qb: qb.resumeTorrents(state=args.state))
    else:
        return doQbitTorrentCall(
            args,
            lambda qb: qb.resumeTorrents(hashes=args.torrents))


def manageQueueCommand(args):
    logger.debug(args)
    pass


def pauseTorrentsCommand(args):
    logger.debug(args)
    if args.state:
        return doQbitTorrentCall(
            args,
            lambda qb: qb.pauseTorrents(state=args.state))
    else:
        return doQbitTorrentCall(
            args,
            lambda qb: qb.pauseTorrents(hashes=args.torrents))


def listTorrentsCommand(args):
    def action(qb):
        for t in qb.getTorrents(args.state):
            if (args.format == "json"):
                print(json.dumps(t, sort_keys=True, indent=2))
            elif (args.format == "csv"):
                print(",".join([unicode(i) for i in t.values()]))
    return doQbitTorrentCall(args, action)


def doQbitTorrentCall(args, action):
    try:
        qb = qbittorrent.QBitTorrent(args.user,
                                     args.password,
                                     args.host,
                                     args.port)
        return action(qb)
    except requests.ConnectionError as e:
        logger.error(e)
        return -1


if __name__ == '__main__':
    v = sysmain()
    exit(v)
