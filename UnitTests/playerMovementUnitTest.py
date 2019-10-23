import unittest

class PlayerCoordinateTestCase(unittest.TestCase):
    def test_player_move_left(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = moved("left",self.xcor, self.ycor)
        expectedplayercoord = (80,100)
        self.assertEqual(expectedplayercoord, playercoord)

    def test_player_move_right(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = moved("right",self.xcor, self.ycor)
        expectedplayercoord = (120,100)
        self.assertEqual(expectedplayercoord, playercoord)

    def test_player_move_up(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = moved("up",self.xcor, self.ycor)
        expectedplayercoord = (100,120)
        self.assertEqual(expectedplayercoord, playercoord)

    def test_player_move_down(self):
        self.xcor = 100
        self.ycor = 100
        playercoord = moved("down",self.xcor, self.ycor)
        expectedplayercoord = (100,80)
        self.assertEqual(expectedplayercoord, playercoord)


def moved(direction,xcor, ycor):
    if direction == "left":
        return xcor - 20, ycor
    elif direction == "right":
        return xcor + 20, ycor
    elif direction == "up":
        return xcor, ycor + 20
    elif direction == "down":
        return xcor, ycor - 20



if __name__ == '__main__':
    unittest.main()
