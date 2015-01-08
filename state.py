import time

State = type("State", (), {})

class TimeableEvent():
    def __init__(self, ctime):
        self.ctime = ctime


class TickEvent(TimeableEvent):
    pass


class StartEvent(TimeableEvent):
    ''' push start button '''
    pass


class StopEvent:
    ''' push stop button '''
    pass


class ShortEvent(TimeableEvent):
    ''' push short pause button '''
    pass


class LongEvent(TimeableEvent):
    ''' push long pause button '''
    pass


class InitState(State):

    def __init__(self):
        self.name = 'init'


class SelectState(State):

    def __init__(self):
        self.name = 'select'

class CountableState(object):
    def __init__(self, stime):
        self.stime = stime


class TomatoState(CountableState):
    pass

class ShortState(CountableState):
    pass


class LongState(CountableState):
    pass

class LogicFMS():
    def __init__(self):
        self.state       = InitState()
        self.maxpomodoro = 10
        self.maxlong     = 5
        self.maxshort    = 3

    def set_state(self, name):
        self.state = name

    @property
    def get_state(self):
        return self.state.name

    def remining_time(self, t):
        if isinstance(self.state, CountableState):
            passed = t - self.state.stime
            if isinstance(self.state, TomatoState):
                return self.maxpomodoro - passed
            if isinstance(self.state, ShortState):
                return self.maxshort - passed
            if isinstance(self.state, LongState):
                return self.maxlong - passed

    def next_state(self, event):

        if isinstance(self.state, InitState):
            if isinstance(event, StartEvent):
                self.state = TomatoState(event.ctime)

        elif isinstance(self.state, CountableState):
            if isinstance(event, TickEvent):
                rest = self.remining_time(event.ctime)
                if rest <= 0:
                    if isinstance(self.state, TomatoState):
                        self.state = SelectState()
                    else:
                        self.state = InitState()
            elif isinstance(event, StopEvent):
                self.state = InitState()

        elif isinstance(self.state, SelectState):
            if isinstance(event, ShortEvent):
                self.state = ShortState(event.ctime)
            elif isinstance(event, LongEvent):
                self.state = LongState(event.ctime)

        # elif isinstance(self.state, ShortState):
        #     if event == TickEvent:
        #         if 6 == (TickEvent.get_time - ShortState.get_time):
        #             self.state = SelectState()
        #     elif event == StopEvent():
        #         self.state = InitState()

        # elif isinstance(self, LongState):
        #     if event == TickEvent:
        #         if 6 == (TickEvent.get_time - LongState.get_time):
        #             self.state = SelectState()
        #     elif event == StopEvent:
        #         self.state = InitState()
