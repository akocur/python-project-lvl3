from pathlib import Path

import pytest

from page_loader import download

fixtures_path = Path('tests/fixtures/')


@pytest.mark.parametrize(
    'url,expected_file_name',
    [
        (
            'https://sub1.example.com/path/to/',
            'sub1-example-com-path-to.html',
        ),
        (
            'https://sub1.example.com/path/to/file.html',
            'sub1-example-com-path-to-file.html',
        ),
    ],
)
def test_download_check_return_value(
    url, expected_file_name, tmp_path, requests_mock,
):
    """Test return value from download()."""
    requests_mock.get(url, text='text')
    expected_file_path = tmp_path / expected_file_name
    file_path = download(url, tmp_path)
    assert file_path == str(expected_file_path.resolve())


def test_download_check_file(tmp_path, requests_mock):
    """Test download().

    Check that the file exists and its content is correct.
    """
    url = 'https://sub1.example.com/path/to/file.html'
    text = 'data\n'
    requests_mock.get(url, text=text)
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == text


def test_replacement_of_original_urls_with_local_ones(
    tmp_path, requests_mock, image_mocks, link_mocks, script_mocks,
):
    """Test download().

    Check that the original urls to resourses of the current domain and
    subdomains have been replaced with links to local resources.
    """
    url = 'https://sub1.example.com/path/to/file.html'
    expected_html_file = fixtures_path / 'processed_file.html'
    input_html_file = fixtures_path / 'original_file.html'
    requests_mock.get(url, text=input_html_file.read_text())
    file_path = Path(download(url, tmp_path))
    assert file_path.exists()
    assert file_path.read_text() == expected_html_file.read_text()


def test_download_images(  # noqa: WPS218
    tmp_path, requests_mock, image_mocks, link_mocks, script_mocks,
):
    """Test download().

    Check that the download directory exists and contains images that belong
    to the domain and subdomains.
    """
    url = 'https://sub1.example.com/path/to/file.html'
    base_name = 'sub1-example-com'
    expected_download_dir = Path(tmp_path) / f'{base_name}-path-to-file_files'
    expected_image1 = expected_download_dir / f'{base_name}-images-image1.png'
    expected_image2 = (
        expected_download_dir / f'{base_name}-path-to--images-image2.png'
    )
    expected_image3 = (
        expected_download_dir / f'{base_name}-path-images-image3.png'
    )
    expected_image4 = expected_download_dir / f'{base_name}-images-image4.jpg'
    expected_image5 = (
        expected_download_dir / f'sub2-{base_name}-path-images-image5.png'
    )
    image6 = expected_download_dir / 'example-com-images-image6.png'
    image7 = expected_download_dir / 'other-com-images-image7.jpg'
    assert not expected_download_dir.exists()
    input_html_file = fixtures_path / 'original_file.html'
    requests_mock.get(url, text=input_html_file.read_text())
    download(url, tmp_path)
    assert expected_download_dir.exists()
    assert expected_image1.exists()
    assert expected_image2.exists()
    assert expected_image3.exists()
    assert expected_image4.exists()
    assert expected_image5.exists()
    assert not image6.exists()
    assert not image7.exists()
    assert expected_image1.read_bytes() == b'image1'


def test_download_links(  # noqa: WPS218
    tmp_path, requests_mock, image_mocks, link_mocks, script_mocks,
):
    """Test download().

    Check that the download directory exists and contains link files that
    belong to the domain and subdomains.
    """
    url = 'https://sub1.example.com/path/to/file.html'
    base_name = 'sub1-example-com'
    expected_download_dir = Path(tmp_path) / f'{base_name}-path-to-file_files'
    expected_file1 = expected_download_dir / f'{base_name}-assets-file1.css'
    expected_file2 = (
        expected_download_dir / f'{base_name}-path-to-assets-file2.css'
    )
    expected_file3 = (
        expected_download_dir / f'{base_name}-path-assets-file3.css'
    )
    expected_file4 = expected_download_dir / f'{base_name}-path-to-file4.html'
    expected_courses_file = expected_download_dir / f'{base_name}-courses.html'
    expected_file5 = expected_download_dir / f'{base_name}-assets-file5.css'
    expected_file6 = (
        expected_download_dir / f'sub2-{base_name}-path-assets-file6.css'
    )
    file7 = expected_download_dir / 'example-com-assets-file7.css'
    file8 = expected_download_dir / 'other-com-assets-file8.css'
    assert not expected_download_dir.exists()
    input_html_file = fixtures_path / 'original_file.html'
    requests_mock.get(url, text=input_html_file.read_text())
    download(url, tmp_path)
    assert expected_download_dir.exists()
    assert expected_file1.exists()
    assert expected_file2.exists()
    assert expected_file3.exists()
    assert expected_file4.exists()
    assert expected_file5.exists()
    assert expected_file6.exists()
    assert expected_courses_file.exists()
    assert not file7.exists()
    assert not file8.exists()
    assert expected_file1.read_text() == 'text'


def test_download_scripts(  # noqa: WPS218
    tmp_path, requests_mock, image_mocks, link_mocks, script_mocks,
):
    """Test download().

    Check that the download directory exists and contains script files that
    belong to the domain and subdomains.
    """
    url = 'https://sub1.example.com/path/to/file.html'
    base_name = 'sub1-example-com'
    expected_download_dir = Path(tmp_path) / f'{base_name}-path-to-file_files'
    expected_file1 = expected_download_dir / f'{base_name}-static-script1.js'
    expected_file2 = (
        expected_download_dir / f'{base_name}-path-to--static-script2.js'
    )
    expected_file3 = (
        expected_download_dir / f'{base_name}-path-static-script3.js'
    )
    expected_file4 = expected_download_dir / f'{base_name}-static-script4.js'
    expected_file5 = (
        expected_download_dir / f'sub2-{base_name}-path-static-script5.js'
    )
    file6 = expected_download_dir / 'example-com-static-script6.js'
    file7 = expected_download_dir / 'other-com-static-script7.js'
    assert not expected_download_dir.exists()
    input_html_file = fixtures_path / 'original_file.html'
    requests_mock.get(url, text=input_html_file.read_text())
    download(url, tmp_path)
    assert expected_download_dir.exists()
    assert expected_file1.exists()
    assert expected_file2.exists()
    assert expected_file3.exists()
    assert expected_file4.exists()
    assert expected_file5.exists()
    assert not file6.exists()
    assert not file7.exists()
    assert expected_file1.read_text() == 'text'
