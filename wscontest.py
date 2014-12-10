#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Wikisource Contest Winner Extraction Application.

Usage:
  wikisource_contest.py
  wikisource_contest.py --password FILE
  wikisource_contest.py (-h | --help)
  wikisource_contest.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from bottle import Bottle
from bottle import run
from bottle import request
from bottle import response
from bottle import redirect
from bottle import static_file, template
from docopt import docopt
from urlparse import urlparse, parse_qs
import sys
import os
import hashlib

Contest = Bottle()

# BASEDIR is public_html/wscontest/
PASSWORD_FILE = os.path.realpath(
    os.path.join('..',
                 '..',
                 'wscontest',

                 'wscontest_config.txt'
                 ))
Contest.password_file = PASSWORD_FILE


@Contest.get('/')
def index_get():
    return static_file('index.html', root='static')


@Contest.post('/')
def index_post():

    password = request.forms.get('password')
    revid = request.forms.get('revid')
    page = request.forms.get('page')
    lang = request.forms.get('lang', 'it')
    section = request.forms.get('section', 0)

    PASSWORD = None
    print Contest.password_file
    with open(Contest.password_file, 'r+') as f:
        PASSWORD = f.read().strip('\n')

    if hashlib.sha1(password).hexdigest() == PASSWORD or password == 'test':
        from wikisource_contest import get_participants_table
        from wikisource_contest import choose_first, choose_winner

        try:
            table = get_participants_table(
                lang=lang,
                page=page,
                section=section,
                revid=revid
            )
        except ValueError:
            return template('error_table', revid=revid)

        winner1 = None
        winner2 = None
        winner3 = None
        try:
            winner1 = choose_first(table)
            winner2 = choose_winner(table, [winner1])
            winner3 = choose_winner(table, [winner1, winner2])

            assert winner1 is not None, "winner1 is None"
            assert winner2 is not None, "winner2 is None"
            assert winner3 is not None, "winner3 is None"
        except Exception as e:
            return template('error_winners',
                            winner1=winner1,
                            winner2=winner2,
                            winner3=winner3,
                            e=repr(e)
                            )

        if password != 'test':
            # from wikisource_contest import write_results
            # write_results(winner2,
            #               winner3,
            #               pagename='Wikisource:'
            #                        'Decimo_compleanno_di_Wikisource/'
            #                        'Scrutini',
            #               summary='Inserisco i vincitori'
            #               )
            return template('winners',
                            winner1=winner1,
                            winner2=winner2,
                            winner3=winner3
                            )

        else:
            return template('test')

    else:
        return template('error_password', message="Password errata")


@Contest.get('/change-password')
def change_password_form():
    return static_file('change-password.html', root='static')


@Contest.post('/change-password')
def change_password():

    PASSWORD = None
    with open(PWD_FILE, 'r+') as f:
        PASSWORD = f.read().strip('\n')

    old = request.forms.get('old')
    new = request.forms.get('new')
    repeat = request.forms.get('repeat')

    if new != repeat:
        return template('error_password',
                        message="La nuova password e la sua ripetizione "
                                "non coincidono."
                        )

    if old == new:
        return template('error_password',
                        message="La nuova password è uguale a quella "
                                "precedente."
                        )

    if hashlib.sha1(old).hexdigest() == PASSWORD:
        with open(PWD_FILE, 'w+') as out:
            out.write(hashlib.sha1(new).hexdigest())

        return template('success')
    else:
        return template('error_password', message="Password errata")


@Contest.route('/css/<css_file>')
def serve_css(css_file):
    return static_file(css_file, root='css')


@Contest.route('/images/<filepath:path>')
def serve_images(filepath):
    return static_file(filepath, root='images')


@Contest.route('/favicon.ico')
def serve_favicon():
    return static_file('wikisource.ico', root='.')


@Contest.route('/js/<filepath:path>')
def serve_js(filepath):
    return static_file(filepath, root='js')


@Contest.get('/github')
def github():
    return redirect("http://github.com/CristianCantoro/wscontest")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Wikisouce Contest 2.0')

    # parse command line arguments
    password_file = os.path.realpath(
        os.path.join('wscontest_config.txt'))
    if arguments['--password'] and arguments['FILE']:
        password_file = arguments['FILE']

    # main app
    app = Bottle()

    @app.get('/')
    @app.get('/wscontest')
    def app_index():
        return redirect('/wscontest/')

    Contest.password_file = password_file

    app.mount(prefix='/wscontest/', app=Contest)
    run(app, host='localhost', port=40000, debug=True, reloader=True)
