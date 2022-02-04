from pathlib import Path

import bs4
import requests

from page_loader.url import (
    is_same_domain_or_subdomain,
    normalize_url,
    url_to_name,
)


def download(url: str, output_path: str, client=requests) -> str:
    """
    Download data from *url* and save to *output_path*.

    >>> download('https://git-scm.com/docs/git-commit', '/home/user/')
    '/home/user/git-scm-com-docs-git-commit.html'

    >>> download('docs.python.org:80/3/library/', '/home/user/')
    '/home/user/docs-python-org-80-3-library.html'

    """
    normalized_url = normalize_url(url)
    response = client.get(normalized_url)
    content_type = response.headers.get('content-type', 'text/html')
    file_name = url_to_name(normalized_url, content_type)
    file_path = Path(output_path) / file_name
    files_dir_name = url_to_name(normalized_url, content_type, '_files')
    files_dir = Path(output_path) / files_dir_name
    image_paths = download_additional_files(
        normalized_url, files_dir, response.text, 'img', 'src',
    )
    new_html = replace_links(
        response.text, image_paths, str(files_dir), 'img', 'src',
    )
    link_paths = download_additional_files(
        normalized_url, str(files_dir), response.text, 'link', 'href',
    )
    new_html = replace_links(
        new_html, link_paths, str(files_dir), 'link', 'href',
    )
    file_path.write_text(new_html)

    return str(file_path.resolve())


def replace_links(
    html: str,
    new_links: dict,
    files_dir: str,
    tag_name: str,
    link_attribute_name: str,
) -> str:
    """
    Replace file links in *html* by *new_links* in tag whose name is tag_name.

    html - html text.
    new_links - Key is url. Value is absolute file path.
    files_dir - the directory where the files are stored.
    tag_name - the name of tag in which the link needs to be changed.
    link_attribute_name - link attribute name of tag
    Return new html text.
    """
    soup = bs4.BeautifulSoup(html, features='html.parser')
    tags = soup.find_all(
        lambda t: (  # noqa: WPS111
            t.name == tag_name and t.get(link_attribute_name) in new_links
        ),
    )
    for tag in tags:
        link = tag.get(link_attribute_name)
        old_path = new_links[link]
        new_src = Path(old_path).relative_to(Path(files_dir).parent)
        tag[link_attribute_name] = new_src

    return soup.prettify()


def download_file(url: str, output_path: str, client=requests) -> str:
    """Download and save file to *output_path*.

    Return full file path.
    """
    response = client.get(url)
    content_type = response.headers.get('content-type', 'text/html')
    file_name = url_to_name(response.url, content_type)
    file_path = Path(output_path) / file_name
    file_path.write_bytes(response.content)
    return str(file_path.resolve())


def download_additional_files(
    url: str,
    files_dir: str,
    html: str,
    tag_name: str,
    link_attribute_name: str,
) -> dict:
    """Download same domain or subdomain files.

    url - url from which the *html* was downloaded.
    files_dir - the directory where the files are stored.
    html - html text from which to download files.
    tag_name - the name of tag containing a link to the file.
    link_attribute_name - link attribute name of tag.

    If the *files_dir* doesn't exists, it will be created.
    Return dict. Key is file url, value is absolute file path.
    """
    normalized_url = normalize_url(url)
    soup = bs4.BeautifulSoup(html, features='html.parser')
    file_paths = {}
    if soup.find(tag_name):
        tags = soup.find_all(
            lambda t: (   # noqa: WPS111
                t.name == tag_name
                and is_same_domain_or_subdomain(
                    url, t.get(link_attribute_name),
                )
            ),
        )
        files_dir_path = Path(files_dir)
        if not files_dir_path.exists():
            files_dir_path.mkdir()

        for tag in tags:
            file_url = tag.get(link_attribute_name)
            normalized_file_url = normalize_url(
                file_url, parent_url=normalized_url,
            )
            file_path = download_file(normalized_file_url, files_dir)
            file_paths[file_url] = file_path
    return file_paths
