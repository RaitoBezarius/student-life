# -*- coding: utf-8 -*-

import tempfile
from .namespace import Namespace
from .step import order_steps, OnboardingFailure, OnboardingStep, StepLevel

class Process:

    def __init__(self, steps, state=None):
        self.load_from_state(state)
        self.steps = list(map(self.initialize_step, order_steps(steps)))

    def load_from_state(self, state=None):
        """
            Loading from state makes the Onboarding system simpler.
            The state is a Namespace with time-travelling features.
            So you can go back and edit at any point the onboarding.
        """

        self.state = Namespace(state)
        if not self.state.has('start'):
            self.state.start = 0

    def save_state(self):
        with tempfile.TemporaryFile() as fp:
            fp.write(self.state.serialize())

    def initialize_step(self, step):
        return OnboardingStep(step)

    def update_towards_next_step(self):
        self.state.start = self.state.start + 1

    def trigger_fatal_error(self, exc):
        self.save_state()
        print ('Fatal error occurred while we were setting up your studies!')
        print ('Aaah, this is a shame! Here are some details: {}'.format(exc))
        print ('Do not hesitate to fill a bug report on GitHub!')
        raise RuntimeError('Fatal error')

    def show_warning(self, exc):
        print ('Warning! We got this while setting up your stuff: {}'\
               .format(exc))
        print ('It may arise to be a bug at some point, keep it in mind!')

    def execute_step(self, step):
        try:
            step.execute(self.state)
            self.update_towards_next_step()
        except OnboardingFailure as failure:
            if failure.level == StepLevel.CRITICAL:
                self.trigger_fatal_error(failure.exc)
            else:
                self.show_warning(failure.exc)
        except Exception as e:
            self.trigger_fatal_error(e)

    def run(self):
        for step in self.steps[self.state.start:]:
            self.execute_step(step)

    def __iter__(self):
        for step in self.steps[self.state.start:]:
            self.execute_step(step)
            yield step
