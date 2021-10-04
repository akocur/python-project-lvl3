from pathlib import Path

from page_loader import download

fixtures_path = Path('tests/fixtures/')


def _fake_download(url, dir_path, requests_mock, expected_content='data'):
    requests_mock.get(url, text=expected_content)
    return Path(download(url, str(dir_path)))


def test_download(tmp_path, requests_mock):
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


def test_download_check_file(tmp_path, requests_mock):
    """
    Test download().

    Check that the file exists and its contents are correct.
    """
    url = 'https://ru.hexlet.io/courses'
    expected_content = 'data'
    file_path = _fake_download(url, tmp_path, requests_mock, expected_content)
    assert file_path.exists()
    assert file_path.read_text() == expected_content
