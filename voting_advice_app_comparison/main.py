#!/usr/bin/env python

import csv
import itertools
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Iterator, List, Set


@dataclass
class Question:
    id_: str
    text: str


@dataclass
class App:
    lang: str
    questions: List[Question]


@dataclass
class Link:
    left: str
    right: str
    same: bool


def read_app(path: str) -> App:
    lang = Path(path).stem
    with open(path) as f:
        reader = csv.reader(f)
        questions = [
            Question(id_=id_, text=text_en)
            for id_, text_orig, text_en in reader
        ]
    return App(lang=lang, questions=questions)


def read_links(path: str) -> List[Link]:
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        return [
            Link(left=left, right=right, same=int(same))
            for left, right, same in reader
            if left and right
        ]


def find_question_ids_with_link(links: List[Link]) -> Set[str]:
    return set(
        itertools.chain.from_iterable(
            (link.left, link.right) for link in links
        )
    )


def format_graph(apps: List[App], links: List[Link]) -> Iterator[str]:
    q_ids_with_links = find_question_ids_with_link(links)
    yield 'digraph G {\n'
    yield '    rankdir=LR; ranksep=3; nodesep=0.05;\n'
    yield '    graph [pencolor=transparent,splines=line,fontname="Roboto"];\n'
    yield '    node [shape=box,fontname="Roboto",width=13];\n'
    yield '    edge [dir=none];\n'
    for i, app in enumerate(apps):
        yield f'    subgraph cluster{i} {{\n'
        yield f'        label="{app.lang}";\n'
        yield f'        rank=same;\n'
        for q in app.questions:
            style = ',style=filled' if q.id_ not in q_ids_with_links else ''
            align = '\\r' if i == 0 else '\\l'
            yield f'        {q.id_} [label="{q.text}{align}"{style}];\n'
        yield '    }\n'
    first_questions = next(zip(*(app.questions for app in apps)))
    first_ids = [q.id_ for q in first_questions]
    first_link = ' -> '.join(first_ids)
    yield f'    {first_link}[style=invis,weight=100];\n'
    for link in links:
        options = ' [style=dashed]' if not link.same else ''
        yield f'    {link.left}:e -> {link.right}:w{options};\n'
    yield '}\n'


def create_and_write_graph(path_links: str, paths_apps: List[str], f_out: IO):
    apps = [read_app(path) for path in paths_apps]
    links = read_links(path_links)
    graph_lines = format_graph(apps, links)
    f_out.writelines(graph_lines)


def main():
    path_links = sys.argv[1]
    paths_apps = sys.argv[2:]
    create_and_write_graph(path_links, paths_apps, sys.stdout)


if __name__ == '__main__':
    main()
