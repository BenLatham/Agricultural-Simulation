"""
TODO:
    - find original references
    - find formulas for protein requirements
    - complete diet calculation


"""

import math
test = "---"

def calculateDiet():
    a=0

def monthly(year, month):
    print (test,"cows go moo in %2d/%d" %(month, year))

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
    :return: dairy cow feed intake in kg dry matter per day
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

def energyForMilk(milkYield, fat, protein, qm):
    return milkYield*((0.0376*fat)+(0.029*protein)+0.948)/(0.35*qm+0.42)

def energyForPregnancy():
    return 0

def energyForWeightChange(change, qm):
    if (change>0):
        return -1*((change*19)/(0.95*0.35*qm+0.42))
    return -1*(change*20)/0.84

def proteinRequired(weight, weightChange, milkYield, fat, protein, qm):
    return proteinForMaintainance()+proteinForMilk()+proteinForPregnancy()+proteinForPregnancy()+proteinForWeightChange()

def proteinForMaintainance():
    return 0

def proteinForMilk():
    return 0

def proteinForPregnancy():
    return 0

def proteinForWeightChange():
    return 0