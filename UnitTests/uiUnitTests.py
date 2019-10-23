import unittest

class UIUnitTests(unittest.TestCase):
    def test_cursor_move_start(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = click("start")
        expectedplayercoord = (150, 120)
        self.assertEqual(expectedplayercoord, playercoord)

    def test_cursor_move_settings(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = click("settings")
        expectedplayercoord = (150, 100)
        self.assertEqual(expectedplayercoord, playercoord)

    def test_cursor_move_quit(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = click("quit")
        expectedplayercoord = (150, 80)
        self.assertEqual(expectedplayercoord, playercoord)

def click(buttonlocation):
    if buttonlocation == "start":
        return 150, 120
    elif buttonlocation == "settings":
        return 150, 100
    elif buttonlocation == "quit":
        return 150, 80

if __name__ == "__main__":
    unittest.main()
