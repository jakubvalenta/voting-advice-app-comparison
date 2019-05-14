#!/usr/bin/env python

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List


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


def format_graph(apps: List[App], links: List[Link]) -> Iterator[str]:
    yield 'digraph G {\n'
    yield '    ranksep=.75; rankdir=LR;\n'
    for i, app in enumerate(apps):
        yield f'    subgraph cluster{i} {{\n'
        yield f'        label="{app.lang}";\n'
        for q in app.questions:
            yield f'        {q.id_} [shape=box,label="{q.text}"];\n'
        yield '    }\n'
    for link in links:
        style = ',style=dotted' if not link.same else ''
        yield f'    {link.left} -> {link.right} [dir=none{style}];\n'
    yield '}\n'


def main():
    _, path_a, path_b, path_links = sys.argv
    apps = [read_app(path) for path in (path_a, path_b)]
    links = read_links(path_links)
    graph_lines = format_graph(apps, links)
    sys.stdout.writelines(graph_lines)


if __name__ == '__main__':
    main()
