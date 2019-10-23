import unittest


class ShootingTestCase(unittest.TestCase):
    def test_shooting(self):
        self.xcor = 100
        self.ycor = 100
        playerCoord = (self.xcor, self.ycor)
        bulletCoord = bullet_shot(True, playerCoord[0], playerCoord[1])
        expectedBulletCoord = (self.xcor, self.ycor + 50)
        self.assertEqual(bulletCoord, expectedBulletCoord)

def bullet_shot(bulletWasShot, xcor, ycor):
    if bulletWasShot:
        return xcor, ycor + 50

if __name__ == '__main__':
    unittest.main()
