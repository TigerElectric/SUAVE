import SUAVE
from Plane_Body import getPlane
from configurations import configSetup

def setup():
    vehicle = getPlane()
    configs = configSetup(vehicle)
    return configs

if __name__=="__main__":
    setup()