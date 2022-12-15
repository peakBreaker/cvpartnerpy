#!/usr/bin/env python
# -*- coding: utf-8 -*-

# std lib
from typing import Tuple
from typing import List
# from functools import lru_cache
# from methodtools import lru_cache

import json
import os
from time import sleep
import logging

# 3rd party
import requests

# consts
USERS_URL_BASE = "https://{org}.cvpartner.com/api/v1/users?offset={offset}"
CV_URL_BASE = "https://{org}.cvpartner.com/api/v3/cvs/{user_id}/{cv_id}"

COUNTRIES = "https://{org}.cvpartner.com/api/v1/countries"

# logger
log = logging.getLogger(__name__)


class CVPartner():

    def __init__(self, org, api_key: str, verbose: bool = False, sleep_time: float = 0.2):
        self.auth_header = {"Authorization": f'Token token="{api_key}"'}
        self.org = org
        self.verbose = verbose
        self.sleep_time = sleep_time

    def _get_users_by_offset(self, offset):
        log.debug(f'{offset} - Retreiving data from API...')
        users_url = USERS_URL_BASE.format(org=self.org, offset=offset)
        r = requests.get(users_url, headers=self.auth_header)
        return r.json()

    def get_users_from_api(self):
        offset = 0
        users = self._get_users_by_offset(offset)
        while len(users) > 0:
            offset += len(users)
            yield from users
            sleep(self.sleep_time)
            users = self._get_users_by_offset(offset)

    def get_user_cv(self, user_id, cv_id):
        log.debug(f'Retreiving user {user_id} CV {cv_id} from API...')
        cv_url = CV_URL_BASE.format(org=self.org, user_id=user_id, cv_id=cv_id)
        r = requests.get(cv_url, headers=self.auth_header)
        return r.json()

    def list_countries(self):
        url = COUNTRIES.format(org=self.org)
        r = requests.get(url, headers=self.auth_header)
        return r.json()

    def list_offices(self, country='no') -> List[Tuple[str, str]]:
        """return id and name of offices, aka departments"""
        contries = self.list_countries()
        offices = [n for n in contries if n.get(
            'code') == country][0].get('offices')
        return [(o.get('_id'), o.get('name')) for o in offices]

    # @lru_cache(maxsize=None)
    def get_department(self, office_name: str = 'Data Engineering') -> List[Tuple[dict, dict]]:
        '''Returns a tuple with (user, cv) in a list'''
        the_dep = []
        all_users = self.get_users_from_api()
        for user in all_users:
            if user['office_name'] == office_name:
                cv = self.get_user_cv(user['user_id'], user['default_cv_id'])
                the_dep.append((user, cv))
        return the_dep
