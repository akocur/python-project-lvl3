from pathlib import Path

import bs4
import requests

from page_loader.url import (
    is_same_domain_or_subdomain,
    normalize_url,
    url_to_name,
)


def download(url: str, output_path: str, client=requests) -> str:
    """Download data from *url* and save to *output_path*."""
    url = normalize_url(url)
    response = client.get(url)
    content_type = response.headers.get('content-type', 'text/html')
    file_path = Path(output_path) / url_to_name(url, content_type)
    files_dir = str(
        Path(output_path) / url_to_name(url, content_type, '_files'),
    )
    link_tags = (('img', 'src'), ('link', 'href'), ('script', 'src'))
    new_links = []
    for tag_name, link_attribute_name in link_tags:
        local_links = download_additional_files(
            url, files_dir, response.text, tag_name, link_attribute_name,
        )
        new_links.append((tag_name, link_attribute_name, local_links))
    file_path.write_text(replace_links(response.text, new_links, files_dir))

    return str(file_path.resolve())


def replace_links(html: str, new_links: list, files_dir: str) -> str:
    """
    Replace file links in *html* from *new_links*.

    html - html text.
    new_links - list of tuple (tag_name, link_attribute_name, new_links).
    files_dir - the directory where the files are stored.
    Return new html text.
    """
    soup = bs4.BeautifulSoup(html, features='html.parser')
    for tag_name, link_attribute_name, links in new_links:
        tags = soup.find_all(tag_name)
        for tag in tags:
            link = tag.get(link_attribute_name)
            if link not in links:
                continue
            new_path = links[link]
            relative_path = Path(new_path).relative_to(Path(files_dir).parent)
            tag[link_attribute_name] = relative_path

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
                    normalized_url, t.get(link_attribute_name, ""),
                )
            ),
        )
        files_dir_path = Path(files_dir)
        if not files_dir_path.exists():
            files_dir_path.mkdir()

        for tag in tags:
            file_url = tag.get(link_attribute_name, '')
            normalized_file_url = normalize_url(
                file_url, parent_url=normalized_url,
            )
            file_path = download_file(normalized_file_url, files_dir)
            file_paths[file_url] = file_path
    return file_paths
