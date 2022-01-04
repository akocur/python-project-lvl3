from pathlib import Path

import bs4
import requests

from page_loader.url import (
    is_same_domain_or_subdomain,
    normalize_url,
    url_to_name,
)


def download(url: str, dir_output_path: str) -> str:
    """
    Download data from url and save to dir_output_path.

    >>> download('https://git-scm.com/docs/git-commit', '/home/user/')
    '/home/user/git-scm-com-docs-git-commit.html'

    >>> download('docs.python.org:80/3/library/', '/home/user/')
    '/home/user/docs-python-org-80-3-library.html'

    """
    normalized_url = normalize_url(url)
    response = requests.get(normalized_url)
    file_name = url_to_name(normalized_url, '.html')
    file_path = Path(dir_output_path) / file_name
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    if soup.find('img'):
        img_tags_of_domain_and_subdomain = filter(
            lambda img: (
                is_same_domain_or_subdomain(normalized_url, img.get('src'))
            ),
            soup.find_all('img'),
        )
        dir_for_images = (
            Path(dir_output_path) / url_to_name(normalized_url, '_files')
        )
        dir_for_images.mkdir()
        for img_tag in img_tags_of_domain_and_subdomain:
            image_url = normalize_url(
                img_tag.get('src'), parent_url=normalized_url,
            )
            image_path = download_image(image_url, dir_for_images)
            img_tag['src'] = Path(image_path).relative_to(dir_output_path)
    file_path.write_text(soup.prettify())

    return str(file_path.resolve())


def download_image(url: str, output_dir: str) -> str:
    """Download and save image to output_dir.

    Return full image path.
    """
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', 'image/png')
    _, image_type = content_type.split('/')
    extension = f'.{image_type}'
    image_name = url_to_name(response.url, extension)
    image_path = Path(output_dir) / image_name
    image_path.write_bytes(response.content)
    return str(image_path.resolve())
