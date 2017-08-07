from django.contrib.auth.models import User
from django.test import TestCase
from simulation.dairy import intake
from simulation.loadFeeds import types_file
from csvReader.csvReader import read_contents
from simulation.admin import Admin
import simulation.models as models


class FeedLoaderTestCase(TestCase):
    def test_types_file(self):
        contents ="grain,,0.9\ngrass,0.5,\nfat,0.1,0.2"
        processed = read_contents(contents,types_file())
        self.assertEquals(processed[0][0], "grain")
        self.assertEquals(processed[1][0], "grass")
        self.assertEquals(processed[2][0], "fat")

class AdminTestCase(TestCase):
    def setUp(self):
        user = User()
        user.save()
        scenario = models.Scenario(user=user)
        scenario.save()
        self.admin =Admin(scenario)
        self.admin.setup()

    def test_quick_test(self):
        self.assertEquals(True,True)


class IntakeTestCase(TestCase):
    def test_intake_with_concentrate(self):
        self.assertAlmostEqual(intake(0.45, 450.0, 1.0, 26.0), 13.84,2)

