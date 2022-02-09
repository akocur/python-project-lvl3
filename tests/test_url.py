import pytest

from page_loader.url import relative_url_to_absolute, url_to_name


@pytest.mark.parametrize(
    'url,extension,expected_name',
    [
        (
            'https://sub1.example.com/path/to/',
            None,
            'sub1-example-com-path-to.html',
        ),
        (
            'https://sub1.example.com/path/to/',
            '_files',
            'sub1-example-com-path-to_files',
        ),
        (
            'https://sub1.example.com/courses',
            None,
            'sub1-example-com-courses.html',
        ),
        (
            'https://sub1.example.com/courses',
            '_files',
            'sub1-example-com-courses_files',
        ),
        (
            'https://sub1.example.com/path/to/',
            '.html',
            'sub1-example-com-path-to.html',
        ),
        (
            'https://sub1.example.com/path/to/file.1.2.html',
            None,
            'sub1-example-com-path-to-file-1-2.html',
        ),
        (
            'https://sub1.example.com/path/to/file.1.2.html',
            '.html',
            'sub1-example-com-path-to-file-1-2.html',
        ),
        (
            'https://sub1.example.com/path/to/file.1.2.html',
            '_files',
            'sub1-example-com-path-to-file-1-2_files',
        ),
        (
            'https://sub1.example.com/file.1.2.css',
            None,
            'sub1-example-com-file-1-2.css',
        ),
        (
            'https://sub1.example.com/path.ru/file.1.2.png',
            None,
            'sub1-example-com-path-ru-file-1-2.png',
        ),
        (
            'https://sub1.example.com/script.1.2.js',
            None,
            'sub1-example-com-script-1-2.js',
        ),
    ],
)
def test_url_to_name(url, extension, expected_name):
    """Test url_to_name."""
    if extension is None:
        assert url_to_name(url) == expected_name
    else:
        assert url_to_name(url, extension) == expected_name


@pytest.mark.parametrize(
    'url,parent_url,expected_url',
    [
        (
            'https://sub1.example.com/path/to/',
            'https://sub1.example.com/path/to/',
            'https://sub1.example.com/path/to/',
        ),
        (
            '/img/file.png',
            'https://sub1.example.com/path/to/',
            'https://sub1.example.com/img/file.png',
        ),
        (
            '_img/file.png',
            'https://sub1.example.com/path/to/',
            'https://sub1.example.com/path/to/_img/file.png',
        ),
        (
            '../img/file.png',
            'https://sub1.example.com/path/to/',
            'https://sub1.example.com/path/img/file.png',
        ),
        (
            '/img/file.png',
            'https://sub1.example.com/path/to/file.html',
            'https://sub1.example.com/img/file.png',
        ),
        (
            '_img/file.png',
            'https://sub1.example.com/path/to/file.html',
            'https://sub1.example.com/path/to/_img/file.png',
        ),
        (
            '../img/file.png',
            'https://sub1.example.com/path/to/file.html',
            'https://sub1.example.com/path/img/file.png',
        ),
        (
            '_img/1.2.png',
            'https://sub1.example.com/path/to/file.html',
            'https://sub1.example.com/path/to/_img/1.2.png',
        ),
        (
            '_images/6.1.jpg',
            'https://www.crummy.com/BeautifulSoup/bs4/doc.ru/bs4ru.html',
            'https://www.crummy.com/BeautifulSoup/bs4/doc.ru/_images/6.1.jpg',
        ),
    ],
)
def test_relative_url_to_absolute(url, parent_url, expected_url):
    """Test url_to_name."""
    assert relative_url_to_absolute(url, parent_url) == expected_url
