from View.ParentView import View
# view that quits the game


class QuitView(View):
    def __init__(self):
        super(QuitView, self).__init__()
        self.name = "Quit"
    def is_running(self):
        # returns false for is_running which ends the program
        return False
