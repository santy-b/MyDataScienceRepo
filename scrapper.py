import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


class WebScrapper(object):
    exclusion_patterns = [
        '{padding:', '{margin:', '{display:', '{font-', '{background:', '.mw-', '.portalbox-', 'list-', '.reflist',
        'function(', 'window.', 'document.', 'addEventListener(', 'setTimeout(', 'setInterval(', 'console.', '$(', 'jQuery(',
        '{"@context":"', '"@type":"', '"name":"', '"url":"', 'sameAs":"', 'author":{"@type":"',
        '<script', '<style', '<link', '<meta', '<noscript', '<footer', '<nav', '<aside',
        'scribunto', 'cachereport', 'limitreport-', 'transientcontent', 'origin":"mw',
        '<script>', '<style>', '<link>', '<meta>', '<noscript>', '<footer>', '<nav>', '<aside>'
    ]

    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup

    def find_all_html_text(self):
        return self.scrape().prettify()

    def find_all_text(self):
        all_tags = self.scrape().find_all()
        human_readable_text_list = []
        for tag in all_tags:
            tag_text = tag.get_text(strip=True)
            if tag_text and not any(pattern in tag_text for pattern in self.exclusion_patterns):
                human_readable_text_list.append(tag_text)
        concatenated_text = ' '.join(human_readable_text_list)
        return concatenated_text.strip()

    def find_all_links(self):
        valid_link_tags = self.scrape().find_all('a', href=True)
        valid_links = []
        for link in valid_link_tags:
            href = link['href']
            if href.startswith(('http://', 'https://')):
                valid_links.append(href)
        return valid_links

    def find_all_images(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        valid_image_links = []
        for link in self.scrape().find_all('a', href=True):
            url = link['href']
            for ext in image_extensions:
                if url.endswith(ext):
                    valid_image_links.append(url)
                    break
        return valid_image_links

    def find_all_headings(self):
        headings = []
        for heading in self.scrape().find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append(heading.text)
        return headings

    def find_metadata(self):
        metadata = {}
        title_tag = self.scrape().find('title')
        if title_tag:
            metadata['title'] = title_tag.text.strip()
        author_meta = self.scrape().find('meta', attrs={'name': 'author'})
        if author_meta and 'content' in author_meta.attrs:
            metadata['author'] = author_meta['content'].strip()
        return metadata

    def find_tables(self):
        tables = self.scrape().find_all('table')
        dataframes = []
        for table in tables:
            table_data = []
            rows = table.find_all('tr')
            if rows:
                for row in rows:
                    row_data = [cell.get_text(strip=True)
                                for cell in row.find_all(['th', 'td'])]
                    table_data.append(row_data)
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])
                    dataframes.append(df)
                    return dataframes
