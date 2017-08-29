#!/usr/bin/env python
from collections import OrderedDict
from csv import reader
from json import load
from pathlib import Path
from re import split

from .parse import pass_parser


def string2alias(alias):
    return filter(None, split("[.]", alias))


def _csv2dict(path, headers, parse, sep):
    path, headers, parser = Path(str(path)).resolve(), bool(headers), pass_parser(parse)
    dict_ = OrderedDict()

    with path.open("r") as read_file:
        csv_reader = reader(read_file, sep=sep)

        if headers:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    headers = list(row)
                    for header in headers:
                        dict_[header] = []

                else:
                    for col_index, cell in enumerate(row):
                        dict_[headers[col_index]].append(parser(cell))

        else:
            for row_index, row in enumerate(csv_reader):

                if row == 0:
                    for col_index, cell in enumerate(row):
                        dict_[col_index] = [parser(cell)]

                else:
                    for col_index, cell in enumerate(row):
                        dict_[col_index].append(parser(cell))

        return dict_


def _csv2list(path, headers, parse, sep=","):
    path, headers, parser = Path(str(path)).resolve(), bool(headers), pass_parser(parse)
    list_ = list()

    with path.open("r") as read_file:
        csv_reader = reader(read_file, sep=sep)

        if headers:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    headers = list(row)

                else:
                    list_.append({headers[col_index]: parser(cell) for col_index, cell in enumerate(row)})

        else:
            for row_index, row in enumerate(csv_reader):
                list_.append(map(parser, row))

        return list_


def csv2dict(path, headers=True, parse=True):
    return _csv2dict(path, headers, parse, ",")


def csv2list(path, headers=True, parse=True):
    return _csv2list(path, headers, parse, ",")


def json2object(path, alias=None):
    path, alias = Path(str(path)).resolve(), string2alias(alias)

    with path.open("r") as file_io:
        json = load(file_io)

    for key in alias:
        try:
            json = json[key]
        except (KeyError, IndexError):
            return None

    return json


def tsv2dict(path, headers=True, parse=True):
    return _csv2dict(path, headers, parse, "\t")


def tsv2list(path, headers=True, parse=True):
    return _csv2list(path, headers, parse, "\t")


