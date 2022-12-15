from cvpartner.helpers import get_age
import os
from datetime import datetime

import pytest

from cvpartner import CVPartner
from cvpartner.helpers import get_role_from_cv_roles


def test_class_instanciation():
    cvp = CVPartner(org='noaignite', api_key=os.environ['CVPARTNER_API_KEY'])
    assert cvp


@pytest.mark.skip(reason="This is so slow..")
def test_departmen():
    t0 = datetime.now()
    # print(f'starting: {t0}')
    cvp = CVPartner(org='noaignite', api_key=os.environ['CVPARTNER_API_KEY'])
    department = cvp.get_department()
    t1 = datetime.now()-t0
    print(f't1: {t1}')
    department2 = cvp.get_department()
    t2 = datetime.now()-t0
    print(f't2: {t2}')
    print(len(department))
    assert len(department) > 0


@pytest.mark.skip(reason="This is so slow..")  # slow, 30+ seconds
def test_departmen():
    cvp = CVPartner(org='noaignite', api_key=os.environ['CVPARTNER_API_KEY'])
    department = cvp.get_department()
    print(len(department))
    assert len(department) > 0


def test_age():
    cv = {'born_year': 1984}
    assert get_age(cv) == 39


def test_get_role_from_cv_roles_no_lang():
    cv_role = {'name': {'no': 'software developer'}}
    assert get_role_from_cv_roles(cv_role) == 'Software Developer'


def test_get_role_from_cv_roles_no_lang():
    cv_role = {'name': {'no': 'software developer.'}}
    assert get_role_from_cv_roles(cv_role) == 'Software Developer'


def test_get_role_from_cv_roles_en_lang():
    cv_role = {'name': {'en': 'software developer'}}
    assert get_role_from_cv_roles(cv_role, lang='en') == 'Software Developer'


def test_get_role_from_cv_roles_with_dot():
    cv_role = {'name': {'no': 'software developer.'}}
    assert get_role_from_cv_roles(cv_role) == 'Software Developer'


def test_get_role_from_cv_roles_with_slash():
    cv_role = {'name': {'no': 'Tech Lead/Utvikler'}}
    assert get_role_from_cv_roles(cv_role) == 'Tech Lead / Utvikler'


def test_get_role_from_cv_roles_empty_string():
    cv_role = {'name': {'no': ''}}
    assert get_role_from_cv_roles(cv_role) == ''


def test_get_role_from_cv_roles_none():
    cv_role = {'name': {}}
    assert get_role_from_cv_roles(cv_role) == None
