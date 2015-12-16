# -*- coding: utf-8 -*-

from functools import wraps
import enum

class StepLevel(enum.IntEnum):
    CRITICAL = 1
    OPTIONAL = 2

def onboard_step(order):
    def decorator(f):
        f._onboardStep = order
        return f

    return decorator

def onboard_description(description):
    def decorator(f):
        f._onboardDescription = description
        return f
    return decorator

def critical(f):
    f._stepLevel = StepLevel.CRITICAL
    return f

def optional(f):
    f._stepLevel = StepLevel.OPTIONAL
    return f

def order_steps(steps):
    return sorted(steps,
                  key=lambda step: step._onboardStep)

class OnboardingFailure(RuntimeError):

    def __init__(self, level, exc):
        self.level = level
        self.exc = exc


class OnboardingStep:

    def __init__(self, action):
        assert hasattr(action, '_onboardStep')
        assert hasattr(action, '_onboardDescription')
        assert hasattr(action, '_stepLevel')

        self.action = action

    def get_pretty_description(self):
        side_part = '=' * (len(self.action._onboardDescription) // 2)
        return side_part + self.action._onboardDescription + side_part


    def execute(self, namespace):
        try:
            print (self.get_pretty_description())
            self.action(namespace)
            namespace.save_checkpoint()
        except Exception as e:
            namespace.rollback()
            print ('Error occurred during this step: {}'.format(e))
            raise OnboardingFailure(self.action._stepLevel, e)
