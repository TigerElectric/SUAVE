import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing

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

    #initialize the gas turbine network
    gt_engine                   = SUAVE.Components.Energy.Networks.Turbofan()
    gt_engine.tag               = 'turbofan'

    gt_engine.number_of_engines = 2.0
    gt_engine.bypass_ratio      = 5.4
    gt_engine.engine_length     = 2.71
    gt_engine.nacelle_diameter  = 2.05

    #set the working fluid for the network
    gt_engine.working_fluid = SUAVE.Attributes.Gases.Air


    #Component 1 : ram,  to convert freestream static to stagnation quantities
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'

    #add ram to the network
    gt_engine.ram = ram

    #Component 2 : inlet nozzle
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet nozzle'

    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio        = 0.98

    #add inlet nozzle to the network
    gt_engine.inlet_nozzle = inlet_nozzle

    #Component 3 :low pressure compressor    
    low_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()    
    low_pressure_compressor.tag = 'lpc'

    low_pressure_compressor.polytropic_efficiency = 0.91
    low_pressure_compressor.pressure_ratio        = 1.9    

    #add low pressure compressor to the network    
    gt_engine.low_pressure_compressor = low_pressure_compressor

    #Component 4: high pressure compressor  
    high_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()    
    high_pressure_compressor.tag = 'hpc'

    high_pressure_compressor.polytropic_efficiency = 0.91
    high_pressure_compressor.pressure_ratio        = 10.0   

    #add the high pressure compressor to the network    
    gt_engine.high_pressure_compressor = high_pressure_compressor

    #Component 5 :low pressure turbine  
    low_pressure_turbine = SUAVE.Components.Energy.Converters.Turbine()   
    low_pressure_turbine.tag='lpt'

    low_pressure_turbine.mechanical_efficiency = 0.99
    low_pressure_turbine.polytropic_efficiency = 0.93

    #add low pressure turbine to the network    
    gt_engine.low_pressure_turbine = low_pressure_turbine

    #Component 5 :high pressure turbine  
    high_pressure_turbine = SUAVE.Components.Energy.Converters.Turbine()   
    high_pressure_turbine.tag='hpt'

    high_pressure_turbine.mechanical_efficiency = 0.99
    high_pressure_turbine.polytropic_efficiency = 0.93

    #add the high pressure turbine to the network    
    gt_engine.high_pressure_turbine = high_pressure_turbine 

    #Component 6 :combustor  
    combustor = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag = 'Comb'

    combustor.efficiency                = 0.99 
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1500
    combustor.pressure_ratio            = 0.95
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()    

    #add the combustor to the network    
    gt_engine.combustor = combustor

    #Component 7 :core nozzle
    core_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    core_nozzle.tag = 'core nozzle'

    core_nozzle.polytropic_efficiency = 0.95
    core_nozzle.pressure_ratio        = 0.99    

    #add the core nozzle to the network    
    gt_engine.core_nozzle = core_nozzle

    #Component 8 :fan nozzle
    fan_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    fan_nozzle.tag = 'fan nozzle'

    fan_nozzle.polytropic_efficiency = 0.95
    fan_nozzle.pressure_ratio        = 0.99

    #add the fan nozzle to the network
    gt_engine.fan_nozzle = fan_nozzle

    #Component 9 : fan   
    fan = SUAVE.Components.Energy.Converters.Fan()   
    fan.tag = 'fan'

    fan.polytropic_efficiency = 0.93
    fan.pressure_ratio        = 1.7    

    #add the fan to the network
    gt_engine.fan = fan    

    #Component 10 : thrust (to compute the thrust)
    thrust = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag ='compute_thrust'

    #total design thrust (includes all the engines)
    thrust.total_design             = 52700.0* Units.N #Newtons
                                        
    #design sizing conditions
    altitude      = 35000.0*Units.ft
    mach_number   = 0.78 
    isa_deviation = 0.

    # add thrust to the network
    gt_engine.thrust = thrust

    #size the turbofan
    turbofan_sizing(gt_engine,mach_number,altitude) 

    return gt_engine

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