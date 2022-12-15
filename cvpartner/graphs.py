#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

from cvpartner.helpers import get_role_from_cv_roles, get_tags_from_cv
from cvpartner.helpers import clean_name


def create_person_node(user: dict) -> tuple[str, dict]:
    return (
        clean_name(user.get('name')),
        {
            'type': 'person',
            'role': user.get('role'),
            'office_name': user.get('office_name'),
            'country_code': user.get('country_code')
        }
    )


def get_all_people_graph(noa_departments, add_roles=True, add_tags=True) -> nx.Graph:
    # make a graph of all of Noa Ignite
    nodes = []  # roles & people
    edges = []  # (node, node)
    G = nx.Graph()
    for department, people in noa_departments:
        if department not in nodes:
            nodes.append(
                (department, {'type': 'department', 'members': len(people),
                              'office_name': department})
            )

        for user, cv in people:
            user_name = clean_name(user.get('name'))
            if user_name and user_name not in nodes:
                nodes.append(
                    create_person_node(user)
                )
                # relation person -> department
                edges.append((department, user_name))

                if add_roles:
                    for role in cv.get('cv_roles'):
                        if get_role_from_cv_roles(role):
                            nodes.append(
                                (get_role_from_cv_roles(role), {'type': 'role'}))
                            edges.append(
                                (user_name, get_role_from_cv_roles(role)))
                if add_tags:
                    if get_tags_from_cv(cv):
                        # skills are nodes too
                        nodes.extend([(cv_tag, {'type': 'skill'})
                                      for cv_tag in get_tags_from_cv(cv)])

                        # and user-> skill are egdes
                        edges.extend([(user_name, t)
                                     for t in get_tags_from_cv(cv)])

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


def get_roles_and_people_graph(department) -> nx.Graph:
    # what would be a relation.
    # tech skill?
    # roles? .. yeah. probly roles..
    nodes = []  # roles & people
    edges = []  # (node, node)
    G = nx.Graph()

    for user, cv in department:
        if cv.get('name') and cv.get('name') not in nodes:
            nodes.append(
                create_person_node(user)
            )

        for role in cv.get('cv_roles'):
            if get_role_from_cv_roles(role):
                nodes.append(
                    (get_role_from_cv_roles(role), {'type': 'title'}))
                edges.append((cv.get('name'), get_role_from_cv_roles(role)))

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    # print(G)
    # nx.draw(G)
    return G


def get_skills_and_people_graph(department) -> nx.Graph:
    # what would be a relation.
    # tech skill?
    # roles? .. yeah. probly roles..
    nodes = []  # roles & people
    edges = []  # (node, node)
    G = nx.Graph()

    for user, cv in department:

        # people are nodes
        user_name = cv.get('name')
        if user_name and user_name not in nodes:
            nodes.append(
                create_person_node(user)
            )

        if get_tags_from_cv(cv):
            # skills are nodes too
            nodes.extend([(cv_tag, {'type': 'skill'})
                         for cv_tag in get_tags_from_cv(cv)])

            # and user-> skill are egdes
            edges.extend([(user_name, t) for t in get_tags_from_cv(cv)])

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    # print(G)
    # nx.draw(G)
    return G
