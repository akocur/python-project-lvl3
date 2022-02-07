from pathlib import Path

import pytest

from page_loader import download
from page_loader.page_loader import normalize_url

fixtures_path = Path('tests/fixtures/')


@pytest.mark.parametrize(
    'url,expected_file_name',
    [
        (
            'http://www.example.com:80/path/to_something/',
            'www-example-com-80-path-to-something.html',
        ),
        (
            'www.example.com:80/path/to_something/',
            'www-example-com-80-path-to-something.html',
        ),
        (
            'sub-sub-domen.ru.example.com/path/to_something/',
            'sub-sub-domen-ru-example-com-path-to-something.html',
        ),
    ],
)
def test_download_check_return_value(
    url, expected_file_name, tmp_path, requests_mock,
):
    """Test return value from download()."""
    normalized_url = normalize_url(url)
    requests_mock.get(normalized_url, text='text')
    expected_file_path = tmp_path / expected_file_name
    file_path = download(url, tmp_path)
    assert file_path == str(expected_file_path.resolve())


def test_download_check_file(tmp_path, requests_mock):
    """Test download().

    Check that the file exists and its content is correct.
    """
    url = 'https://ru.hexlet.io/courses/'
    text = 'data\n'
    requests_mock.get(url, text=text)
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == text


def test_download_images(tmp_path, requests_mock, image_mocks):  # noqa: WPS218
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
        / f'{base_name}-image-image1.png'
    )
    expected_image2 = (
        expected_download_dir
        / f'{base_name}-path-to-something--image-image2.png'
    )
    expected_image3 = (
        expected_download_dir
        / f'{base_name}-path--images-image3.png'
    )
    expected_image4 = (
        expected_download_dir / f'{base_name}-image-image4.png'
    )
    expected_image5 = (
        expected_download_dir / f'{base_name}-image-image5.jpg'
    )
    expected_image6 = (
        expected_download_dir / f'sub2-{base_name}-path-image-image6.png'
    )

    assert not expected_download_dir.exists()
    input_html_file = (
        fixtures_path / 'input' / 'images.html'
    )
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    download(url, tmp_path)
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
    tmp_path, requests_mock, image_mocks,
):
    """Test download().

    Check that the original links to the images of the current domain and
    subdomains have been replaced with links to local images.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    expected_html_file = (
        fixtures_path / 'output' / 'images.html'
    )
    input_html_file = (
        fixtures_path / 'input' / 'images.html'
    )
    expected_content = expected_html_file.read_text()
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == expected_content


def test_download_links(tmp_path, requests_mock, link_mocks):  # noqa: WPS218
    """Test download().

    Check that the download directory exists and contains link files that
    belong to the domain and subdomains.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    base_name = 'www-sub-example-com'
    expected_download_dir = (
        Path(tmp_path) / f'{base_name}-path-to-something_files'
    )
    expected_file1 = (
        expected_download_dir
        / f'{base_name}-assets-file1.css'
    )
    expected_file2 = (
        expected_download_dir
        / f'{base_name}-path-to-something-assets-file2.css'
    )
    expected_file3 = (
        expected_download_dir
        / f'{base_name}-path-assets-file3.css'
    )
    expected_file4 = (
        expected_download_dir / f'{base_name}-assets-file4.css'
    )
    expected_file5 = (
        expected_download_dir / f'{base_name}-assets-file5.css'
    )
    expected_file6 = (
        expected_download_dir / f'sub2-{base_name}-path-assets-file6.css'
    )
    expected_file7 = (
        expected_download_dir / f'{base_name}-courses.html'
    )

    assert not expected_download_dir.exists()
    input_html_file = (
        fixtures_path / 'input' / 'links.html'
    )
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    download(url, tmp_path)
    assert expected_download_dir.exists()
    file_count = len(list(expected_download_dir.iterdir()))
    assert file_count == 7
    assert expected_file1.exists()
    assert expected_file2.exists()
    assert expected_file3.exists()
    assert expected_file4.exists()
    assert expected_file5.exists()
    assert expected_file6.exists()
    assert expected_file7.exists()
    assert expected_file1.read_text() == 'text'


def test_replacement_of_original_link_to_files_with_local_ones(
    tmp_path, requests_mock, link_mocks,
):
    """Test download().

    Check that the original links to the files from link tags of the current
    domain and subdomains have been replaced with links to local files.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    expected_html_file = (
        fixtures_path / 'output' / 'links.html'
    )
    input_html_file = (
        fixtures_path / 'input' / 'links.html'
    )
    expected_content = expected_html_file.read_text()
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == expected_content


def test_download_scripts(  # noqa: WPS218
    tmp_path, requests_mock, script_mocks,
):
    """Test download().

    Check that the download directory exists and contains script files that
    belong to the domain and subdomains.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    base_name = 'www-sub-example-com'
    expected_download_dir = (
        Path(tmp_path) / f'{base_name}-path-to-something_files'
    )
    expected_file1 = (
        expected_download_dir
        / f'{base_name}-script-script1.js'
    )
    expected_file2 = (
        expected_download_dir
        / f'{base_name}-path-to-something-script-script2.js'
    )
    expected_file3 = (
        expected_download_dir
        / f'{base_name}-path-scripts-script3.js'
    )
    expected_file4 = (
        expected_download_dir / f'{base_name}-script-script4.js'
    )
    expected_file5 = (
        expected_download_dir / f'{base_name}-script-script5.js'
    )
    expected_file6 = (
        expected_download_dir / f'sub2-{base_name}-path-script-script6.js'
    )

    assert not expected_download_dir.exists()
    input_html_file = (
        fixtures_path / 'input' / 'scripts.html'
    )
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    download(url, tmp_path)
    assert expected_download_dir.exists()
    file_count = len(list(expected_download_dir.iterdir()))
    assert file_count == 6
    assert expected_file1.exists()
    assert expected_file2.exists()
    assert expected_file3.exists()
    assert expected_file4.exists()
    assert expected_file5.exists()
    assert expected_file6.exists()
    assert expected_file1.read_text() == 'text'


def test_replacement_of_original_link_to_scripts_with_local_ones(
    tmp_path, requests_mock, script_mocks,
):
    """Test download().

    Check that the original links to the scripts from script tags of the
    current domain and subdomains have been replaced with links to local
    scripts.
    """
    url = 'http://www.sub.example.com/path/to_something/'
    expected_html_file = (
        fixtures_path / 'output' / 'scripts.html'
    )
    input_html_file = (
        fixtures_path / 'input' / 'scripts.html'
    )
    expected_content = expected_html_file.read_text()
    text = input_html_file.read_text()
    requests_mock.get(url, text=text)
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == expected_content
