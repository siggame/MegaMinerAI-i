# -*- python -*-
from base_ai import BaseAI

#  @brief Class to implement competitor code

class AI(BaseAI):
    username = "Shell AI"
    password = "password"

    #  @breif Initialization function that is ran before the game begins.
    def init(self):
        pass

    #  @breif Ending function that is ran after the game ends.
    def end(self):
        pass

    #  @breif Function is ran for each turn.
    def run(self):
        pass

    def __init__(self):
        BaseAI.__init__(self)
