#!/usr/bin/env python

import csv
import itertools
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import IO, List, Set

from jinja2 import Environment, PackageLoader


@dataclass
class Question:
    id_: str
    text: str
    has_link: bool


@dataclass
class App:
    lang: str
    questions: List[Question]


@dataclass
class Link:
    ids: List[str]
    same: bool = False
    dummy: bool = False


def read_app(path: str, q_ids_with_links: Set[str]) -> App:
    lang = Path(path).stem.replace('_', ' ')
    with open(path) as f:
        reader = csv.reader(f)
        questions = [
            Question(id_=id_, text=text_en, has_link=id_ in q_ids_with_links)
            for id_, text_orig, text_en in reader
        ]
    return App(lang=lang, questions=questions)


def read_links(path: str) -> List[Link]:
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        return [
            Link(ids=row[1:], same=bool(int(row[0])))
            for row in reader
            if all(row[1:])
        ]


def add_first_dummy_link(apps: List[App], links: List[Link]):
    first_questions = next(zip(*(app.questions for app in apps)))
    first_ids = [q.id_ for q in first_questions]
    first_link = Link(ids=first_ids, dummy=True)
    links.insert(0, first_link)


def find_question_ids_with_link(links: List[Link]) -> Set[str]:
    return set(itertools.chain.from_iterable(link.ids for link in links))


def render_template(package: List[str], f_out: IO, **context):
    environment = Environment(loader=PackageLoader(*package[:-1]))
    template = environment.get_template(package[-1])
    stream = template.stream(**context)
    f_out.writelines(stream)


def create_and_write_graph(path_links: str, paths_apps: List[str], f_out: IO):
    links = read_links(path_links)
    q_ids_with_links = find_question_ids_with_link(links)
    apps = [read_app(path, q_ids_with_links) for path in paths_apps]
    add_first_dummy_link(apps, links)
    render_template(
        ['voting_advice_app_comparison', 'templates', 'graph.gv'],
        f_out,
        apps=apps,
        links=links,
    )


def main():
    path_links = sys.argv[1]
    paths_apps = sys.argv[2:]
    create_and_write_graph(path_links, paths_apps, sys.stdout)


if __name__ == '__main__':
    main()
