import Events

notifiers = []

class Notifier:
    def __init__(self):
        self.actions = []
        self.events = []
        global notifiers
        notifiers.append(self)

    def subscribe(self, action):
        self.actions.append(action)

    def unsubscribe(self, action):
        self.actions.remove(action)

    def add_event(self, event):
        self.events.append(event)

    def refresh(self):
        processed_events = []

        for event in self.events:
            processed_events.append(event)
            for action in self.actions:
                action.do(event)

        for event in processed_events:
            self.events.remove(event)


