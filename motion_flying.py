import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/1/2M/E7E7E7E7EA')

DEFAULT_HEIGHT = 0.3
BOX_LIMIT = 0.5

def move_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(2)
        mc.forward(0.3)
        mc.turn_right(90)

        time.sleep(2)
        mc.forward(0.3)
        mc.turn_right(90)

        time.sleep(2)
        mc.forward(0.3)
        mc.turn_right(90)

        time.sleep(2)
        mc.forward(0.3)
        time.sleep(2)
        mc.land(targetHeight=0.1, duration=10)
        mc.stop()


def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        # mc.up(0.003)
        time.sleep(3)
        # mc.up(0.1)
        # time.sleep(1)
        # mc.land(targetHeight=0.1, duration=10)
        mc.stop()
    # with MotionCommander(scf, default_height = DEFAULT_HEIGHT) as mc:
    #     time.sleep(3)
    #     mc.stop()


if __name__ == '__main__':
    
    cflib.crtp.init_drivers()
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # take_off_simple(scf)
        move_simple(scf)