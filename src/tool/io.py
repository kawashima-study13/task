from typing import List, Dict
import configparser
import json
import csv

from .dataclass import Pathlike, Dictm


def load_json(path: Pathlike) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)


def load_config(path: Pathlike) -> Dictm:
    def eachsection(parser, section):
        config = Dictm(parser.items(section))
        for key in config:
            try:
                config[key] = eval(config[key])
            except:
                pass
        return config

    parser = configparser.ConfigParser()
    parser.read(path, encoding='utf-8')
    return Dictm({section: eachsection(parser, section)
                 for section in parser.sections()})


def load_csv(path: Pathlike, rm_empty: bool=True) -> List:
    with open(path) as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            if rm_empty:
                row = [cell for cell in row if cell]
            rows.append(row)
    return rows
