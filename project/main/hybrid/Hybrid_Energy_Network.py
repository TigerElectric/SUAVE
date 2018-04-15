import SUAVE
from SUAVE.Core import Units, Data
from Parallel_Battery_Propeller_Hybrid_Interp import Series_Battery_Propeller_Hybrid_Interp
from Internal_Combustion_Engine import Internal_Combustion_Engine
from SUAVE.Methods.Propulsion.electric_motor_sizing import size_from_kv
from SUAVE.Methods.Power.Battery.Sizing import initialize_from_mass
from SUAVE.Methods.Propulsion import propeller_design

import numpy as np 

def battery():
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 2181.1  * Units.lb
    bat.specific_energy      = 250. *Units.Wh/Units.kg #Write expression to compute necessary power density
    bat.resistance           = 0.003
    bat.iters                = 0
    initialize_from_mass(bat,bat.mass_properties.mass)
    return bat

def motor(prop):
    mot = SUAVE.Components.Energy.Converters.Motor()
    mot.resistance           = 0.008
    mot.no_load_current      = 4.5  * Units.ampere
    mot.speed_constant       = 120. * Units['rpm'] # RPM/volt converted to (rad/s)/volt    
    mot.propeller_radius     = prop.prop_attributes.tip_radius
    mot.propeller_Cp         = prop.prop_attributes.Cp
    mot.gear_ratio           = 12. # Gear ratio
    mot.gearbox_efficiency   = .98 # Gear box efficiency
    mot.expected_current     = 160. # Expected current
    mot.mass_properties.mass = 2.0  * Units.kg
    return mot

def propeller():
    '''
    Parameters need to be added
    '''
    prop_attributes = Data()
    prop_attributes.number_blades       = 2.0
    prop_attributes.freestream_velocity = 40.0 * Units['m/s']# freestream
    prop_attributes.angular_velocity    = 150. * Units['rpm']
    prop_attributes.tip_radius          = 4.25 * Units.meters
    prop_attributes.hub_radius          = 0.05 * Units.meters
    prop_attributes.design_Cl           = 0.7
    prop_attributes.design_altitude     = 14.0 * Units.km
    prop_attributes.design_thrust       = 0.0 
    prop_attributes.design_power        = 3500.0 * Units.watts
    prop_attributes                     = propeller_design(prop_attributes)
    
    prop = SUAVE.Components.Energy.Converters.Propeller()
    prop.prop_attributes = prop_attributes
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

    network.propeller         = propeller()
    network.motor             = motor(network.propeller)
    network.esc               = esc()
    network.avionics          = avionics()
    network.payload           = payload()
    network.battery           = battery()
    network.nacelle_diameter  = 0.2 * Units.meters
    network.engine_length     = 4*Units.ft
    network.number_of_engines = 1
    network.voltage           = None
    network.combustion_engine = combustion_engine()
    network.generator         = None
    network.thrust_angle      = 0.0
    network.max_omega         = 0.0
    network.motors_per_prop   = 1
    network.number_of_props   = 1
    network.areas             = Data()
    network.areas.wetted      = 0.01*(2*np.pi*0.01/2.)
    network.tag               = 'network'

    return network

if __name__ == "__main__":
    hybrid_engine()