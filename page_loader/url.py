import re
import urllib


def is_same_domain_or_subdomain(url: str, verifiable_url: str) -> bool:
    """Return True if verifiable_url is same domain or subdomain else False.

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
        '/image/image1.png', parent_url='example.com/path')
    'https://example.com/image/image1.png'
    """
    if parent_url.endswith('.html'):
        parent_url, *_ = parent_url.rsplit('/', 1)
        parent_url = f'{parent_url}/'
    parsed_parent_url = urllib.parse.urlparse(parent_url)
    if url.startswith('/'):
        scheme = parsed_parent_url.scheme
        netloc = parsed_parent_url.netloc
        absolute_url = f'{scheme}://{netloc}{url}'
    elif url.startswith('..'):
        new_parent_url = parent_url.rstrip('/').rpartition('/')[0]
        new_parent_url = f'{new_parent_url}/'
        new_url = url.partition('../')[2]
        absolute_url = relative_url_to_absolute(
            new_url, new_parent_url,
        )
    elif url.startswith('http'):
        absolute_url = url
    else:
        absolute_url = f'{parent_url}{url}'
    return absolute_url


def url_to_name(url: str, extension=None) -> str:
    """Create name for file/directory from url.

    Replace everything except letters and numbers with a hyphen.
    """
    parsed_url = urllib.parse.urlparse(url)
    path, *other = parsed_url.path.rsplit('.', 1)
    domain_and_path = '{domain}{path}'.format(
        domain=parsed_url.netloc,
        path=path.rstrip('/'),
    )
    file_name = re.sub('[^a-zA-Z0-9\n]', '-', domain_and_path)
    extension_from_path = f'.{other[0]}' if other else '.html'
    suffix = extension if extension else extension_from_path
    return f'{file_name}{suffix}'
