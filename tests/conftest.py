import pytest


@pytest.fixture
def image_mocks(requests_mock):
    """Mock image urls."""
    requests = [
        (
            'http://www.sub.example.com/image/image1.png',
            {'Content-type': 'image/png'},
            b'image1',
        ),
        (
            'http://www.sub.example.com/path/to_something/_image/image2.png',
            {'Content-type': 'image/png'},
            b'image2',
        ),
        (
            'http://www.sub.example.com/path/_images/image3.png',
            {'Content-type': 'image/png'},
            b'image3',
        ),
        (
            'http://www.sub.example.com/image/image4.png',
            {'Content-type': 'image/png'},
            b'image4',
        ),
        (
            'https://www.sub.example.com/image/image5.jpg',
            {'Content-type': 'image/jpg'},
            b'image5',
        ),
        (
            'http://sub2.www.sub.example.com/path/image/image6.png',
            {'Content-type': 'image/png'},
            b'image6',
        ),
        (
            'http://sub.example.com/image/image7.png',
            {'Content-type': 'image/png'},
            b'image7',
        ),
        (
            'http://www.example.com/image/image8.png',
            {'Content-type': 'image/png'},
            b'image8',
        ),
        (
            'http://example.com/image/image9.png',
            {'Content-type': 'image/png'},
            b'image9',
        ),
        (
            'http://other.com/image/image10.png',
            {'Content-type': 'image/png'},
            b'image10',
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
            'http://www.sub.example.com/assets/file1.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://www.sub.example.com/path/to_something/assets/file2.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://www.sub.example.com/path/assets/file3.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://www.sub.example.com/assets/file4.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'https://www.sub.example.com/assets/file5.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://sub2.www.sub.example.com/path/assets/file6.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://www.example.com/assets/file7.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://www.sub.example.com/courses',
            {'Content-type': 'text/html'},
            'text',
        ),
        (
            'http://www.example.com/assets/menu.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://example.com/assets/menu.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://other.com/assets/menu.css',
            {'Content-type': 'text/css'},
            'text',
        ),
        (
            'http://other.com/courses',
            {'Content-type': 'text/html'},
            'text',
        ),
    ]
    for request in requests:
        url, headers, text = request  # noqa: WPS110
        requests_mock.get(url, text=text, headers=headers)
