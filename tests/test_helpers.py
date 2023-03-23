import re
import pytest

from cvpartner.helpers import remove_extra_whitespace, remove_ending_period, convert_developer_to_utvikler, \
    convert_enginer_to_engineer, rename_common_variations_in_dev, get_role_from_cv_roles


def test_remove_extra_whitespace():
    assert remove_extra_whitespace("   a  b  c  ") == "a b c"
    assert remove_extra_whitespace("a\tb\tc") == "a b c"


def test_remove_ending_period():
    assert remove_ending_period("abcd.") == "abcd"
    assert remove_ending_period("abcd") == "abcd"


def test_convert_developer_to_utvikler():
    assert convert_developer_to_utvikler("Developer") == "utvikler"
    assert convert_developer_to_utvikler("developer") == "utvikler"


def test_convert_enginer_to_engineer():
    assert convert_enginer_to_engineer("Enginer") == "engineer"
    assert convert_enginer_to_engineer("enginer") == "engineer"


def test_rename_common_variations_in_dev():
    assert rename_common_variations_in_dev(
        "Back End Developer") == "Backend Utvikler"
    assert rename_common_variations_in_dev(
        "Backend Developer") == "Backend Developer"


def test_get_role_from_cv_roles():
    cv_role = {'name': {'no': 'Back End Developer.'}}
    assert get_role_from_cv_roles(cv_role) == "Backend Utvikler"
    cv_role = {'name': {'no': 'Enginer'}}
    assert get_role_from_cv_roles(cv_role) == "Engineer"
    cv_role = {'name': {'no': None}}
    assert get_role_from_cv_roles(cv_role) is None
