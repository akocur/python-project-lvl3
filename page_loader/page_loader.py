import re
import urllib
from pathlib import Path

import requests


def _url_to_file_name(url: str) -> str:
    """
    Format the url to the correct html file name.

    Replace everything except letters and numbers with a hyphen.

    >>> _url_to_file_name('https://docs.python.org:8080/3/library/\
        urllib.parse.html?highlight=url#urllib.parse.urlparse')
    docs-python-org-8080-3-library-urllib-parse-html.html

    """
    url_with_scheme = url if url.startswith('http') else ''.join([
        'https://',
        url,
    ])
    urlparse = urllib.parse.urlparse(url_with_scheme)
    domain_and_path = ''.join([urlparse.netloc, urlparse.path.rstrip('/')])
    return ''.join([
        re.sub('[^a-zA-Z0-9]', '-', domain_and_path),
        '.html',
    ])


def download(url: str, dir_path: str) -> str:
    """
    Download data from url and save to dir_path.

    >>> download('https://git-scm.com/docs/git-commit', '/home/user/')
    '/home/user/git-scm-com-docs-git-commit.html'

    >>> download('docs.python.org:80/3/library/', '/home/user/')
    '/home/user/docs-python-org-80-3-library.html'

    """
    response = requests.get(url)
    file_name = _url_to_file_name(url)
    file_path = Path(dir_path) / file_name
    file_path.write_text(response.text)

    return str(file_path.resolve())
