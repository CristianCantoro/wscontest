#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# (C) Pywikipedia bot team, 2006-2011
#
# Distributed under the terms of the MIT license.

__version__ = '$Id$'

import re
import pywikibot
from pywikibot import pagegenerators
from pywikibot import i18n

docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}

TEMPLATE = u"""
{{Utente:CristianCantoro/Vincitore1|%s}}
{{Utente:CristianCantoro/Vincitore2|%s}}
{{Utente:CristianCantoro/Vincitore3|%s}}
"""


class BasicBot(object):

    def __init__(self, summary):
        # init constants
        import pdb

        self.site = pywikibot.Site()
        # Set the edit summary message
        if summary:
            self.summary = summary
        else:
            self.summary = i18n.twtranslate(self.site, 'basic-changing')

    def run(self, page, winner1, winner2, winner3):
        """
        Loads the given page, does some changes, and saves it.
        """
        text = self.load(page)
        if not text:
            return

        new_text = TEMPLATE % (winner1, winner2, winner3)

        text = text.replace('<!--substme-->', new_text)

        if not self.save(text, page, self.summary):
            pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))

    def load(self, page):
        """
        Loads the given page, does some changes, and saves it.
        """
        try:
            # Load the page
            text = page.get()
        except pywikibot.NoPage:
            pywikibot.output(u"Page %s does not exist; skipping."
                             % page.title(asLink=True))
        except pywikibot.IsRedirectPage:
            pywikibot.output(u"Page %s is a redirect; skipping."
                             % page.title(asLink=True))
        else:
            return text
        return None

    def save(self, text, page, comment=None, **kwargs):
        if text != page.get():
            try:
                page.put(text, comment=comment or self.comment, **kwargs)
            except pywikibot.LockedPage:
                pywikibot.output(u"Page %s is locked; skipping."
                                 % page.title(asLink=True))
            except pywikibot.EditConflict:
                pywikibot.output(
                    u'Skipping %s because of edit conflict'
                    % (page.title()))
            except pywikibot.SpamfilterError, error:
                pywikibot.output(
                    u'Cannot change %s because of spam blacklist entry %s'
                    % (page.title(), error.url))
            else:
                return True
        return False


def main(pagename='Utente:CristianCantoro'):
    sito = pywikibot.Site('it', 'wikisource')
    page = pywikibot.Page(sito, pagename)

    bot = BasicBot('Test')

    bot.run(page=page,
            winner1='Pippo1',
            winner2='Paperino',
            winner3='Topolino'
            )


if __name__ == "__main__":

    try:
        main()
    finally:
        pywikibot.stopme()
