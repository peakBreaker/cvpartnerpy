#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
from typing import Optional
from datetime import date

import logging
# set up logging to std out
logger = logging.getLogger(__name__)


# grab date parts from project
# put together a proper python date
def create_dates_from_project(project) -> tuple[datetime.datetime, datetime.datetime | None, int]:
    month_from = int(project.get('month_from')
                     ) if project.get('month_from') else 1
    month_to = int(project.get('month_to')) if project.get(
        'month_to') else 1
    year_from = int(project.get('year_from')) if project.get(
        'year_from') else 1
    year_to = int(project.get('year_to')) if project.get('year_to') else 1

    date_from = datetime.datetime(year=year_from, month=month_from, day=1)
    date_to = datetime.datetime(year=year_to, month=month_to, day=1)
    # compute time delta in months between from and to
    delta_months = (date_to.year - date_from.year) * \
        12 + (date_to.month - date_from.month)

    if date_to == datetime.datetime(year=1, month=1, day=1):
        # if no end date, assume it's still ongoing
        date_to = None
        delta_months = (datetime.datetime.now().year - date_from.year) * \
            12 + (datetime.datetime.now().month - date_from.month)

    return date_from, date_to, delta_months


def sort_projects_newest_to_oldest(cv) -> list[tuple[datetime.datetime, datetime.datetime | None, int, dict]]:
    projects_to_sort = []
    for project in cv.get('project_experiences'):
        date_from, date_to, delta_monts = create_dates_from_project(project)

        projects_to_sort.append((date_from, date_to, delta_monts, project))

    sorted_projects = sorted(
        projects_to_sort, key=lambda x: x[0], reverse=True)
    return sorted_projects


def get_days_since_last_finished_project(project):
    date_from, date_to, delta_months, _ = project
    if date_to is None:
        # current gig is not ended
        return 0
    else:
        return (datetime.datetime.now() - date_to).days


# Dersom feltet «fra-til» har et «til-dato» > 3mnd gammel
def newest_project_is_older_than_n_months(cv, n_months: int = 3):
    projects = sort_projects_newest_to_oldest(cv)
    if not projects:
        # no project experiences found
        return False

    date_from, date_to, delta_months, _ = projects[0]
    if date_to is None:
        # current gig is not ended
        return False
    else:
        days_in_n_months = n_months * 30
        return get_days_since_last_finished_project(projects[0]) > days_in_n_months


def get_new_certification(cv,
                          days_to_look_back: int = 365,
                          language: str = 'no') -> list:
    # print(cv.get('navn'))
    new_certifications: list = []
    for cert in cv['certifications']:
        if not cert.get('year'):
            logger.warning(
                f"{cv.get('navn')} har en uten årstall: {cert.get('name').get(language)}")
            continue  # skip certification without a year

        # print(f"{cert.get('name').get(language)}")
        _month = int(cert.get('month')) if cert.get('month') else 1
        cert_date = datetime.datetime(
            year=int(cert.get('year')),
            month=_month,
            day=1
        ).astimezone()
        now = datetime.datetime.now().astimezone()
        delta_in_days = (now - cert_date).days
        # print(f"{cert.get('name').get(language)} for {delta} dager siden")

        if delta_in_days < days_to_look_back:
            # print(f'\t --> New last {days_to_look_back} days')
            new_certifications.append(cert)

    return new_certifications


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
