import argparse
from pathlib import Path

from page_loader import download


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] <url>',  # noqa: WPS323
        description="""
        PageLoader is a command-line utility that downloads pages
        from the Internet and saves them on your computer. Together with
        the page, it downloads all resources (images, styles and js),
        allowing you to open the page without the Internet.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        '-o',
        '--out',
        help='output directory where the specified url is saved',
        default=Path.cwd(),
        type=Path,
        metavar='[dir]',
        dest='dir_path',
    )
    parser.add_argument(
        'url',
        type=str,
    )
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='display help for command',
    )
    args = parser.parse_args()
    path = download(args.url, args.dir_path)
    print(path)  # noqa: WPS421


if __name__ == '__main__':
    main()
