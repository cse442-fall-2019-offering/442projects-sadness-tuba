import unittest
import Controller.MenuController as controller
import Model


class uiUnitTests(unittest.TestCase):

    def test_user_click_on_start(self):
        result = controller.option_click_event(Model.optionTuple[0], 380, 370)
        expected = "start"
        self.assertEqual(expected, result)

    def test_user_click_on_shop(self):
        result = controller.option_click_event(Model.optionTuple[1], 332, 449)
        expected = "shop"
        self.assertEqual(expected, result)

    def test_user_click_on_settings(self):
        result = controller.option_click_event(Model.optionTuple[2], 343, 527)
        expected = "settings"
        self.assertEqual(expected, result)

    def test_user_click_on_quit(self):
        result = controller.option_click_event(Model.optionTuple[3], 340, 610)
        expected = "quit"
        self.assertEqual(expected, result)

    def test_user_did_not_click_on_start(self):
        result = controller.option_click_event(Model.optionTuple[0], 0, 0)
        is_not_expected = "start"
        self.assertNotEqual(is_not_expected, result)

    def test_user_did_not_click_on_hop(self):
        result = controller.option_click_event(Model.optionTuple[1], 0, 0)
        is_not_expected = "shop"
        self.assertNotEqual(is_not_expected, result)

    def test_user_did_not_click_on_settings(self):
        result = controller.option_click_event(Model.optionTuple[2], 0, 0)
        is_not_expected = "settings"
        self.assertNotEqual(is_not_expected, result)

    def test_user_did_not_click_on_quit(self):
        result = controller.option_click_event(Model.optionTuple[3], 0, 0)
        is_not_expected = "quit"
        self.assertNotEqual(is_not_expected, result)


if __name__ == "__main__":
    unittest.main()
