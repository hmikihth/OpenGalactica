from django.test import TestCase
from engine.models import Round

class RoundTestCase(TestCase):
    def setUp(self):
        Round.objects.create()

    def test_tick(self):
        """Test the tick() method"""
        round = Round.objects.first()
        original = round.turn

        self.assertGreater(original, 0, 
            "The turn has to be greater than 0"
        )

        round.tick()
        new = round.turn

        self.assertGreater(new, original, 
            "The new turn has to be greater than the original turn"
        )

        self.assertGreater(new, 1, 
            "The new turn has to be greater than 1"
        )

        self.assertEqual(new, original+1, 
            "The new turn has to be exactly 1 greater than the original turn"
        )


    def test_new_round(self):
        """Test the new_round() method"""
        round = Round.objects.first()

        original = round.number

        self.assertGreater(original, 0, 
            "The Round number has to be greater than 0"
        )

        round.tick()
        original_turn = round.turn
        round.new_round()
        
        new = round.number
        
        self.assertGreater(new, original, 
            "The new Round number has to be greater than the original"
        )

        self.assertGreater(new, 1, 
            "The new Round number has to be greater than 1"
        )

        self.assertEqual(new, original+1, 
            "The new Round number has to be exactly 1 greater than the original"
        )

        self.assertNotEqual(round.turn, original_turn, 
            "The original and the new turn cannot be the same"
        )

        self.assertEqual(round.turn, 1, 
            "The new turn has to be  exactly 1"
        )

    def test_start_calculations(self):
        round = Round.objects.first()
        round.end_calculations()
        round.start_calculations()
        self.assertTrue(round.calculate, "The calculate variable has be True")

    def test_start_calculations(self):
        round = Round.objects.first()
        round.start_calculations()
        round.end_calculations()
        self.assertFalse(round.calculate, "The calculate variable has to be False")
