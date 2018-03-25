# -*- coding: utf-8 -*-


class Controller(object):
    def __init__(self, router, view):
        self.router = router
        self.view = view

    def show(self):
        if self.view:
            self.view.show()
        else:
            raise Exception("None view")

    def hide(self):
        if self.view:
            self.view.hide()
        else:
            raise Exception("None view")

    def go(self, ctrl_name, hide_self=True):
        self.router.go(ctrl_name)
        if hide_self:
            self.hide()
