import pytest

from page_loader.url import url_to_name


@pytest.mark.parametrize(
    'url,content_type,suffix,expected_name',
    [
        (
            'http://www.example.com:80/path/to_something/',
            'text/html',
            '.html',
            'www-example-com-80-path-to-something.html',
        ),
        (
            'www.example.com:80/path/to_something/',
            'text/html',
            None,
            'www-example-com-80-path-to-something.html',
        ),
        (
            'sub-sub-domen.ru.example.com/path/to_something/',
            'text/html',
            None,
            'sub-sub-domen-ru-example-com-path-to-something.html',
        ),
        (
            (
                'https://sub.domain.com:8080/path/to/part.file.html'
                '?param=value#fragment'
            ),
            'text/html',
            None,
            'sub-domain-com-8080-path-to-part-file.html',
        ),
        (
            'http://www.example.com:80/path/to_something/',
            'text/html',
            '_files',
            'www-example-com-80-path-to-something_files',
        ),
        (
            'http://www.sub.example.com/file.css',
            'text/css',
            None,
            'www-sub-example-com-file.css',
        ),
        (
            'http://www.sub.example.com/file.png',
            'image/png',
            None,
            'www-sub-example-com-file.png',
        ),
        (
            'http://www.sub.example.com/courses',
            'text/html',
            None,
            'www-sub-example-com-courses.html',
        ),
    ],
)
def test_url_to_name(url, content_type, suffix, expected_name):
    """Test url_to_name."""
    assert url_to_name(url, content_type, suffix) == expected_name
