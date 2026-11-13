import unittest

from llm import (
    CONTACT_MESSAGE,
    COURSE_DETAILS,
    COURSE_MENU,
    INTERNSHIP_ELIGIBILITY,
    INTERNSHIP_MENU,
    MAIN_MENU,
    SERVICES_MESSAGE,
    WELCOME_MESSAGE,
    _local_response,
    menu_response,
)


class MenuResponseTests(unittest.TestCase):
    def test_root_choice_opens_correct_menu(self):
        self.assertEqual(menu_response("1"), COURSE_MENU)
        self.assertEqual(menu_response("2"), INTERNSHIP_MENU)
        self.assertEqual(menu_response("3"), SERVICES_MESSAGE)

    def test_internship_menu_can_return_to_main_menu(self):
        history = [{"sender": "bot", "message": INTERNSHIP_MENU}]
        self.assertEqual(menu_response("2", history), INTERNSHIP_ELIGIBILITY)
        self.assertEqual(menu_response("0", history), MAIN_MENU)

    def test_course_choice_uses_previous_bot_menu(self):
        history = [{"sender": "bot", "message": COURSE_MENU}]
        self.assertEqual(menu_response("1", history), COURSE_DETAILS)
        self.assertEqual(menu_response("9", history), COURSE_MENU)

    def test_zero_returns_to_main_menu(self):
        history = [{"sender": "bot", "message": COURSE_MENU}]
        self.assertEqual(menu_response("0", history), MAIN_MENU)

    def test_non_numeric_input_is_not_consumed_as_a_menu_choice(self):
        self.assertIsNone(menu_response("Tell me about Python"))

    def test_welcome_message_is_treated_as_root_menu(self):
        history = [{"sender": "bot", "message": WELCOME_MESSAGE}]
        self.assertEqual(menu_response("4", history), CONTACT_MESSAGE)

    def test_course_questions_use_published_program_details(self):
        response = _local_response("What courses do you offer?")
        self.assertIn("Full Stack Engineering + AI", response)
        self.assertIn("Data Engineering + AI", response)

    def test_fees_and_internship_questions_do_not_invent_details(self):
        fees = _local_response("How much are the course fees?")
        internships = _local_response("What internships are available?")
        self.assertIn("aren't listed", fees)
        self.assertIn("doesn't list internship openings", internships)
        self.assertIn("+91 96267 12101", fees)
        self.assertIn("info@codingbodhi.com", internships)


if __name__ == "__main__":
    unittest.main()
