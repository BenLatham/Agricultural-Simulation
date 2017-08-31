import math
from abc import ABCMeta, abstractmethod
import numpy.random as rand
import inspect

KG_PER_LB = 0.453592
MJ_PER_MCAL = 4.184

class Cow:
    __metaclass__ = ABCMeta

    def __init__(self, day_of_lactation=None, day_of_gestation=None,
                 parity=None, weight=None):
        self._day_of_lactation = day_of_lactation
        self._day_of_gestation = day_of_gestation
        self._parity = parity
        self._weight = weight

    @property
    def day_of_lactation(self):
        """days into lactation"""
        return self._day_of_lactation

    @property
    def day_of_gestation(self):
        """"days since fertilisation"""
        return self._day_of_gestation

    @property
    def parity(self):
        """parity"""
        return self._parity

    @property
    def weight(self):
        """liveweight kg"""
        return self._weight


    @property
    @abstractmethod
    def milk_yield(self):
        """expected milk yield in kg for the current day"""

    @property
    @abstractmethod
    def milk_protein(self):
        """% true protein in the milk by weight at the current day"""

    @property
    @abstractmethod
    def milk_fat(self):
        """% fat in the milk by weight at the current day"""

    @property
    @abstractmethod
    def protein_requirement(self):
        """protein requirement g/day"""

    @property
    @abstractmethod
    def energy_requirement(self):
        """energy requirement mj/day"""

    @abstractmethod
    def intake(self, diet):
        """
        food intake kg/day
        :param diet: diet parameters which impact intake (optional)
        :return: intake kg/day
        """

    @abstractmethod
    def increment(self, days=1):
        """increment the state of the cow by one day"""


class CowFox(Cow):
    """
    Cow implemented according to the formulas in:
    D. G. Fox, C. J. Sniffen, J. D. O'Comor, J. B. Russell, and P. J. Van Soest
    A Net Carbohydrate and Protein System for Evaluating Cattle Diets:
    III. Cattle Requirements and Diet Adequacy
    J. Anim. Sci. 1992. 70:3578-3596

    NOTE: implementation of the formulas is not complete, and may contain errors
    """
    def __init__(self, day_of_lactation, day_of_gestation, parity, weight, herd_average_yield, peak_fat, peak_protein):
        self._herd_average_yield = herd_average_yield  # rolling herd average milk yield kg milk/yr
        self._peak_protein = peak_protein   # %
        self._peak_fat = peak_fat  # %

        super().__init__(
            day_of_lactation=day_of_lactation,
            day_of_gestation=day_of_gestation,
            parity=parity,
            weight=weight
        )

    @property
    def milk_yield(self):
        """
        :return: expected yield for the current day in kg
        """
        d_lact = self.day_of_lactation
        d_gest = self.day_of_gestation
        parity = self.parity
        exp = math.exp
        milk_yield_lb = self._herd_average_yield / KG_PER_LB  # conversion to the LB milk/yr used by fox et.al.

        woods = {}  # Wood's coefficients
        if parity % 1 != 0 or parity < 0:
            raise ValueError("parity must have an integer value greater than 0")
        elif parity == 0:
            return 0
        elif parity == 1:
            a = (milk_yield_lb * 0.01 - 20) / 2.96
            woods["b"] = 0.08
            woods["c"] = -0.002
            woods["d"] = -0.001
        else:
            a = (14 + milk_yield_lb * 0.01) / 2.96
            if parity == 2:
                woods["b"] = 0.12
                woods["c"] = -0.004
                woods["d"] = -0.002
            if parity >= 3:
                woods["b"] = 0.16
                woods["c"] = -0.005
                woods["d"] = -0.002

        yield_lb = a * d_lact * woods["b"] * exp(woods["c"] * d_lact) * exp(woods["d"] * d_gest)
        return yield_lb * KG_PER_LB

    @property
    def protein_requirement(self):
        return self._p_milk() + self._p_preg() + self._p_weight_change() + self._p_maint()

    @property
    def energy_requirement(self): raise NotImplementedError

    @property
    def milk_protein(self):
        """
        :return: milk protein % on the given day
        """
        d_lact = self.day_of_lactation
        peak = self._peak_protein
        return 1.14 * peak * (((d_lact + 11) / 71) ** (-0.12)) * (math.exp(0.01 * ((d_lact + 1) / 7)))

    @property
    def milk_fat(self):
        """
        :return: milk fat % on the given day
        """
        d_lact = self.day_of_lactation
        peak = self._peak_fat
        return 1.01 * peak * (((d_lact + 1) / 71) ** (-0.13)) * (math.exp(0.02 * ((d_lact + 1) / 7)))

    @property
    def milk_lactose(self):
        """
        :return: milk lactose % on the given day
        """
        return 5 - 0.0027 * self.day_of_lactation

    def increment(self, days=1):
        self._day_of_lactation += days
        self._day_of_gestation += days

    def intake(self, diet): raise NotImplementedError

    def _e_milk(self):
        """
        fox et.al 1992
        :return: energy required for milk MJ/day

        """
        milk_yield_lb = self.milk_yield / KG_PER_LB
        requirement_mcal = 0.1 * milk_yield_lb * (self.milk_fat + 3.4) / 0.65
        return requirement_mcal * MJ_PER_MCAL

    def _p_milk(self):
        """
        :return: metabolisable protein g/day

        """
        milk_yield_lb = self.milk_yield / KG_PER_LB
        return 10 * milk_yield_lb * self.milk_protein / 0.65

    def _p_preg(self): raise NotImplementedError

    def _p_weight_change(self): raise NotImplementedError

    def _p_maint(self):
        """
        function incomplete
        """
        raise NotImplementedError
        # # commented out as implementation is not complete
        # T = self.age #Age of cow in days
        # CBW = self.cbw
        # Q1 = self.Q1  # age of dam adjustment factor for a 1-yr-old
        # Q2 = self.Q2  # age of dam adjustment factor for a 2.yr-old
        # Q3 = self.Q3  # age of dam adjustment factor for a 3-yr-old
        # Q4 = self.Q4  # age of dam adjustment factor for a 4 and > 10 yr old
        # breed = self.breed
        #
        #
        # details = BreedDetails.objects.get(breed=breed)
        # if T < 0:
        #     raise ValueError("cow age cannot be negative")
        # elif T < 731:
        #     w9 = CBW - details.BW_adjustment_Q1 #birth weight adjusted for the age of dam, kg;
        # elif T < 1096:
        #     w9 = CBW - details.BW_adjustment_Q2
        # else:
        #     raise ValueError("this function is incomplete")
        #
        # return 0


class CowAfrc(Cow):
    """
    Cow implemented according to the formulas in:

    AFRC(1993)
    Energy and Protein Requirements of Ruminants.
    An advisory manual prepared by the AFRC Technical Committee on Responses to Nutrients.
    CAB International, Wallingford, UK.
    """

    def __init__(self, day_of_lactation, day_of_gestation, parity, weight, yield_at_150):
        """

        :param day_of_lactation: days since calving
        :param day_of_gestation: days since insemination
        :param parity: parity
        :param weight: live weight kg
        :param yield_at_150: expected yield 150 days after calving
        """
        self._yield_at_150 = yield_at_150
        self._milk_fat = 4.06
        self._milk_protein = 3.29

        self._default_qm = 0.56
        # based on the values for maize silage of ME = 10.5 and GE = 18.9 from
        #  feedipedia https://www.feedipedia.org/content/feeds?category=13598

        self._default_concentrate = 0

        self._weight_change = 0  # TODO: implement a weight change property

        super().__init__(
            day_of_lactation=day_of_lactation,
            day_of_gestation=day_of_gestation,
            parity=parity,
            weight=weight
        )

    def increment(self, days=1):
        self._day_of_lactation += days
        self._day_of_gestation += days

    @property
    def milk_yield(self):
        """
        Morant and Gnanasakthy(1989)
        :return: expected yield for the current day in kg
        """
        exp = math.exp
        ln = math.log
        a = ln(self._yield_at_150)
        b = 3.25
        c = 0.0
        d = -0.86
        k = 0.39
        t = self.day_of_lactation
        t1 = (t-150)/100

        return exp(a - b*t1*(1+k*t1)+c*t1**2+d/t)

    @property
    def milk_protein(self):
        """% protein in the milk at the current day"""
        return self._milk_protein

    @property
    def milk_fat(self):
        """% fat in the milk at the current day"""
        return self._milk_fat

    @property
    def protein_requirement(self):
        """protein requirement g/day"""
        return (self._p_maint()
                + self._p_milk()
                + self._p_preg()
                + self._p_weight_change()
                )

    @property
    def energy_requirement(self):
        """energy requirement mj/day"""
        return self._energy_requirement()

    def intake(self, concentrate=0):
        """
        source AFRC
        :param concentrate: as a fraction of total ration
        :return: dairy cow feed intake in kg dry matter per

        """
        if concentrate is None:
            concentrate = self._default_concentrate
        week_of_lactation = int(self.day_of_lactation/7)

        base_intake = 0.076 + (0.013 * self.weight) - (0.129 * week_of_lactation) + 4.12 * math.log10(
            week_of_lactation) + 0.14 * self.milk_yield
        if concentrate == 0:
            return base_intake
        return base_intake * 1.2 / (1 - 0.404 * concentrate)

    def _energy_requirement(self, qm=None):
        if qm is None:
            qm = self._default_qm
        return (self._e_maint(qm)
                + self._e_milk(qm)
                + self._e_preg()
                + self._e_weight_change(qm)
                ) * 1.05

    def _e_maint(self, qm):
        """
        :param qm: quality of the forage component of the diet
        :return: energy required by the dairy cow for maintainance

        """
        return 1.036 * (0.53 * (self.weight / 1.08) ** 0.67) + 0.007 * self.weight / (0.35 * qm + 0.503)

    def _e_milk(self, qm):
        fat_g_perkg = self.milk_fat * 10
        protein_g_perkg = self.milk_protein * 10
        return self.milk_yield * ((0.0376 * fat_g_perkg) + (0.0209 * protein_g_perkg) + 0.948) / self._me_eff_lact(qm)

    def _e_preg(self):
        time_factor = math.exp(-0.0000576 * self.day_of_gestation)
        log10_ref_req = 151.665 - 151.64*time_factor
        ref_req = 10**log10_ref_req

        return 0.025*self._birth_weight()*(ref_req*0.0201*time_factor)

    def _birth_weight(self):
        return (self._weight ** 0.73 - 28.89) / 2.064

    def _e_weight_change(self, qm):
        if self._weight_change > 0:
            return (self._weight_change * 19) / self._me_eff_growth(qm)
        return self._weight_change * 20 / self._me_mob_eff()

    def _me_eff_lact(self, qm):
        """efficiency of ME use for lactation"""
        return 0.35 * qm + 0.42

    def _me_eff_maint(self, qm):
        """efficiency of ME use for maintenance"""
        return 0.35 * qm + 0.42

    def _me_eff_growth(self, qm):
        """efficiency of ME use for growth"""
        return self._me_eff_lact(qm)*0.95

    def _me_eff_preg(self):
        """efficiency of ME use for growth of the concepta"""
        return 0.133

    def _me_mob_eff(self):
        """efficiency of energy mobilisation"""
        return 0.84

    def _p_maint(self):
        return 2.30*self.weight**0.75

    def _p_milk(self):
        return self.milk_yield*self.milk_protein/0.68

    def _p_weight_change(self):
        if self._weight_change > 0:
            correction_factor = 0.8
            weight_term = (168.07+0.16869*self.weight + 0.0001633*self.weight**2)
            weight_change_term = (1.12-0.1223*self._weight_change)*1.695*self._weight_change
            return correction_factor*weight_term*weight_change_term
        return 138*self._weight_change

    def _p_preg(self):
        exponential_term = math.exp(-0.00262*self.day_of_gestation)
        tp = 10**(3.707 - 5.68*exponential_term)
        return 1.01*self._birth_weight() * tp * exponential_term

class Dist:
    def __init__(self, mean, standard_deviation):
        self.mean = mean
        self.stddev = standard_deviation

class Herd:
    """
    data structure containing a group of cow objects,
    and methods for creating such a group
    """
    def __init__(self, cow_type):
        self.cow_type = cow_type
        self.groups = []

    def load_from_csv(self):
        raise NotImplementedError

    def generate(self, number, **params):
        expected_params = inspect.signature(self.cow_type).parameters
        data ={}
        group =[]
        for key, value in expected_params.items():
            print(key)
            try:
                param = params[key]
            except KeyError:
                if value.default == inspect.Parameter.empty:
                    raise ValueError('"'+key+'" is a required parameter')
            data[key] = self._random_data(param, number)

        for index in range(number):
            cow_params ={key:value[index]for key, value in data.items()}
            group.append(self.cow_type(**cow_params))
        self.groups.append(group)

    def _random_data(self, dist, number):
        return rand.normal(dist.mean, dist.stddev, number)



def monthly(year, month):
    a=0
    # print (test,"cows go moo in %2d/%d" %(month, year))








"""
MY*(F+K1)*K2
MY *(F+3.4)*2/13

MY*(F+((0.29*P)+0.948)/0.0376)*0.0376/(0.035*qm+0.42)
MY*(F +50.664893617)* 1/qm+1.2
"""

