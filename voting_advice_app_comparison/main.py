#!/usr/bin/env python

import csv
import sys
from typing import Dict, Iterator, List, Tuple

TQuestions = Dict[str, str]
TMapping = List[Tuple[str, str]]  # TODO: Loose connection


def read_questions(path: str) -> TQuestions:
    with open(path) as f:
        reader = csv.reader(f)
        return {id_: text_en for id_, text_orig, text_en in reader}


def read_mapping(path: str) -> TMapping:
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        return [(id_a, id_b) for id_a, id_b, same in reader if id_a and id_b]


def read_all_questions(*paths: str) -> TQuestions:
    all_questions: TQuestions = {}
    for path in paths:
        questions = read_questions(path)
        all_questions.update(questions)
    return all_questions


def format_graph(questions: TQuestions, mapping: TMapping) -> Iterator[str]:
    yield "digraph G {\n"
    yield "    ranksep=.75; rankdir=LR;\n"
    for id_a, id_b in mapping:
        yield f"    {id_a} -> {id_b};\n"
    for id_, text in questions.items():
        yield f'    {id_} [shape=box,label="{text}"];\n'
    yield "}\n"


def main():
    _, path_a, path_b, path_mapping = sys.argv
    all_questions = read_all_questions(path_a, path_b)
    mapping = read_mapping(path_mapping)
    graph_lines = format_graph(all_questions, mapping)
    sys.stdout.writelines(graph_lines)


if __name__ == "__main__":
    main()
