# -*- coding: utf-8 -*-

class Namespace:

    def __init__(self, state=None):
        if state is None:
            state = {}

        self.history = [state]
        self.state = state

    def save_checkpoint(self):
        self.history.append(self.state.copy())

    def rollback(self):
        self.state = self.history.pop()

    def has(self, key):
        return key in self.state

    def serialize(self):
        return '\n'.join(map(lambda t: '{} = {}'.format(*t),
                             zip(self.state.keys(), self.state.values())))\
            .encode('utf8')

    def __getattr__(self, key):
        return self.state[key]

    def __setattr__(self, key, value):
        if key in ['history', 'state']:
            super(Namespace, self).__setattr__(key, value)
        else:
            self.state[key] = value

    def __repr__(self):
        return 'OnboardingNamespace({})'.format(self.state)

    def __str__(self):
        return '{}'.format(self.state)
