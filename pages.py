# -*- coding: utf-8 -*-

# Copyright(C) 2015 Cédric Félizard
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


from decimal import Decimal
from weboob.browser.pages import HTMLPage, LoggedPage
from weboob.capabilities.bank import Account
from weboob.tools.capabilities.bank.transactions import AmericanTransaction as Transaction

__all__ = ['LoginPage', 'ListPage']

class LoginPage(HTMLPage):
    def login(self, username, password):
        form = self.get_form(name='aspnetForm')
        form['ctl00$chi$txtUserName'] = username
        form['ctl00$chi$txtPassword'] = password
        form.submit()

class ListPage(LoggedPage, HTMLPage):
    def get_accounts(self):
        for el in self.doc.getroot().cssselect('div#content tr.row'):
            account = Account()

            balance = el.cssselect('td.Balance')[0].text
            account.balance = Decimal(Transaction.clean_amount(balance))
            account.id = el.cssselect('span')[0].text.strip()
            account.currency = u'NZD' # TODO: handle other currencies

            if el.cssselect('td.AccountName > a'):
                label_el = el.cssselect('td.AccountName > a')
            else:
                label_el = el.cssselect('td.AccountName')

            account.label = unicode(label_el[0].text.strip())

            yield account
