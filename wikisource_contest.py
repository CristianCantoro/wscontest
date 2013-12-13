# -*- coding: utf-8 -*-

import re
import random
import requests
import urllib
import pywikibot
from bot import BasicBot

REGEX = "\[\[User:.*?\|(.*?)\]\]\s*\|\| (\d+)"


def get_participants_table(lang, page, section, revid):
    """
    Given a page title and the language returns the wiki text of the latest
    revision of the page
    """

    url = 'http://{}.wikisource.org/w/api.php'.format(lang)
    params = {
        'action': 'query',
        'prop': 'revisions',
        'titles': urllib.unquote(page.replace(' ', '_')),
        'rvstartid': revid,
        'rvprop': 'content',
        'rvlimit': '1',
        'format': 'json',
        'rvsection': section,
        'redirects': True
    }

    res = requests.get(url, params=params)

    if not res.ok:
        res.raise_for_status()

    json_pages = res.json()['query']['pages']

    try:
        result = json_pages.values()[0]['revisions'][0]['*']
    except:
        raise ValueError('Section {section} of page {page} does not exist on '
                         '{lang}.wikisource'.format(
                         section=section, page=page, lang=lang))

    return result


def choose_first(table):
    usuaris = [[x[0], int(x[1])] for x in re.findall(REGEX, table)]
    return max(usuaris, key=lambda el: el[1])[0]


def choose_winner(table, exclude=None):
    if not exclude:
        exclude = []

    usuaris = [[x[0], int(x[1])] for x in re.findall(REGEX, table)]

    llista = sum([[
        user[0]]*user[1]
        for user in usuaris
        if user[0] not in exclude],
        [])

    winner = random.choice(llista)

    assert winner not in exclude, "Winner already picked, cannot win 2 prizes!"

    return winner


def write_results(winner1,
                  winner2,
                  winner3,
                  pagename='Utente:CristianCantoro',
                  summary='Test'
                  ):

    sito = pywikibot.Site('it', 'wikisource')
    page = pywikibot.Page(sito, pagename)

    bot = BasicBot(summary)

    bot.run(page=page,
            winner1=winner1,
            winner2=winner2,
            winner3=winner3
            )

    pywikibot.stopme()


if __name__ == '__main__':
    table = get_participants_table(
        lang='it',
        page='Wikisource:Decimo_compleanno_di_Wikisource/Scrutini',
        section=1,
        revid=1354532)

    winner1 = choose_first(table)
    print 'winner1: ', winner1

    winner2 = choose_winner(table, [winner1])
    print 'winner2: ', winner2

    winner3 = choose_winner(table, [winner1, winner2])
    print 'winner3: ', winner3

    write_results(winner1, winner2, winner3)
