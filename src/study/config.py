# -*- coding: utf-8 -*-

import os
import codecs

DEFAULT_CONFIG_PATHS = [
    '$XDG_CONFIG_HOME/.studyrc',
    '/etc/studyrc'
]

class EnvironmentVariableMissing(RuntimeError):
    pass

class IncompleteConfiguration(RuntimeError):

    def __init__(self, config_key, description=None):
        if description is None:
            description = ''
        else:
            description = '(reason: {})'.format(description)

        super(IncompleteConfiguration, self).__init__(
            'Incomplete configuration: missing {key} {reason}'.format(
            key=config_key, reason=description))

def read_config_from_string(data):
    lines = data.split('\n')
    kv = map(str.strip, map(lambda line: line.split('='), lines))
    return {key.lower(): value for (key, value) in kv}


def load_current_student():
    try:
        return load_current_student_from_env()
    except EnvironmentVariableMissing:
        return load_current_student_from_config()

def load_current_student_from_env():
    cur_student = os.getenv('STUDY_CURRENT_STUDENT')
    if cur_student is None:
        raise EnvironmentVariableMissing

    return cur_student

def find_config_path():
    for candidate in DEFAULT_CONFIG_PATHS:
        expanded_candidate = os.path.expandvars(candidate)
        if (os.path.exists(expanded_candidate)
            and os.path.access(expanded_candidate)):
            return expanded_candidate

    raise RuntimeError(
        'No configuration file was found.\n'
        'Please ensure that there is a config file in one of these places:\n'
        '{}'.format(', '.join(DEFAULT_CONFIG_PATHS))
    )


def load_current_student_from_config():
    config_filename = find_config_path()
    config = None
    with codecs.open(config_filename, 'r', 'utf8') as file:
        config = read_config_from_string(file.read())
    cur_student = config.get('current_student')
    if cur_student is None:
        raise IncompleteConfiguration('current_student',
                                      'You must specify who uses the tool')
