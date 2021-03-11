# -*- coding: utf-8 -*-

from os import path as osPath  # Import path
import webbrowser

class Help(object):
    def __init__(self):
        self.path = osPath.dirname(osPath.realpath(__file__))
        self.filepath = self.path + "/Manual for Pepper Health.pdf"

    def open_pdf(self,path):
        webbrowser.open_new(path)

    def open_manual(self):
        self.open_pdf(self.filepath)
