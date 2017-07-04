from django.test import TestCase
from simulation.dairy import intake

class intakeTestCase(TestCase):
    def test_intake_with_concentrate(self):
        self.assertAlmostEqual(intake(0.45, 450.0, 1.0, 26.0), 13.84,2)



