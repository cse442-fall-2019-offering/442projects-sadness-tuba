import pygame  # importation for pygame

import os

from View.ParentView import View


class QuitView(View):
    def __init__(self):
        super(QuitView, self).__init__()

    def isRunning(self):
        return False
