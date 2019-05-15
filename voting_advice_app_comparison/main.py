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
    text: str = ''
    has_link: bool = False
    invisible: bool = False


@dataclass
class App:
    lang: str
    questions: List[Question]


@dataclass
class Link:
    ids: List[str]
    same: bool = False


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


def find_question_ids_with_link(links: List[Link]) -> Set[str]:
    return set(itertools.chain.from_iterable(link.ids for link in links))


def add_invisible_questions(apps: List[App]):
    max_questions = max(len(app.questions) for app in apps)
    for app in apps:
        n_invisible_questions = max_questions - len(app.questions)
        last_id = app.questions[-1].id_
        for i in range(n_invisible_questions):
            app.questions.append(
                Question(id_=f'{last_id}_invis_{i}', invisible=True)
            )


def render_template(package: List[str], f_out: IO, **context):
    environment = Environment(loader=PackageLoader(*package[:-1]))
    template = environment.get_template(package[-1])
    stream = template.stream(**context)
    f_out.writelines(stream)


def create_and_write_graph(path_links: str, paths_apps: List[str], f_out: IO):
    links = read_links(path_links)
    q_ids_with_links = find_question_ids_with_link(links)
    apps = [read_app(path, q_ids_with_links) for path in paths_apps]
    add_invisible_questions(apps)
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
