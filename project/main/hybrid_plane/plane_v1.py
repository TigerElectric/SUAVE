"""
change battery resistance. 
"""

import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing

def battery_takeoff():
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 70.2 * Units.lb
    bat.specific_energy      = 120 * Units.Wh/Units.kg
    bat.resistance           = 0.05
    initialize_from_mass(bat,bat.mass_properties.mass)

    return bat

def battery_climb():
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 882* Units.lb
    bat.specific_energy      = 220*Units.Wh/Units.kg
    bat.resistance           = 0.05
    initialize_from_mass(bat,bat.mass_properties.mass)

    return bat

def battery_emergency():
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 1229 * Units.lb
    bat.specific_energy      = 300*Units.Wh/Units.kg
    bat.resistance           = 0.05
    initialize_from_mass(bat,bat.mass_properties.mass)
    
    return bat

def newPlane():

    vehicle  = SUAVE.Vehicle()
    vehicle.tag = "Big_Bird"

    # mass properties
    vehicle.mass_properties.max_takeoff               = 52000  * Units.kg
    vehicle.mass_properties.operating_empty           = 27837. * Units.kg
    vehicle.mass_properties.takeoff                   = 52000  * Units.kg
    vehicle.mass_properties.max_zero_fuel             = 42977. * Units.kg
    vehicle.mass_properties.cargo                     = 0.0    * Units.kg
    vehicle.mass_properties.max_payload               = 13063. * Units.kg
    vehicle.mass_properties.max_fuel                  = 12971. * Units.kg

    vehicle.mass_properties.center_of_gravity         = [18., 0, 0]
    #vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct

    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 92.00 * Units['meters**2']  
    vehicle.passengers             = 114
    vehicle.systems.control        = "fully powered"
    vehicle.systems.accessories    = "medium range"

    return vehicle

def fuselage(vehicle):

    body = SUAVE.Components.Fuselages.Fuselage()
    body.tag = 'fuselage'

    body.number_coach_seats    = vehicle.passengers
    body.seats_abreast         = 4
    body.seat_pitch            = 0.7455
    body.fineness.nose         = 2.0
    body.fineness.tail         = 3.0
    body.lengths.nose          = 6.0   * Units.meter
    body.lengths.tail          = 9.0   * Units.meter
    body.lengths.cabin         = 21.24 * Units.meter
    body.lengths.total         = 36.24 * Units.meter
    body.lengths.fore_space    = 0.    * Units.meter
    body.lengths.aft_space     = 0.    * Units.meter
    body.width                 = 3.18  * Units.meter
    body.heights.maximum       = 3.50  * Units.meter
    body.areas.side_projected  = 239.20 * Units['meters**2'] 
    body.areas.wetted          = 327.01 * Units['meters**2'] 
    body.areas.front_projected = 8.0110 * Units['meters**2']    
    body.effective_diameter    = 3.18
    body.differential_pressure = 10**5 * Units.pascal

    body.heights.at_quarter_length          = 3.35 * Units.meter
    body.heights.at_three_quarters_length   = 3.35 * Units.meter
    body.heights.at_wing_root_quarter_chord = 3.50 * Units.meter

    return body

def mainWing():

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'
    
    wing.aspect_ratio            = 10.18
    wing.sweeps.quarter_chord    = 25 * Units.deg
    wing.thickness_to_chord      = 0.1
    wing.taper                   = 0.1
    wing.span_efficiency         = 0.9
    wing.spans.projected         = 34.32 * Units.meter
    wing.chords.root             = 7.760 * Units.meter
    wing.chords.tip              = 0.782 * Units.meter
    wing.chords.mean_aerodynamic = 4.235 * Units.meter
    wing.areas.reference         = 124.862 * Units['meters**2']  
    wing.twists.root             = 4.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees
    wing.origin                  = [13.61,0,-1.27] # meters
    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True
    wing.dynamic_pressure_ratio  = 1.0

    return wing

def horizontalTail():

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 5.5
    wing.sweeps.quarter_chord    = 34.5 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.11
    wing.span_efficiency         = 0.9
    wing.spans.projected         = 11.958 * Units.meter
    wing.chords.root             = 3.030  * Units.meter
    wing.chords.tip              = 0.883  * Units.meter
    wing.chords.mean_aerodynamic = 2.3840 * Units.meter
    wing.areas.reference         = 26.0 * Units['meters**2'] 
    wing.areas.wetted            = 2.0  * wing.areas.reference
    wing.areas.exposed           = 0.8  * wing.areas.wetted
    wing.areas.affected          = 0.6  * wing.areas.reference
    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 2.0 * Units.degrees
    wing.origin                  = [31.,0,0]
    wing.vertical                = False
    wing.symmetric               = True
    wing.dynamic_pressure_ratio  = 0.9
    
    return wing

def verticalTail():

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'

    wing.aspect_ratio            = 1.7   
    wing.sweeps.quarter_chord    = 35 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.31
    wing.span_efficiency         = 0.9
    wing.spans.projected         = 5.270 * Units.meter
    wing.chords.root             = 4.70  * Units.meter
    wing.chords.tip              = 1.45  * Units.meter
    wing.chords.mean_aerodynamic = 3.36  * Units.meter
    wing.areas.reference         = 16.0  * Units['meters**2'] 
    wing.areas.wetted            = 2.0   * wing.areas.reference
    wing.areas.exposed           = 0.8   * wing.areas.wetted
    wing.areas.affected          = 0.6   * wing.areas.reference
    wing.twists.root             = 0.0   * Units.degrees
    wing.twists.tip              = 0.0   * Units.degrees
    wing.origin                  = [29.5,0,0]
    wing.vertical                = True
    wing.symmetric               = False
    wing.dynamic_pressure_ratio  = 1.0

    return wing

def engine():

    # build network
    net = Solar_Low_Fidelity()
    net.number_of_engines = 1.
    net.nacelle_diameter  = 0.05
    net.areas             = Data()
    net.areas.wetted      = 0.01*(2*np.pi*0.01/2)
    net.engine_length     = 0.01

    # Component 1 the Sun
    sun = SUAVE.Components.Energy.Processes.Solar_Radiation()
    net.solar_flux = sun

    # Component 2 the solar panels
    panel = SUAVE.Components.Energy.Converters.Solar_Panel()
    panel.ratio                = 0.9
    panel.area                 = vehicle.reference_area * panel.ratio 
    panel.efficiency           = 0.25
    panel.mass_properties.mass = panel.area*(0.60 * Units.kg)
    net.solar_panel            = panel

    # Component 3 the ESC
    esc = SUAVE.Components.Energy.Distributors.Electronic_Speed_Controller()
    esc.efficiency = 0.95 # Gundlach for brushless motors
    net.esc        = esc

    # Component 5 the Propeller
    prop = SUAVE.Components.Energy.Converters.Propeller_Lo_Fid()
    prop.propulsive_efficiency = 0.825
    net.propeller        = prop
    
    # Component 4 the Motor
    motor = SUAVE.Components.Energy.Converters.Motor_Lo_Fid()
    kv                         = 800. * Units['rpm/volt'] # RPM/volt is standard
    motor                      = size_from_kv(motor, kv)    
    motor.gear_ratio           = 1. # Gear ratio, no gearbox
    motor.gearbox_efficiency   = 1. # Gear box efficiency, no gearbox
    motor.motor_efficiency     = 0.825
    net.motor                  = motor    

    # Component 6 the Payload
    payload = SUAVE.Components.Energy.Peripherals.Payload()
    payload.power_draw           = 0. #Watts 
    payload.mass_properties.mass = 0.0 * Units.kg
    net.payload                  = payload

    # Component 7 the Avionics
    avionics = SUAVE.Components.Energy.Peripherals.Avionics()
    avionics.power_draw = 10. #Watts  
    net.avionics        = avionics      

    # Component 8 the Battery
    bat = SUAVE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion()
    bat.mass_properties.mass = 5.0  * Units.kg
    bat.specific_energy      = 250. *Units.Wh/Units.kg
    bat.resistance           = 0.003
    bat.iters                = 0
    initialize_from_mass(bat,bat.mass_properties.mass)
    net.battery              = bat

    #Component 9 the system logic controller and MPPT
    logic = SUAVE.Components.Energy.Distributors.Solar_Logic()
    logic.system_voltage  = 18.5
    logic.MPPT_efficiency = 0.95
    net.solar_logic       = logic
 
    return net

def vehicleAssembly():
    plane  = newPlane()
    plane.append_component(fuselage(plane))
    plane.append_component(mainWing())
    plane.append_component(horizontalTail())
    plane.append_component(verticalTail())
    plane.wings['vertical_stabilizer'].rudder = SUAVE.Components.Physical_Component()
    plane.append_component(engine())

    #additional objects for weight estimation
    plane.landing_gear       = SUAVE.Components.Landing_Gear.Landing_Gear()
    plane.control_systems    = SUAVE.Components.Physical_Component()
    plane.electrical_systems = SUAVE.Components.Physical_Component()
    plane.avionics           = SUAVE.Components.Energy.Peripherals.Avionics()
    plane.passenger_weights  = SUAVE.Components.Physical_Component()
    plane.furnishings        = SUAVE.Components.Physical_Component()
    plane.air_conditioner    = SUAVE.Components.Physical_Component()
    plane.fuel               = SUAVE.Components.Physical_Component()
    plane.apu                = SUAVE.Components.Physical_Component()
    plane.hydraulics         = SUAVE.Components.Physical_Component()
    plane.optionals          = SUAVE.Components.Physical_Component()

    return plane

def getPlane():
    plane = vehicleAssembly()
    return plane