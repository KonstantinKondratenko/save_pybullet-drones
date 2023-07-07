
import os
import time
import argparse
from datetime import datetime
import pdb
import math
import random
import numpy as np
import pybullet as p
import matplotlib.pyplot as plt

import gym_pybullet_drones.utils.velocity_commands as commands

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.envs.VisionAviary import VisionAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.control.SimplePIDControl import SimplePIDControl
# from gym_pybullet_drones.utils.Logger import Logger
from gym_pybullet_drones.utils.utils import sync, str2bool

from gym_pybullet_drones.envs.VelocityAviary import VelocityAviary





import time

DEFAULT_DRONE = DroneModel("cf2x")
DEFAULT_GUI = True
DEFAULT_RECORD_VIDEO = False
DEFAULT_PLOT = True
DEFAULT_USER_DEBUG_GUI = False
DEFAULT_AGGREGATE = True
DEFAULT_OBSTACLES = False
DEFAULT_SIMULATION_FREQ_HZ = 240
DEFAULT_CONTROL_FREQ_HZ = 48
DEFAULT_DURATION_SEC = 5
DEFAULT_OUTPUT_FOLDER = 'results'
DEFAULT_COLAB = False

def run(
        drone=DEFAULT_DRONE,
        gui=DEFAULT_GUI,
        record_video=DEFAULT_RECORD_VIDEO,
        plot=DEFAULT_PLOT,
        user_debug_gui=DEFAULT_USER_DEBUG_GUI,
        aggregate=DEFAULT_AGGREGATE,
        obstacles=DEFAULT_OBSTACLES,
        simulation_freq_hz=DEFAULT_SIMULATION_FREQ_HZ,
        control_freq_hz=DEFAULT_CONTROL_FREQ_HZ,
        duration_sec=DEFAULT_DURATION_SEC,
        output_folder=DEFAULT_OUTPUT_FOLDER,
        colab=DEFAULT_COLAB
        ):
        #### Initialize the simulation #############################
    # INIT_XYZS = np.array([
    #                       [ 0, 0, .1],
    #                       [.3, 0, .1],
    #                       [.6, 0, .1],
    #                       [0.9, 0, .1]
    #                       ])
    # INIT_RPYS = np.array([
    #                       [0, 0, 0],
    #                       [0, 0, np.pi/3],
    #                       [0, 0, np.pi/4],
    #                       [0, 0, np.pi/2]
    #                       ])
    INIT_XYZS = np.array([
                          [ 0, 0, 1.1],
                          [ 0, 0, 5.3],
                          [ 2, 0.3, 5.3],
                          [ 3, 0.4, 5.4]
                          ])
    INIT_RPYS = np.array([
                          [0, 0, 0],
                          [3, 3, 3],
                          [0, 0, 0],
                          [3, 3, 3]
                          ])
    AGGR_PHY_STEPS = int(simulation_freq_hz/control_freq_hz) if aggregate else 1
    PHY = Physics.PYB

    #### Create the environment ################################
    env = VelocityAviary(drone_model=drone,
                         num_drones=4,
                         initial_xyzs=INIT_XYZS,
                         initial_rpys=INIT_RPYS,
                         physics=Physics.PYB,
                         neighbourhood_radius=10,
                         freq=simulation_freq_hz,
                         aggregate_phy_steps=AGGR_PHY_STEPS,
                         gui=gui,
                         record=record_video,
                         obstacles=obstacles,
                         user_debug_gui=user_debug_gui
                         )

    #### Obtain the PyBullet Client ID from the environment ####
    PYB_CLIENT = env.getPyBulletClient()
    DRONE_IDS = env.getDroneIds()

    #### Compute number of control steps in the simlation ######
    PERIOD = duration_sec
    NUM_WP = control_freq_hz*PERIOD
    wp_counters = np.array([0 for i in range(4)])

    #### Initialize the velocity target ########################
    TARGET_VEL = np.zeros((4,NUM_WP,4))
    print(f"\n\n\n\n\n Numwp ({NUM_WP} )  == control_freq_hz ({control_freq_hz}) * PERIOD( <==> ) duration_sec({duration_sec}) ")
    for i in range(NUM_WP):
        # TARGET_VEL[0, i, :] = [-0.5, 1, 0, 0.99] if i < (NUM_WP/8) else [0.5, -1, 0, 0.99]
        # TARGET_VEL[1, i, :] = [0, 1, 0, 0.99] if i < (NUM_WP/8+NUM_WP/6) else [0, -1, 0, 0.99]
        # TARGET_VEL[2, i, :] = [0.2, 1, 0.2, 0.99] if i < (NUM_WP/8+2*NUM_WP/6) else [-0.2, -1, -0.2, 0.99]
        # TARGET_VEL[3, i, :] = [0, 1, 0.5, 0.99] if i < (NUM_WP/8+3*NUM_WP/6) else [0, -1, -0.5, 0.99]
        ###09808098####
        # TARGET_VEL[0, i, :] = [0, 1, 0, 0.99] if i < (NUM_WP/8) else [0.5, -1, 0, 0.99]
        # TARGET_VEL[1, i, :] = [0, 1, 0, 0.99] if i < (NUM_WP/8+NUM_WP/6) else [0, -1, 0, 0.99]
        # TARGET_VEL[2, i, :] = [0,   1, 0, 0.99] if i < (NUM_WP/8+2*NUM_WP/6) else [-0.2, -1, -0.2, 0.99]
        # TARGET_VEL[3, i, :] = [0,   1, 0, 0.99] if i < (NUM_WP/8+3*NUM_WP/6) else [0, -1, -0.5, 0.99]


        # TARGET_VEL[0, i, :] = [1,   0, 0, 0] 
        # TARGET_VEL[1, i, :] = [0,   1, -1, 0.99] 
        # TARGET_VEL[2, i, :] = [0,   1, 0, 0.99] 
        # TARGET_VEL[3, i, :] = [0,   1, 0, 0.99] 



        # это прикольные команды

        # TARGET_VEL[0, i, :] = [1,   0, 1, 1] if i % 40 < 20 else [-1,   0, -1, 1]
        # TARGET_VEL[1, i, :] = [5,   0, 0, 1] if i % 40 < 20 else [-5,   0, 0, 1]
        # TARGET_VEL[2, i, :] = [-1,   1, -1, 1] if i % 20 < 10 else [1,  -1, 1, -1]
        # if i < NUM_WP / 2:
        #     TARGET_VEL[3, i, :] = [-1,   1, -1, 1] if i % 20 < 10 else [1,  1, 1, 1]
        # else:
        #     TARGET_VEL[3, i, :] = [1,   -1, 1, -1] if i % 20 < 10 else [-1,  -1, -1, -1]

        # TARGET_VEL[0, i, :] = [1,   1, 1, 1] # - движение равномерное вдоль всех осей - по диагонали куба***
        # TARGET_VEL[1, i, :] = [1,   1, 1, 0] # - стоит на месте
        # TARGET_VEL[2, i, :] = [1,   1, 0, 1] # - движение равномерное вдоль ox oy - по диагонали основания куба***
        # TARGET_VEL[3, i, :] = [1,   0, 1, 1] # - движение равномерное вдоль oz oy (or ox) - по диагонали боковой грани куба***
        
        # if i < NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.along_x_axis(1, True)
        # elif i < NUM_WP/2:
        #     TARGET_VEL[0, i, :] = commands.along_y_axis(1, True)
        # elif i < 3*NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.along_x_axis(1, False)
        # else:
        #     TARGET_VEL[0, i, :] = commands.along_y_axis(1, False)

        
        # print (commands.compare(commands.along_x_axis(1, True), commands.along_z_axis(1, True)))

        # TARGET_VEL[0, i, :] = commands.stand_still()

                            # это хорошо работает компеир из 2х
        # if i < NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.compare_two(commands.along_x_axis(1, True), commands.along_z_axis(1, True))
        # elif i < NUM_WP/2:
        #     TARGET_VEL[0, i, :] = commands.compare_two(commands.along_y_axis(1, True), commands.along_z_axis(1, False))
        # elif i < 3*NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.compare_two(commands.along_x_axis(1, False), commands.along_z_axis(1, True))
        # else:
        #     TARGET_VEL[0, i, :] = commands.compare_two(commands.along_y_axis(1, False), commands.along_z_axis(1, False))

                            # это хорошо работает компеир из 3х
        if i < NUM_WP/4:
            TARGET_VEL[0, i, :] = commands.compare_tree(commands.along_x_axis(1, True), commands.along_z_axis(1, True), commands.along_y_axis(i/NUM_WP, True))
        elif i < NUM_WP/2:
            TARGET_VEL[0, i, :] = commands.compare_tree(commands.along_y_axis(1, True), commands.along_z_axis(1, False), commands.along_x_axis(i/NUM_WP, True))
        elif i < 3*NUM_WP/4:
            TARGET_VEL[0, i, :] = commands.compare_tree(commands.along_x_axis(1, False), commands.along_z_axis(1, True), commands.along_y_axis(i/NUM_WP, False))
        else:
            TARGET_VEL[0, i, :] = commands.compare_tree(commands.along_y_axis(1, False), commands.along_z_axis(1, False), commands.along_x_axis(i/NUM_WP, False))

        
        # if i < NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.angle_between_ox_oy(53, 1, True)
        # elif i < NUM_WP/2:
        #     TARGET_VEL[0, i, :] = commands.angle_between_ox_oy(53, 1, False)
        # elif i < 3*NUM_WP/4:
        #     TARGET_VEL[0, i, :] = commands.angle_between_ox_oz(24, 1, True)
        # else:
        #     TARGET_VEL[0, i, :] = commands.angle_between_ox_oz(24, 1, False)
        
        TARGET_VEL[1, i, :] = commands.stand_still()
        TARGET_VEL[2, i, :] = commands.stand_still() 
        TARGET_VEL[3, i, :] = commands.stand_still()


        # ox - red; oy - green; oz - blue.
        # Цифры: 1 - ox; 2 - oy; 3 - oz; 4 - скорость. -- задается первым тремя числами направление вектора, а 4 - его длина



    #### Run the simulation ####################################
    CTRL_EVERY_N_STEPS = int(np.floor(env.SIM_FREQ/control_freq_hz))
    action = {str(i): np.array([0,0,0,0]) for i in range(4)}
    START = time.time()
    i=0
    while True:
        # time.sleep(0.05)
        
        i+=1

        ############################################################
        # for j in range(3): env._showDroneLocalAxes(j)

        #### Step the simulation ###################################
        obs, reward, done, info = env.step(action)

        #### Compute control at the desired frequency ##############
        if i%CTRL_EVERY_N_STEPS == 0:
           
            #### Compute control for the current way point #############
            for j in range(4):
                action[str(j)] = TARGET_VEL[j, wp_counters[j], :] 

            #### Go to the next way point and loop #####################
            for j in range(4): 
                wp_counters[j] = wp_counters[j] + 1 if wp_counters[j] < (NUM_WP-1) else 0

  
        #### Printout ##############################################
        if i%env.SIM_FREQ == 0:
            env.render()

        #### Sync the simulation ###################################
        if gui:
            sync(i, START, env.TIMESTEP)

    #### Close the environment #################################
    env.close()

    #### Plot the simulation results ###########################

if __name__ == "__main__":
    #### Define and parse (optional) arguments for the script ##
    parser = argparse.ArgumentParser(description='Velocity control example using VelocityAviary')
    parser.add_argument('--drone',              default=DEFAULT_DRONE,     type=DroneModel,    help='Drone model (default: CF2X)', metavar='', choices=DroneModel)
    parser.add_argument('--gui',                default=DEFAULT_GUI,       type=str2bool,      help='Whether to use PyBullet GUI (default: True)', metavar='')
    parser.add_argument('--record_video',       default=DEFAULT_RECORD_VIDEO,      type=str2bool,      help='Whether to record a video (default: False)', metavar='')
    parser.add_argument('--plot',               default=DEFAULT_PLOT,       type=str2bool,      help='Whether to plot the simulation results (default: True)', metavar='')
    parser.add_argument('--user_debug_gui',     default=DEFAULT_USER_DEBUG_GUI,      type=str2bool,      help='Whether to add debug lines and parameters to the GUI (default: False)', metavar='')
    parser.add_argument('--aggregate',          default=DEFAULT_AGGREGATE,       type=str2bool,      help='Whether to aggregate physics steps (default: False)', metavar='')
    parser.add_argument('--obstacles',          default=DEFAULT_OBSTACLES,      type=str2bool,      help='Whether to add obstacles to the environment (default: False)', metavar='')
    parser.add_argument('--simulation_freq_hz', default=DEFAULT_SIMULATION_FREQ_HZ,        type=int,           help='Simulation frequency in Hz (default: 240)', metavar='')
    parser.add_argument('--control_freq_hz',    default=DEFAULT_CONTROL_FREQ_HZ,         type=int,           help='Control frequency in Hz (default: 48)', metavar='')
    parser.add_argument('--duration_sec',       default=DEFAULT_DURATION_SEC,         type=int,           help='Duration of the simulation in seconds (default: 5)', metavar='')
    parser.add_argument('--colab',              default=DEFAULT_COLAB, type=bool,           help='Whether example is being run by a notebook (default: "False")', metavar='')
    ARGS = parser.parse_args()

    run(**vars(ARGS))

