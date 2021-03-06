#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests

nondestructive = pytest.mark.nondestructive
skip_selenium = pytest.mark.skip_selenium


@nondestructive
@skip_selenium
class TestLocalizations:

    def get_language_rows(self, mozwebqa):
        url = "%s/firefox/all.html" % mozwebqa.base_url
        page_response = requests.get(url)
        html = BeautifulSoup(page_response.content)
        language_rows = html.findAll('tr', id=True)
        return language_rows

    def test_that_response_url_contains_locale_code(self, mozwebqa):
        '''
           Check that bouncer links have the right locale code.
        '''
        bad_links = []
        language_rows = self.get_language_rows(mozwebqa)
        for language in language_rows:
            links = language.findAll('a')
            for link in links:
                url = link['href']
                response = requests.head(url, allow_redirects=True)
                if language['id'] not in response.url:
                    bad_links.append("Lang '%s' not in response: %s \n"
                                     % (language['id'], response.url))
        assert [] == bad_links

    def test_that_download_links_return_302(self, mozwebqa):
        '''
            Check that download links return a status 302.
        '''
        bad_links = []
        language_rows = self.get_language_rows(mozwebqa)
        for language in language_rows:
            links = language.findAll('a')
            for link in links:
                url = link['href']
                try:
                    response = requests.head(url, allow_redirects=False)
                    status = response.status_code
                    if not (300 < status <= 302):
                        bad_links.append("Lang '%s' %s link: status %s" %
                                         (language['id'], link['href'], status))
                except Exception, e:
                    bad_links.append("Exception thrown: %s url: %s" % (e, url))
        assert [] == bad_links
