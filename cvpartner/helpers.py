#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional
from datetime import date


def get_highest_degree(cv) -> Optional[str]:
    # degree_mapping = {
    #     'phd': 'phd',
    #     'ph.d.': 'phd',
    #     'doktor': 'phd',
    #     'doctor': 'phd',
    #     'master': 'master',
    #     'm.a.': 'master',
    #     'm.s.': 'master',
    #     'siviløkonom': 'master',
    #     'sivilingeniør': 'master',
    #     'cand scient': 'master',
    #     'cand.sci.': 'master',
    #     'cand.mag.': 'master',
    #     'cand-mag': 'master',
    #     'm. sc.': 'master',
    #     'm.sc.': 'master',
    #     'b.a.': 'bachelor',
    #     'bs': 'bachelor',
    #     'ba': 'bachelor',
    #     'bachelor': 'bachelor',
    #     'ingeniør': 'bachelor'
    # }
    canditate_top_degrees = []

    # for edu in cv.get('educations', []):
    #     year_to = edu.get('year_to')
    #     if year_to and not year_to.strip().isnumeric():
    #         continue  # skip unfinnished education

    #     degree = edu.get('degree').get('no')
    #     if degree:
    #         degree = degree.lower()
    #     print("--", degree)

    #     if degree in degree_mapping:
    #         canditate_top_degrees.append(degree_mapping[degree])
    for edu in cv.get('educations'):
        if not edu.get('year_to') or not edu.get('year_to').strip().isnumeric():
            # skip unfinnished education
            continue

        degree = edu.get('degree').get('no')
        if degree:
            degree = degree.lower()
            if any(deg in degree for deg in ['phd', 'ph.d.', 'doktor', 'doctor']):
                canditate_top_degrees.append('phd')
            if any(deg in degree for deg in
                   ['master', 'm.a.', 'm.s.', 'siviløkonom', 'sivilingeniør',
                    'cand scient', 'cand.scient.', 'cand.mag.', 'cand-mag',
                    'm. sc', 'm.sc.']):
                canditate_top_degrees.append('master')
            if any(deg in degree for deg in ['b.a.', 'bs', 'ba', 'bachelor',
                                             'b.sc.', 'b.sc', 'ingeniør']):
                canditate_top_degrees.append('bachelor')

    # resolve
    if 'phd' in canditate_top_degrees:
        return 'phd'
    if 'master' in canditate_top_degrees:
        return 'master'
    if 'bachelor' in canditate_top_degrees:
        return 'bachelor'


def get_email(person) -> Optional[str]:
    return person.get('email')


def get_graduation_year(cv) -> Optional[int]:
    """Get the finnal year of the last compleated education

    Args:
        cv (dict): CVpartner cv object

    Returns:
        Optional[int]: the year as int (eg 2008) or None
    """
    if cv.get('educations'):
        graduation_years = [int(n.get('year_to'))
                            for n in cv.get('educations') if n.get('year_to').isnumeric()]
        if len(graduation_years) > 0:
            return int(max(graduation_years))


def get_age(cv) -> Optional[int]:
    if cv.get('born_year'):
        return date.today().year-cv.get('born_year')


def add_space_around_slash(string):
    return string.replace("/", " / ")


def clean_name(name: str) -> Optional[str]:
    # guard
    if not name:
        return name
    name = remove_ending_period(name)
    name = remove_extra_whitespace(name)
    return name


def remove_extra_whitespace(string: str) -> str:
    return ' '.join(string.split())


def remove_ending_period(string: str) -> str:
    string = string.strip()
    if string.endswith("."):
        string = string.replace(".", "")
    return string


def convert_developer_to_utvikler(string: str) -> str:
    '''substitute developer with utvikler, disregard case'''
    return re.sub('developer', 'utvikler', string, flags=re.IGNORECASE)


def convert_enginer_to_engineer(string: str) -> str:
    return re.sub('enginer', 'enginer', string, flags=re.IGNORECASE)


def rename_common_variations_in_dev(string) -> str:
    if string == 'Back End Developer':
        return 'Backend Utvikler'


def get_role_from_cv_roles(cv_role: dict, lang: str = 'no') -> str | None:
    tmp_role_string = cv_role.get('name').get(lang)
    if tmp_role_string:
        tmp_role_string = tmp_role_string.replace("-", " ")
        tmp_role_string = convert_enginer_to_engineer(tmp_role_string)
        tmp_role_string = convert_developer_to_utvikler(tmp_role_string)
        tmp_role_string = remove_ending_period(tmp_role_string)
        tmp_role_string = add_space_around_slash(tmp_role_string)
        tmp_role_string = remove_extra_whitespace(tmp_role_string)
        tmp_role_string = tmp_role_string.title().strip()

    return tmp_role_string


def get_tags_from_cv(cv, lang='no') -> list[str]:
    tags = []
    for technology in cv.get('technologies'):
        # these come in groups
        if technology.get('technology_skills'):
            for group in technology.get('technology_skills'):
                if group.get('tags').get(lang):
                    tags.append(group.get('tags').get(lang))
            # print(json.dumps(group.get('tags').get(lang), indent=2))
    return tags
