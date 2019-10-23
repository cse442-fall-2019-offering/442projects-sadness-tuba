import unittest


class HitBoxTestCase(unittest.TestCase):
    def test_hitbox(self):
        self.xcor = 50
        self.ycor = 50
        self.height = 10
        bullet = (self.xcor, self.ycor, self.height)
        hitbox = (50, 50, 10)
        self.assertEqual(bullet, hitbox)

    def test_hitbox1(self):
        self.xcor = 430
        self.ycor = 50
        self.height = 20
        bullet = (self.xcor, self.ycor, self.height)
        hitbox1 = (430, 50, 20)
        self.assertEqual(bullet, hitbox1)

    def test_hitbox2(self):
        self.xcor = 128
        self.ycor = 128
        self.height = 40
        bullet = (self.xcor, self.ycor, self.height)
        hitbox2 = (128, 128, 40)
        self.assertEqual(bullet, hitbox2)

    def test_hitbox3(self):
        self.xcor = 320
        self.ycor = 420
        self.height = 100
        bullet = (self.xcor, self.ycor, self.height)
        hitbox3 = (320, 420, 100)
        self.assertEqual(bullet, hitbox3)

    def test_hitbox4(self):
        self.xcor = 300
        self.ycor = 300
        self.height = 50
        bullet = (self.xcor, self.ycor, self.height)
        hitbox4 = (300, 300, 50)
        self.assertEqual(bullet, hitbox4)


if __name__ == '__main__':
    unittest.main()
