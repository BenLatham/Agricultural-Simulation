from django.contrib.auth.models import User
from django.test import TestCase
from simulation.dairy_herd import Herd, Dist
from simulation.dairy_group import group
from simulation.loadFeeds import types_file
from csvReader.csvReader import read_contents
from simulation.admin import Admin
import simulation.models as models
from scipy.cluster.vq import ClusterError


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

class DietTestCase(TestCase):
    def setUp(self):
        self.herd = Herd(DummyCow)
        self.herd.generate(10, e=Dist(30,2), p=Dist(34,4))

    def test_group(self):
        self.assertRaises(ClusterError, lambda: group(self.herd, 11))


class DummyCow:
    def __init__(self, e, p):
        self.energy_requirement = e
        self.protein_requirement = p
