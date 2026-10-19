#!/usr/bin/env python3
"""Check the two static pages without third-party Python dependencies."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.stack = []
        self.errors = []
        self.regions = {'header': [], 'footer': []}
        self.region = None
        self.feed(source)
        if self.stack:
            self.errors.append(f'Unclosed tags: {self.stack}')

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append((tag, attrs))
        if tag in self.regions:
            self.region = tag
        if self.region:
            normalized = attrs.copy()
            normalized.pop('aria-current', None)
            if 'class' in normalized:
                normalized['class'] = ' '.join(c for c in normalized['class'].split() if c != 'active')
            self.regions[self.region].append((tag, normalized))
        if tag == 'li' and (not self.stack or self.stack[-1] not in ('ul', 'ol')):
            self.errors.append('List item outside a list')
        if tag in ('ul', 'ol') and 'p' in self.stack:
            self.errors.append('List inside a paragraph')
        if self.stack and self.stack[-1] in ('ul', 'ol') and tag != 'li':
            self.errors.append(f'{tag} directly inside a list')
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in VOID:
            if not self.stack or self.stack[-1] != tag:
                self.errors.append(f'Unexpected closing tag: {tag}')
            else:
                self.stack.pop()
        if tag == self.region:
            self.region = None

    def handle_data(self, text):
        if self.region and text.strip():
            self.regions[self.region].append(('text', ' '.join(text.split())))


pages = {name: Page((ROOT / name).read_text()) for name in ('index.html', 'resume.html')}
failures = []
for name, page in pages.items():
    problems = list(page.errors)
    tags = page.tags
    ids = [a['id'] for _, a in tags if 'id' in a]
    problems += [f'Duplicate id: {key}' for key, count in Counter(ids).items() if count > 1]
    for required in ('main', 'h1', 'title'):
        if sum(t == required for t, _ in tags) != 1:
            problems.append(f'Expected one {required}')
    if sum(t == 'meta' and a.get('name') == 'description' for t, a in tags) != 1:
        problems.append('Expected one description')
    if not any(t == 'a' and a.get('aria-current') == 'page' for t, a in tags):
        problems.append('Missing active page announcement')
    for tag, attrs in tags:
        if tag == 'img' and not all(attrs.get(key) for key in ('alt', 'width', 'height')):
            problems.append('Image missing alt text or dimensions')
        if attrs.get('target') == '_blank' and 'noopener' not in attrs.get('rel', '').split():
            problems.append('External window link missing noopener')
        for key in ('src', 'href'):
            value = attrs.get(key)
            if not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            target = ROOT / unquote(url.path) if url.path else ROOT / name
            if not target.is_file():
                problems.append(f'Missing resource: {value}')
            elif url.fragment:
                if target.suffix == '.html' and target.name in pages:
                    target_ids = {a.get('id') for _, a in pages[target.name].tags}
                elif target.suffix == '.svg':
                    target_ids = {e.get('id') for e in ET.parse(target).iter()}
                else:
                    continue
                if url.fragment not in target_ids:
                    problems.append(f'Missing fragment: {value}')
    if problems:
        failures.extend(f'{name}: {problem}' for problem in problems)
    else:
        print(f'{name}: structure, metadata, local resources and fragments passed')
for region in ('header', 'footer'):
    if pages['index.html'].regions[region] != pages['resume.html'].regions[region]:
        failures.append(f'Shared {region} differs between pages')
for file in ('sitemap.xml', 'assets/images/icons.svg'):
    ET.parse(ROOT / file)
if failures:
    raise SystemExit('\n'.join(failures))
print('Shared header/footer and XML resources passed')
