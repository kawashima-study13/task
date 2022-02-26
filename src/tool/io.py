import configparser
import json
import csv

from .dataclass import Dictm


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def load_config(path):
    def eachsection(parser, section):
        config = Dictm(parser.items(section))
        for key in config:
            try:
                config[key] = eval(config[key])
            except:
                pass
        return config

    parser = configparser.ConfigParser()
    parser.read(path)
    return Dictm({section: eachsection(parser, section)
                 for section in parser.sections()})


def load_csv(path):
    with open(path) as f:
        reader = csv.reader(f)
        return [row for row in reader]