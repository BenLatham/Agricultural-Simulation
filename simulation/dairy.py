"""
TODO:
    - find original references
    - find formulas for protein requirements
    - complete diet calculation

"""

import math
from simulation.models.diet_models import BreedDetails

KG_PER_LB = 0.453592
MJ_PER_MCAL = 4.184


test = "---"
def calculateDiet():
    a=0

def monthly(year, month):
    a=0
    # print (test,"cows go moo in %2d/%d" %(month, year))

def metabolisableProtein(FME, ERDP, DUP, targetYield):
    """
    Calculate the metabolisable protein in a given diet

    :param FME: Fermentable Metabolisable Energy
    :param ERDP: Effective Rumen Degradable Protein
    :param DUP: Digestible Undegradable Protein
    :param targetYield: Target Microbial Protein Yield
    :return: float, metabolisable protein

    """
    MCP = microbialCrudeProtein(FME, ERDP,targetYield)
    DMTP = digestibleMicrobialTrueProtein(MCP)
    MP = DMTP + DUP
    return MP


def microbialCrudeProtein(FME, ERDP,targetYield):
    """
    Calculate the microbial Crude protien yield of a diet

    :param FME: Fermentable Metabolisable Energy
    :param ERDP: Effective Rumen Degradable Protein
    :param targetYield: Target Microbial Protein Yield
    :return: float, microbial crude protien

    """
    if (ERDP / FME > targetYield):
        return FME*targetYield
    else:
        return ERDP

    return 0;
def digestibleMicrobialTrueProtein(MCP):
    """
    calculate digestible microbial true protien given the amount of microbial crude protein

    :param MCP: Microbial Crude Protein
    :return: float, digestible microbial true protein
    """
    MTP =   MCP * 0.75 # estimated fraction true protein
    DMTP =  MTP * 0.85 # estimated fraction digestible
    return DMTP

def intake(concentrate, weight, weekOfLactation, milkYield):
    """
    :param concentrate: as a fraction of total ration
    :param weight: of the cow in kg
    :param weekOfLactation: week of lactation
    :param milkYield: dairy cow milk yield in litres per day
    :return: dairy cow feed intake in kg dry matter per

    """
    baseIntake = 0.076+(0.013*weight)-(0.129*weekOfLactation)+4.12*math.log10(weekOfLactation)+0.14*milkYield
    if (concentrate == 0):
        return baseIntake
    return baseIntake*1.2/(1-0.404*concentrate)

def energyRequired(weight, weightChange, milkYield, fat, protein, qm):
    return energyForMaintainance(weight, qm)+ energyForMilk(milkYield, fat, protein, qm)+energyForPregnancy()+energyForWeightChange(weightChange, qm)

def energyForMaintainance(weight, qm):
    """

    :param weight: weight of the cow
    :param qm: quality of the forage component of the diet
    :return: energy required by the dairy cow for maintainance

    """
    return 1.036*(0.53*(weight/1.08)**0.67)+0.007*weight/(0.35*qm+0.503)

# NOTE: there seems to be a significant difference between
# equation from fox et al and the other function (~2x), given reasonable assumptions for protein and qm
# this may be caused by some error
def energyForMilk(milkYield, fat, protein, qm):
    """

    :param milkYield: daily milk yield kg
    :param fat: milk fat %
    :param protein: milk protein %
    :param qm:
    :return:

    """
    fat_g_perkg = fat*10
    protein_g_perkg = protein*10
    return milkYield*((0.0376*fat_g_perkg )+(0.0209*protein_g_perkg)+0.948)/(0.35*qm+0.42)

def energyForMilk_fox(milkYield, fat):
    """
    fox et.al 1992

    :param milkYield: daily milk yield kg
    :param fat: milk fat %
    :return: energy required for milk MJ/day

    """
    milkYield_LB = milkYield / KG_PER_LB
    requirement_Mcal = 0.1 * milkYield_LB * (fat+3.4)/0.65
    return requirement_Mcal*MJ_PER_MCAL


"""
MY*(F+K1)*K2
MY *(F+3.4)*2/13

MY*(F+((0.29*P)+0.948)/0.0376)*0.0376/(0.035*qm+0.42)
MY*(F +50.664893617)* 1/qm+1.2
"""

def energyForPregnancy():
    return 0

def energyForWeightChange(change, qm):
    if (change>0):
        return -1*((change*19)/(0.95*0.35*qm+0.42))
    return -1*(change*20)/0.84

def proteinRequired(weight, weightChange, milkYield, fat, protein, qm):
    return proteinForMaintainance()+proteinForMilk(milkYield,protein)+proteinForPregnancy()+proteinForPregnancy()+proteinForWeightChange()

def proteinForMaintainance(T, CBW, Q1, Q2, Q3, breed="Holstein"):
    """
    W9 is birth weight adjusted for the age of dam, kg;
    Q4 is age of dam adjustment factor for a 4 and > 10 yr old (Appendix Table 8);
    Q3 is age of dam adjustment factor for a 3-yr-old (Appendix Table 8);
    Q2 is age of dam adjustment factor for a 2.yr-old (Appendix Table 8);
    Q1 is age of dam adjustment factor for a 1-yr-old (Appendix Table 8);
    TG is day of gestation, d;
    CBW is calf birth weight (Appendix Table 8);
    FF is fetal fat accretion, g/d;
    FP is fetal protein accretion, g/d;
    FE is fetal energy, kcal/d;
    CW is cotyledon accretion rate, g/d;
    CE is cotyledon energy, kcal/d;
    CP is cotyledon protein, g/d;
    N W is placental accretion rate, g/d;
    NE is placental energy, kcal/d; CT is placental protein, g/d;
    U W is uterus accumulation, g/d;
    UE is uterine energy, kcal/d;
    Up is uterine protein, g/d;
    FE is total energy accumulation for pregnancy, kcal/d;
    RP is net pregnancy protein accretion, g/d;
    PE is metabolizable energy required for pregnancy, Mcal/d;
    WP is metabolizable protein
    required for pregnancy, g/d.

    :param T: Age of cow in days
    :param CBW:
    :param Q1:
    :param Q2:
    :param Q3:
    :param breed:
    :return:

    """
    details = BreedDetails.objects.get(breed=breed)
    if T < 0:
        raise ValueError("cow age cannot be negative")
    elif T < 731:
        w9 = CBW - details.BW_adjustment_Q1
    elif T < 1096:
        w9 = CBW - details.BW_adjustment_Q2
    else:
        raise ValueError("this function is incomplete")

    return 0

def proteinForMilk(milkYield, protein):
    """

    :param milkYield: daily milk yield kg
    :param protein: protein in milk  %
    :return: metabolisable protein g/day

    """
    milkYield_LB = milkYield/KG_PER_LB
    return 10*milkYield_LB*protein/0.65

def proteinForPregnancy():
    return 0

def proteinForWeightChange():
    return 0

def expected_yield(RHA, TL, TGEST, parity):
    """
    Ref:
    D. G. Fox*, C. J. Sniffen*p2, J. D. O'Comor*~, J. B. Russell*~+,
    and P. J. Van Soest
    A Net Carbohydrate and Protein System for Evaluating Cattle Diets:
    III. Cattle Requirements and Diet Adequacy
    J. Anim. Sci. 1992. 70:3578-3596

    :param RHA: rolling herd lactation average, kg milk/yr
    :param TL: day of lactation
    :param TGEST: day of gestation
    :return: expected yield for the given day in kg

    """

    GNRHA = RHA / KG_PER_LB # conversion to the LB milk/yr used by fox et.al.
    WC ={} # Wood's coefficients
    if parity == 1:
        A = (GNRHA * 0.01 - 20)/2.96
        WC["b"] = 0.08
        WC["c"] =-0.002
        WC["d"] =-0.001
    if parity > 1:
        A = (14 + GNRHA * 0.01)/2.96
    if parity == 2:
        WC["b"] = 0.12
        WC["c"] = -0.004
        WC["d"] = -0.002
    if parity >= 3:
        WC["b"] = 0.16
        WC["c"] = -0.005
        WC["d"] = -0.002
    Yield_LB = A * TL * WC["b"] * math.exp(WC["c"] * TL) * math.exp(WC["d"] * TGEST)
    return Yield_LB * KG_PER_LB

def milk_fat(MF,TL):
    """
    fox et.al 1992

    :param MF: peak milk fat %
    :param TL: day of lactation
    :return: milk fat % on the given day

    """
    return 1.01*MF*(((TL + 1)/71)**(-0.13))*(math.exp(0.02*((TL + 1)/7)))


def milk_fat(MP, TL):
    """
    fox et.al 1992

    :param MP: peak milk protien %
    :param TL: day of lactation
    :return: milk protein % on the given day

    """
    return 1.14*MP*(((TL + 11)/71)**(-0.12))*(math.exp(0.01*((TL + 1)/7)))

def milk_lactose(TL):
    """
    fox et.al 1992

    :param TL: day of lactation
    :return: milk lactose % on the given day

    """
    return 5 - 0.0027*TL

