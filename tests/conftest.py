import pytest


@pytest.fixture
def image_mocks(requests_mock):
    """Mock image urls."""
    requests = [
        (
            'https://sub1.example.com/images/image1.png',
            {'Content-type': 'image/png'},
            b'image1',
        ),
        (
            'https://sub1.example.com/path/to/_images/image2.png',
            {'Content-type': 'image/png'},
            b'image2',
        ),
        (
            'https://sub1.example.com/path/images/image3.png',
            {'Content-type': 'image/png'},
            b'image3',
        ),
        (
            'https://sub1.example.com/images/image4.jpg',
            {'Content-type': 'image/jpg'},
            b'image4',
        ),
        (
            'https://sub2.sub1.example.com/path/images/image5.png',
            {'Content-type': 'image/png'},
            b'image5',
        ),
        (
            'https://example.com/images/image6.png',
            {'Content-type': 'image/png'},
            b'image6',
        ),
        (
            'https://other.com/images/image7.jpg',
            {'Content-type': 'image/jpg'},
            b'image7',
        ),
    ]
    for request in requests:
        url, headers, content = request  # noqa: WPS110
        requests_mock.get(url, content=content, headers=headers)


@pytest.fixture
def link_mocks(requests_mock):
    """Mock link urls."""
    requests = [
        (
            'https://sub1.example.com/assets/file1.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'https://sub1.example.com/path/to/assets/file2.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'https://sub1.example.com/path/assets/file3.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'https://sub1.example.com/path/to/file4.html',
            {'Content-type': 'text/html'},
            'text',
        ),
        (
            'https://sub1.example.com/courses',
            {'Content-type': 'text/html'},
            'text',
        ),
        (
            'https://sub1.example.com/assets/file5.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://sub2.sub1.example.com/path/assets/file6.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://example.com/assets/file7.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://other.com/assets/file8.css',
            {'Content-type': 'text/css'},
            'text',
        ),
    ]
    for request in requests:
        url, headers, text = request  # noqa: WPS110
        requests_mock.get(url, text=text, headers=headers)


@pytest.fixture
def script_mocks(requests_mock):
    """Mock script urls."""
    requests = [
        (
            'https://sub1.example.com/static/script1.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://sub1.example.com/path/to/_static/script2.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://sub1.example.com/path/static/script3.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://sub1.example.com/static/script4.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://sub2.sub1.example.com/path/static/script5.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://example.com/static/script6.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
        (
            'https://other.com/static/script7.js',
            {'Content-type': 'application/javascript'},
            'text',
        ),
    ]
    for request in requests:
        url, headers, text = request  # noqa: WPS110
        requests_mock.get(url, text=text, headers=headers)
