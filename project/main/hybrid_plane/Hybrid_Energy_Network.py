import SUAVE
from SUAVE.Core import Units
from Parallel_Battery_Propeller_Hybrid_Interp import Series_Battery_Propeller_Hybrid_Interp
from Internal_Combustion_Engine import Internal_Combustion_Engine
from SUAVE.Methods.Propulsion.electric_motor_sizing import size_from_kv
from SUAVE.Methods.Power.Battery.Sizing import initialize_from_mass

def battery():
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 2181.1  * Units.lb
    bat.specific_energy      = 250. *Units.Wh/Units.kg #Write expression to compute necessary power density
    bat.resistance           = 0.003
    bat.iters                = 0
    initialize_from_mass(bat,bat.mass_properties.mass)
    return bat

def motor():
    mot = SUAVE.Components.Energy.Converters.Motor_Lo_Fid()
    kv                       = 800. * Units['rpm/volt'] # RPM/volt is standard
    mot                      = size_from_kv(mot, kv)    
    mot.gear_ratio           = 1. # Gear ratio, no gearbox
    mot.gearbox_efficiency   = 1. # Gear box efficiency, no gearbox
    mot.motor_efficiency     = 0.825
    return mot

def propeller():
    prop = SUAVE.Components.Energy.Converters.Propeller_Lo_Fid()
    prop.propulsive_efficiency = 0.825
    return prop

def payload():
    payload = SUAVE.Components.Energy.Peripherals.Payload()
    payload.power_draw           = 0. #Watts 
    payload.mass_properties.mass = 0.0 * Units.kg
    return payload

def esc():
    """
    Electronic_Speed_Controller
    """
    esc = SUAVE.Components.Energy.Distributors.Electronic_Speed_Controller()
    esc.efficiency = 0.95 # Gundlach for brushless motors    
    return esc

def avionics():
    avionics = SUAVE.Components.Energy.Peripherals.Avionics()
    avionics.power_draw = 23.8 #Watts , 5 Hp 
    return avionics

def combustion_engine():
    engine = Internal_Combustion_Engine()
    engine.BSFC = 0.2986
    engine.sea_level_power =  450*Units.hp
    engine.flat_rate_altitude = 20000*Units.ft
    engine.speed = 3000*Units.rpm
    return engine

# Complete hybrid engine
def hybrid_engine():
    network = Series_Battery_Propeller_Hybrid_Interp()

    network.motor             = motor()
    network.propeller         = propeller()
    network.esc               = esc()
    network.avionics          = avionics()
    network.payload           = payload()
    network.battery           = battery()
    network.nacelle_diameter  = None
    network.engine_length     = 4*Units.ft
    network.number_of_engines = 1
    network.voltage           = None
    network.combustion_engine = combustion_engine()
    network.generator         = None
    network.thrust_angle      = 0.0
    network.max_omega         = 0.0
    network.motors_per_prop   = 1
    network.number_of_props   = 1
    network.tag               = 'network'

    return network

if __name__ == "__main__":
    hybrid_engine()