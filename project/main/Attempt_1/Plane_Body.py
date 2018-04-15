"""
Holds physical configuration
"""

import SUAVE
from SUAVE.Core import Units
from Hybrid_Energy_Network import hybrid_engine

def vehicle():
    vehicle  = SUAVE.Vehicle()
    vehicle.tag = "Big_Hybrid"

    # mass properties
    vehicle.mass_properties.max_takeoff               = 8338  * Units.lb
    vehicle.mass_properties.operating_empty           = 4184 * Units.lb
    vehicle.mass_properties.takeoff                   = 8338  * Units.lb
    vehicle.mass_properties.max_zero_fuel             = (8338. - 653) * Units.lb
    vehicle.mass_properties.cargo                     = 0.0    * Units.lb
    vehicle.mass_properties.max_payload               = 1320. * Units.lb
    vehicle.mass_properties.max_fuel                  = 653. * Units.lb

    vehicle.mass_properties.center_of_gravity         = [5., 0, 0] # check units and value!
    # # commented out from start:
    #vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct

    # envelope properties
    vehicle.envelope.ultimate_load = 4.4
    vehicle.envelope.limit_load    = 1.8

    # basic parameters
    vehicle.reference_area         = 308.8 * Units['ft**2']  
    vehicle.passengers             = 5
    vehicle.systems.control        = "fully powered"
    vehicle.systems.accessories    = "medium range"

    return vehicle

def fuselage(vehicle):

    body = SUAVE.Components.Fuselages.Fuselage()
    body.tag = 'fuselage'

    body.number_coach_seats    = vehicle.passengers
    # body.seats_abreast         = 4
    # body.seat_pitch            = 0.7455
    # body.fineness.nose         = 2.0
    # body.fineness.tail         = 3.0
    body.lengths.nose          = 8.0945   * Units.ft
    # body.lengths.tail          = 9.0   * Units.ft
    # body.lengths.cabin         = 21.24 * Units.ft
    body.lengths.total         = 33.5278 * Units.ft
    # body.lengths.fore_space    = 0.    * Units.ft
    # body.lengths.aft_space     = 0.    * Units.ft
    # body.width                 = 4.66 * Units.ft
    # body.heights.maximum       = 3.50  * Units.ft
    # body.areas.side_projected  = 239.20 * Units['ft**2'] 
    body.areas.wetted          = 35379.853 * Units['ft**2'] 
    # body.areas.front_projected = 8.0110 * Units['ft**2']    
    # body.effective_diameter    = 3.18
    # body.differential_pressure = 10**5 * Units.pascal

    # body.heights.at_quarter_length          = 3.35 * Units.meter
    # body.heights.at_three_quarters_length   = 3.35 * Units.meter
    # body.heights.at_wing_root_quarter_chord = 3.50 * Units.meter

    return body

def mainWing():

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'
    
    wing.aspect_ratio            = 7
    wing.sweeps.quarter_chord    = -2.045 * Units.deg
    # wing.thickness_to_chord      = 0.1
    wing.taper                   = 0.6
    # wing.span_efficiency         = 0.9
    wing.spans.projected         = 46.85 * Units.ft
    wing.chords.root             = 8.366 * Units.ft
    wing.chords.tip              = 5.019 * Units.ft
    wing.chords.mean_aerodynamic = 5.019 * Units.ft
    wing.areas.reference         = 313.56 * Units['ft**2']  
    # wing.twists.root             = 4.0 * Units.degrees
    # wing.twists.tip              = 0.0 * Units.degrees
    wing.origin                  = [7.78*Units.ft,0,-2*Units.ft] # meters
    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True
    # wing.dynamic_pressure_ratio  = 1.0

    return wing

def horizontalTail():

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 5
    wing.sweeps.quarter_chord    = 2.1469 * Units.deg
    # wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.6
    # wing.span_efficiency         = 0.9
    wing.spans.projected         = 19.31 * Units.ft
    wing.chords.root             = 4.826  * Units.ft
    wing.chords.tip              = 2.8959  * Units.ft
    wing.chords.mean_aerodynamic = 3.941 * Units.ft
    wing.areas.reference         = 74.546 * Units['ft**2'] 
    wing.areas.wetted            = 2.0  * wing.areas.reference
    wing.areas.exposed           = 0.8  * wing.areas.wetted
    wing.areas.affected          = 0.6  * wing.areas.reference
    # wing.twists.root             = 2.0 * Units.degrees
    # wing.twists.tip              = 2.0 * Units.degrees
    wing.origin                  = [28.70,0,1.25*Units.ft]
    wing.vertical                = False
    wing.symmetric               = True
    # wing.dynamic_pressure_ratio  = 0.9
    
    return wing

def verticalTail():

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'

    wing.aspect_ratio            = 1.6 
    wing.sweeps.quarter_chord    = 29.5219 * Units.deg
    # wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.4
    # wing.span_efficiency         = 0.9
    wing.spans.projected         = 6.836 * Units.ft
    wing.chords.root             = 4.70  * Units.ft
    wing.chords.tip              = 1.45  * Units.ft
    wing.chords.mean_aerodynamic = 3.36  * Units.ft
    wing.areas.reference         = 16.0  * Units['ft**2'] 
    wing.areas.wetted            = 2.0   * wing.areas.reference
    wing.areas.exposed           = 0.8   * wing.areas.wetted
    wing.areas.affected          = 0.6   * wing.areas.reference
    # wing.twists.root             = 0.0   * Units.degrees
    # wing.twists.tip              = 0.0   * Units.degrees
    wing.origin                  = [26.4239*Units.ft,0,0]
    wing.vertical                = True
    wing.symmetric               = False
    # wing.dynamic_pressure_ratio  = 1.0

    return wing

def vehicleAssembly():
    plane  = vehicle()
    plane.append_component(fuselage(plane))
    plane.append_component(mainWing())
    plane.append_component(horizontalTail())
    plane.append_component(verticalTail())
    plane.wings['vertical_stabilizer'].rudder = SUAVE.Components.Physical_Component()
    plane.append_component(hybrid_engine())

    #additional objects for weight estimation
    plane.landing_gear       = SUAVE.Components.Landing_Gear.Landing_Gear()
    plane.control_systems    = SUAVE.Components.Physical_Component()
    plane.electrical_systems = SUAVE.Components.Physical_Component()
    plane.avionics           = SUAVE.Components.Energy.Peripherals.Avionics()
    plane.passenger_weights  = 190*Units.lb
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

if __name__ == "__main__":
    getPlane()