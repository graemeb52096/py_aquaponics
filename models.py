"""
Goal, create an aquaponics system, that is full monitored
and controlled by a raspberry Pi

This file contains the classes we will need in order
to set up a digital aquaponics system.
"""
import datetime


def getTimeStamp():
    date = datetime.datetime.now()
    return date


class PlantNotCompatableError(Exception):
    pass


class Sensor:
    def __init__(self, value=0):
        self.value = value

    def push_value(self, value):
        self.value = value


class Temperature(Sensor):
    def get_temp(self):
        return self.value/1000


class Flow(Sensor):
    def get_flow(self):
        return self.value * 2.25


class PH(Sensor):
    def get_ph(self):
        pass


class Plant:
    """
    The plant class represents the needs
    of a plant, regarding sunlight,
    nutrients etc. for use of automated
    aquaponics growing.
    """
    DEFAULT_REQUIREMENTS = {
        'MinSunPerDay': 240,
        'MaxSunPerDay': 480,
        'PHmin': 5.8,
        'PHmax': 6.8
    }
    def __init__(self, name, requirements=DEFAULT_REQUIREMENTS):
        self.name = name
        self.requirements = requirements

    def isCompatable(self, plant):
        req = self.requirements
        if req['PHmin'] > plant.requirements['PHmax']:
            return False
        if req['PHax'] < plant.requirements['PHmin']:
            return False
        if req['MinSunPerDay'] > plant.requirements['MaxSunPerDay']:
            return False
        if req['MaxSunPerDay'] < plant.requirements['MinSunPerDay']:
            return False
        return True


class Bed:
    """
    The bed class represents our aquaponic
    grow bed.
    """
    def __init__(self, area, plants=[], flow_rate=0, ph_level=0, temp=0):
        self.area = area
        self.plants = plants
        self.requirements = None

    def isCompatable(self, plant):
        # Iterate plants in grow bed
        for p in self.plants:
            # Check that plant is compatable
            if !(p.isCompatable(plant)):
                return False
        return True

    def register_plant(self, plant):
        # Check if compatable
        if !(self.isCompatable(plant)):
            raise PlantNotCompatableError(
                "%s is not compatable with grow bed." % plant.name
            )
        else:
            self.plants.append(plant)
            self.update_bed_req()

    def push_flow(self, flow):
        self.flow_rate = flow

    def push_ph(self, ph):
        self.ph_level = ph

    def push_temp(self, temp):
        self.temp = temp

    def update_bed_req(self):
        req = (self.plants[0]).requirements
        sun_min = req['MinSunPerDay']
        sun_max = req['MaxSunPerDay']
        ph_min = req['PHmin']
        ph_max = req['PHax']
        for plant in self.plants:
            req = plant.requirements
            if sun_min < req['MinSunPerDay']:
                sun_min = req['MinSunPerDay']
            if sun_max > req['MaxSunPerDay']:
                sun_max = req['MaxSunPerDay']
            if ph_min < req['PHmin']:
                ph_min = req['PHmin']
            if ph_max > req['PHmax']:
                ph_max = req['PHmax']
        if sun_min > sun_max:
            raise PlantNotCompatableError("Plants incompatable for sunlight")
        if ph_min > ph_max:
            riase PlantNotCompatableError("Plants incompatable for ph")
        self.requirements = {
            'MinSunPerDay': sun_min,
            'MaxSunPerDay': sun_max,
            'PHmin': ph_min,
            'PHmax': ph_max
        }

    def check_ph_req(self):
        self.update_bed_req()
        req = self.requirements
        ph = self.ph_level
        if ph < req['PHmin'] or ph > req['PHmax']:
            return False
        return True


class Tank:
    """
    Fish tank
    """
    DEFAULT_REQUIREMENTS = {
        'MinTempF': 45,
        'MaxTempF': 60,
        'PHmin': 5.8,
        'PHmax': 6.8
    }
    def __init__(self, requirements=DEFAULT_REQUIREMENTS, temp=50, ph=6):
        self.requirements = requirements
        self.temp = temp
        self.ph = ph
        self.last_feed = None

    def push_temp(self, temp):
        self.temp = temp

    def push_ph(self, ph):
        self.ph = ph

    def feed(self):
        self.last_feed = getTimeStamp()

    def check_req(self):
        req = self.requirements
        if self.temp < req['MinTempF'] or self.temp > req['MaxTempF']:
            return False
        if self.ph < req['PHmin'] or self.ph > req['PHmax']:
            return False
        return True


class Light:
    """
    The light class represents our grow light
    """
    def __init__(self, lumens, state=False):
        self.lumens = lumens
        self.state = state

    def change_state(self):
        self.state = !self.state

    def is_on(self):
        return self.state


class Pump:
    """
    The pump class represents our tank to bed water pump
    """
    def __init__(self, flow_rate=0):
        self.flow = flow_rate

    def push_flow(rate):
        self.flow = rate
