from django.test import TestCase

from .models import SimulationYear, Enterprise, Income


class EnterpriseMethodTests(TestCase):

    def test_gross_margin_with_negative_value(self):
        """
        enterprise_GM should equal income + xfers_out - xfers_in - costs
        """

        negative_gm = Enterprise(total_income=1,total_xfers_out=2, total_costs=3,total_xfers_in=4)
        self.assertEqual(negative_gm.enterprise_GM(), -4, "enterprise GM not correctly identified for negative GM values" )

    def test_gross_margin_with_positive_value(self):
        """
        enterprise_GM should equal income + xfers_out - xfers_in - costs
        """

        negative_gm = Enterprise(total_income=5,total_xfers_out=6, total_costs=3,total_xfers_in=4)
        self.assertEqual(negative_gm.enterprise_GM(), 4, "enterprise GM not correctly identified for positive GM values" )

    def test_gross_margin_with_zero_value(self):
        """
        enterprise_GM should equal income + xfers_out - xfers_in - costs
        """

        negative_gm = Enterprise(total_income=5,total_xfers_out=2, total_costs=3,total_xfers_in=4)
        self.assertEqual(negative_gm.enterprise_GM(), 0, "enterprise GM not correctly identified for zero GM values" )

class IncomeMethodTests(TestCase):
    def test_income(self):
        income= Income(no_units=2, unit_price=2.5)
        self.assertEqual(income.total(), 5, "income not correctly calculated")