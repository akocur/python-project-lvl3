import pytest

from page_loader.url import url_to_name


@pytest.mark.parametrize(
    'url,content_type,extension,expected_name',
    [
        (
            'https://sub1.example.com/path/to/',
            'text/html',
            '.html',
            'sub1-example-com-path-to.html',
        ),
        (
            'https://sub1.example.com/path/to/',
            'text/html',
            None,
            'sub1-example-com-path-to.html',
        ),
        (
            (
                'https://sub.domain.com/path/to/part.file.html'
                '?param=value#fragment'
            ),
            'text/html',
            None,
            'sub-domain-com-path-to-part-file.html',
        ),
        (
            (
                'https://sub.domain.com/path/to/part.file.html'
                '?param=value#fragment'
            ),
            'text/html',
            '.html',
            'sub-domain-com-path-to-part-file.html',
        ),
        (
            'https://sub1.example.com/path/to/',
            'text/html',
            '_files',
            'sub1-example-com-path-to_files',
        ),
        (
            'https://sub1.example.com/path/to/file.html',
            'text/html',
            '_files',
            'sub1-example-com-path-to-file_files',
        ),
        (
            'https://sub1.example.com/file.css',
            'text/css',
            None,
            'sub1-example-com-file.css',
        ),
        (
            'https://sub1.example.com/file.png',
            'image/png',
            None,
            'sub1-example-com-file.png',
        ),
        (
            'https://sub1.example.com/courses',
            'text/html',
            None,
            'sub1-example-com-courses.html',
        ),
        (
            'https://sub1.example.com/script.js',
            'application/javascript',
            None,
            'sub1-example-com-script.js',
        ),
        (
            'https://sub1.example.com/script.js',
            'application/javascript; charset=UTF-8',
            None,
            'sub1-example-com-script.js',
        ),
        (
            'https://js.stripe.com/v3/',
            'application/javascript',
            None,
            'js-stripe-com-v3.js',
        ),
    ],
)
def test_url_to_name(url, content_type, extension, expected_name):
    """Test url_to_name."""
    assert url_to_name(url, content_type, extension) == expected_name
