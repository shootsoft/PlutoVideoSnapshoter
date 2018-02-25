# -*- coding: utf-8 -*-

class Router(object):
    def __init__(self, app):
        self.app = app
        self.controllers = dict()
        self.topic_subscribers = dict()

    def add_ctrl(self, name, ctrl):
        self.controllers[name] = ctrl

    def go(self, ctrl_name):
        if ctrl_name in self.controllers:
            self.controllers[ctrl_name].show()

    def notify(self, topic, message):
        if topic in self.topic_subscribers:
            for ctrl in self.topic_subscribers[topic]:
                ctrl.notify(topic, message)

    def subscribe(self, topic, ctrl):
        if topic not in self.topic_subscribers:
            self.topic_subscribers[topic] = []
        self.topic_subscribers[topic].append(ctrl)
