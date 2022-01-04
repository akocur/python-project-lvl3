import re
import urllib

DEFAULT_SCHEME = 'https'


def is_same_domain_or_subdomain(url: str, verifiable_url: str) -> bool:
    """Return True if cheched_url is same domain or subdomain else False.

    >>> is_same_domain_or_subdomain(\
        'http://sub.host.com/any/path/', 'http://sub.host.com/other/path')
    True

    >>> is_same_domain_or_subdomain(\
        'http://sub.host.com/any/path/', 'http://sub2.sub.host.com/other/path')
    True

    >>> is_same_domain_or_subdomain(\
        'http://sub.host.com/any/path/', '/image/image1.png')
    True

    >>> is_same_domain_or_subdomain(\
        'http://sub.host.com/any/path/', 'http://host.com/other/path')
    False

    >>> is_same_domain_or_subdomain(\
        'http://sub.host.com/any/path/', 'http://other-host.com/other/path')
    False
    """
    if not verifiable_url.startswith('http'):
        return True
    parsed_url = urllib.parse.urlparse(url)
    parsed_verifiable_url = urllib.parse.urlparse(verifiable_url)
    return parsed_verifiable_url.netloc.endswith(parsed_url.netloc)


def make_url_with_scheme(url: str, scheme: str) -> str:
    """Return new url with scheme.

    >>> make_url_with_scheme('example.com/path/index.html', 'http')
    'http://example.com/path/index.html'

    >>> make_url_with_scheme('http://example.com/path/index.html', 'https')
    'https://example.com/path/index.html'
    """
    _, _, url_without_sheme = url.rpartition('://')
    return f'{scheme}://{url_without_sheme}'


def complete_url_with_slash(url: str):
    """Add a slash to the end of the url if one not exist.

    >>> complete_url_with_slash('http://example.com/path/index.html')
    'http://example.com/path/index.html'

    >>> complete_url_with_slash('http://example.com/path')
    'http://example.com/path/'
    """
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    end = path.rpartition('/')[2]
    is_file = end.find('.') > 0
    if is_file or path.endswith('/'):
        return url
    new_path = f'{path}/'
    new_parsed_url = parsed_url._replace(path=new_path)  # noqa: WPS437
    return new_parsed_url.geturl()


def normalize_url(url: str, scheme='https', parent_url=None) -> str:
    """Return normalize url.

    >>> normalize_url('example.com/path/index.html')
    'https://example.com/path/index.html'

    >>> normalize_url('http://example.com/path/index.html')
    'http://example.com/path/index.html'

    >>> normalize_url('http://example.com/path')
    'http://example.com/path/'

    >>> normalize_url(\
        '/image/image1.png', parent_url='http://example.com/path')
    'http://example.com/image/image1.png'

    >>> normalize_url(\
        'http://example.com/image/image1.png',\
        parent_url='http://example.com/path')
    'http://example.com/image/image1.png'

    >>> normalize_url(\
        'example.com/image/image1.png',\
        parent_url='http://example.com/path')
    'https://example.com/image/image1.png'
    """
    if parent_url:
        if url.startswith('http'):
            return complete_url_with_slash(url)
        return relative_url_to_absolute(url, parent_url)
    if not url.startswith('http'):
        url = make_url_with_scheme(url, scheme)
    return complete_url_with_slash(url)


def relative_url_to_absolute(url: str, parent_url: str) -> str:
    """Convert relative url to absulute.

    >>> relative_url_to_absolute(\
        '/image/image1.png', parent_url='http://example.com/path')
    'http://example.com/image/image1.png'

    >>> relative_url_to_absolute(\
        '../../image/image1.png', parent_url='http://example.com/p1/p2/p3')
    'http://example.com/p1/image/image1.png'

    >>> relative_url_to_absolute(\
        'image/image1.png', parent_url='http://example.com/p1/p2')
    'http://example.com/p1/p2/image/image1.png'

    >>> relative_url_to_absolute(\
        '/image/image1.png',\
        parent_url='example.com/path')
    'https://example.com/image/image1.png'
    """
    normalized_parent_url = normalize_url(parent_url)
    parsed_parent_url = urllib.parse.urlparse(normalized_parent_url)
    if url.startswith('/'):
        scheme = parsed_parent_url.scheme
        netloc = parsed_parent_url.netloc
        absolute_url = f'{scheme}://{netloc}{url}'
    elif url.startswith('..'):
        new_parent_url = normalized_parent_url.rstrip('/').rpartition('/')[0]
        normalized_new_parent_url = normalize_url(new_parent_url)
        new_url = url.partition('../')[2]
        absolute_url = relative_url_to_absolute(
            new_url, normalized_new_parent_url,
        )
    else:
        absolute_url = f'{parent_url}{url}'
    return absolute_url


def url_to_name(url: str, extension: str) -> str:
    """
    Format the url to a directory/file name.

    Replace everything except letters and numbers with a hyphen.

    >>> url_to_name('https://docs.python.org:8080/3/library/\
        urllib.parse.html?highlight=url#urllib.parse.urlparse')
    docs-python-org-8080-3-library-urllib-parse-html.html

    """
    parsed_url = urllib.parse.urlparse(url, scheme=DEFAULT_SCHEME)
    path = parsed_url.path.rstrip('/')
    domain_and_path = f'{parsed_url.netloc}{path}'
    file_name = re.sub('[^a-zA-Z0-9]', '-', domain_and_path)
    return f'{file_name}{extension}'
