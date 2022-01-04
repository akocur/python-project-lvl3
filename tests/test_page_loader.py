from pathlib import Path

from page_loader import download
from page_loader.page_loader import normalize_url

fixtures_path = Path('tests/fixtures/')


def _fake_download_images(requests_mock):
    image_mocks = [
        {
            'url': (
                'http://www.sub.example.com/image/image1.png'
            ),
            'response': {
                'content-type': 'image/png',
                'content': b'image1',
            },
        },
        {
            'url': (
                'http://www.sub.example.com/path/to_something/'
                '_image/image2.png'
            ),
            'response': {
                'content-type': 'image/png',
                'content': b'image2',
            },
        },
        {
            'url': (
                'http://www.sub.example.com/path/_images/image3.png'
            ),
            'response': {
                'content-type': 'image/png',
                'content': b'image3',
            },
        },
        {
            'url': 'http://www.sub.example.com/image/image4.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image4',
            },
        },
        {
            'url': 'https://www.sub.example.com/image/image5.jpg',
            'response': {
                'content-type': 'image/jpg',
                'content': b'image5',
            },
        },
        {
            'url': 'http://sub2.www.sub.example.com/path/image/image6.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image6',
            },
        },
        {
            'url': 'http://sub.example.com/image/image7.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image7',
            },
        },
        {
            'url': 'http://www.example.com/image/image8.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image8',
            },
        },
        {
            'url': 'http://example.com/image/image9.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image9',
            },
        },
        {
            'url': 'http://other.com/image/image10.png',
            'response': {
                'content-type': 'image/png',
                'content': b'image10',
            },
        },
    ]
    for mock in image_mocks:
        url = mock['url']
        content = mock['response']['content']  # noqa: WPS110
        content_type = mock['response']['content-type']
        headers = {'Content-type': content_type}
        requests_mock.get(url, content=content, headers=headers)


def _fake_download(url, dir_path, requests_mock, text='data'):
    normalized_url = normalize_url(url)
    requests_mock.get(normalized_url, text=text)
    _fake_download_images(requests_mock)
    return Path(download(url, str(dir_path)))


def test_download_check_return_value(tmp_path, requests_mock):
    """Test return value from download()."""
    url = 'http://www.example.com:80/path/to_something/'
    expected_file_name = 'www-example-com-80-path-to-something.html'
    expected_file_path = tmp_path / expected_file_name
    file_path = _fake_download(url, tmp_path, requests_mock)
    assert str(file_path.resolve()) == str(expected_file_path.resolve())

    url = 'www.example.com:80/path/to_something/'
    expected_file_name = 'www-example-com-80-path-to-something.html'
    expected_file_path = tmp_path / expected_file_name
    file_path = _fake_download(url, tmp_path, requests_mock)
    assert str(file_path.resolve()) == str(expected_file_path.resolve())

    url = 'sub-sub-domen.ru.example.com/path/to_something/'
    expected_file_name = 'sub-sub-domen-ru-example-com-path-to-something.html'
    expected_file_path = tmp_path / expected_file_name
    file_path = _fake_download(url, tmp_path, requests_mock)
    assert str(file_path.resolve()) == str(expected_file_path.resolve())


def test_download_check_file(tmp_path, requests_mock):
    """
    Test download().

    Check that the file exists and its contents are correct.
    """
    url = 'https://ru.hexlet.io/courses'
    text = 'data\n'
    file_path = _fake_download(url, tmp_path, requests_mock, text)
    assert file_path.exists()
    assert file_path.read_text() == text


def test_download_images(tmp_path, requests_mock):  # noqa: WPS218
    """Test download().

    Check that the download directory exists and contains images that belong
    to the domain and subdomains.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    base_name = 'www-sub-example-com'
    expected_download_dir = (
        Path(tmp_path) / f'{base_name}-path-to-something_files'
    )
    expected_image1 = (
        expected_download_dir
        / f'{base_name}-image-image1-png.png'
    )
    expected_image2 = (
        expected_download_dir
        / f'{base_name}-path-to-something--image-image2-png.png'
    )
    expected_image3 = (
        expected_download_dir
        / f'{base_name}-path--images-image3-png.png'
    )
    expected_image4 = (
        expected_download_dir / f'{base_name}-image-image4-png.png'
    )
    expected_image5 = (
        expected_download_dir / f'{base_name}-image-image5-jpg.jpg'
    )
    expected_image6 = (
        expected_download_dir / f'sub2-{base_name}-path-image-image6-png.png'
    )

    assert not expected_download_dir.exists()
    input_html_file = (
        fixtures_path / 'input' / 'www-sub-example-com-path-to-something.html'
    )
    text = input_html_file.read_text()
    _fake_download(url, tmp_path, requests_mock, text=text)
    assert expected_download_dir.exists()
    file_count = len(list(expected_download_dir.iterdir()))
    assert file_count == 6
    assert expected_image1.exists()
    assert expected_image2.exists()
    assert expected_image3.exists()
    assert expected_image4.exists()
    assert expected_image5.exists()
    assert expected_image6.exists()
    assert expected_image1.read_bytes() == b'image1'


def test_replacement_of_original_image_urls_with_local_ones(
    tmp_path, requests_mock,
):
    """Test download().

    Check that the original links to the images of the current domain and
    subdomains have been replaced with links to local images.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    expected_html_file = (
        fixtures_path / 'output' / 'www-sub-example-com-path-to-something.html'
    )
    input_html_file = (
        fixtures_path / 'input' / 'www-sub-example-com-path-to-something.html'
    )
    expected_content = expected_html_file.read_text()
    text = input_html_file.read_text()
    file_path = _fake_download(url, tmp_path, requests_mock, text)
    assert file_path.exists()
    assert file_path.read_text() == expected_content
