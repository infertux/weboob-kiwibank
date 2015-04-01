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


from weboob.browser import LoginBrowser, URL, need_login
from weboob.exceptions import BrowserIncorrectPassword
from .pages import LoginPage, ListPage#, AccountHistory, CardHistory, UpdateInfoPage, AuthenticationPage


__all__ = ['KiwiBank']


class KiwiBank(LoginBrowser):
    BASEURL = 'https://www.ib.kiwibank.co.nz/mobile/'
    CERTHASH = ['5dc8be7430a2e37fab4dbfe232038ec60feed827d7ce0f68613532676962c197']
    TIMEOUT = 30

    login = URL('login/', LoginPage)
    login_error = URL('login-error/', LoginPage)
    accounts = URL('accounts/$', ListPage)
    # account = URL('/accounts/view/[0-9]+$', AccountHistory)

    # def home(self):
    #     return self.login.go()

    def do_login(self):
        self.login.stay_or_go()
        self.page.login(self.username, self.password)

        if self.login.is_here() or self.login_error.is_here():
            raise BrowserIncorrectPassword()

    @need_login
    def iter_accounts(self):
        self.accounts.stay_or_go()
        return self.page.get_accounts()

    # @need_login
    # def get_history(self, account):
    #     if account._link_id is None:
    #         return
    #     self.location(account._link_id)

    #     if self.page is None:
    #         return

    #     if self.cbPage.is_here():
    #         guesser = LinearDateGuesser(date_max_bump=timedelta(45))
    #         return self.page.get_history(date_guesser=guesser)
    #     else:
    #         return self._get_history()

    # def _get_history(self):
    #     for tr in self.page.get_history():
    #         yield tr
