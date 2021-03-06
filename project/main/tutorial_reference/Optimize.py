# Optimize.py
# Created:  Feb 2016, M. Vegh
# Modified: Aug 2017, E. Botero
#           Aug 2018, T. MacDonald

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
import plane
import configurations
import Analysis
import Missions
import Procedure
import Plot_Mission
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from SUAVE.Optimization import Nexus, carpet_plot
import SUAVE.Optimization.Package_Setups.scipy_setup as scipy_setup

# ----------------------------------------------------------------------        
#   Run the whole thing
# ----------------------------------------------------------------------  
def main():
    problem = setup()
    
    ## Base Input Values
    output = problem.objective()
    
    ## Uncomment to view contours of the design space
    #variable_sweep(problem)
    
    ## Uncomment for the first optimization
    #output = scipy_setup.SciPy_Solve(problem,solver='SLSQP')
    #print output    
    
    ## Uncomment these lines when you want to start an optimization problem from a different initial guess
    #inputs                                   = [1.28, 1.38]
    #scaling                                  = problem.optimization_problem.inputs[:,3] #have to rescale inputs to start problem from here
    #scaled_inputs                            = np.multiply(inputs,scaling)
    #problem.optimization_problem.inputs[:,1] = scaled_inputs
    #output = scipy_setup.SciPy_Solve(problem,solver='SLSQP')
    #print output        
  
    print 'fuel burn = ', problem.summary.base_mission_fuelburn
    print 'fuel margin = ', problem.all_constraints()
    
    Plot_Mission.plot_mission(problem)
    
    return

# ----------------------------------------------------------------------        
#   Inputs, Objective, & Constraints
# ----------------------------------------------------------------------  

def setup():

    nexus = Nexus()
    problem = Data()
    nexus.optimization_problem = problem

    # -------------------------------------------------------------------
    # Inputs
    # -------------------------------------------------------------------

    #   [ tag                            , initial, (lb,ub)             , scaling , units ]
    problem.inputs = np.array([
        [ 'wing_area'                    ,  95    , (   90. ,   130.   ) ,   100. , Units.meter**2],
        [ 'cruise_altitude'              ,  11    , (   9   ,    14.   ) ,   10.  , Units.km],
    ])

    # -------------------------------------------------------------------
    # Objective
    # -------------------------------------------------------------------

    # throw an error if the user isn't specific about wildcards
    # [ tag, scaling, units ]
    problem.objective = np.array([
        [ 'fuel_burn', 10000, Units.kg ]
    ])
    
    # -------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------
    
    # [ tag, sense, edge, scaling, units ]
    problem.constraints = np.array([
        [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less], #fuel margin defined here as fuel 
    ])
    
    # -------------------------------------------------------------------
    #  Aliases
    # -------------------------------------------------------------------
    
    # [ 'alias' , ['data.path1.name','data.path2.name'] ]

    problem.aliases = [
        [ 'wing_area'                        ,   ['vehicle_configurations.*.wings.main_wing.areas.reference',
                                                  'vehicle_configurations.*.reference_area'                    ]],
        [ 'cruise_altitude'                  , 'missions.base.segments.climb_5.altitude_end'                    ],
        [ 'fuel_burn'                        ,    'summary.base_mission_fuelburn'                               ],
        [ 'design_range_fuel_margin'         ,    'summary.max_zero_fuel_margin'                                ],
    ]    
    
    # -------------------------------------------------------------------
    #  Vehicles
    # -------------------------------------------------------------------
    # nexus.vehicle_configurations = Vehicles.setup()
    vehicle = plane.getPlane()
    nexus.vehicle_configurations = configurations.configSetup(vehicle)
    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    nexus.analyses = Analysis.setup(nexus.vehicle_configurations)
    
    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
    nexus.missions = Missions.setup(nexus.analyses)
    
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.procedure = Procedure.setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary = Data()    
    nexus.total_number_of_iterations = 0
    return nexus
    
def variable_sweep(problem):    
    number_of_points = 5
    outputs     = carpet_plot(problem, number_of_points, 0, 0)  #run carpet plot, suppressing default plots
    inputs      = outputs.inputs
    objective   = outputs.objective
    constraints = outputs.constraint_val
    plt.figure(0)
    CS   = plt.contourf(inputs[0,:],inputs[1,:], objective, 20, linewidths=2)
    cbar = plt.colorbar(CS)
    
    cbar.ax.set_ylabel('fuel burn (kg)')
    CS_const = plt.contour(inputs[0,:],inputs[1,:], constraints[0,:,:])
    plt.clabel(CS_const, inline=1, fontsize=10)
    cbar = plt.colorbar(CS_const)
    cbar.ax.set_ylabel('fuel margin')
    
    plt.xlabel('Wing Area (m^2)')
    plt.ylabel('Cruise Altitude (km)')
    
    plt.legend(loc='upper left')  
    # plt.show(block=True)    
    plt.savefig("./res/variable_sweep.png")
    
    return

if __name__ == '__main__':
    main()