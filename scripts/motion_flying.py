import logging
import sys
import time
from datetime import datetime
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H:%M")
dateandtime = 'log_' + str(current_time)[2:]
log_path = '/home/asl/cf/log/' + dateandtime + '.txt'

URI = uri_helper.uri_from_env(default='radio://0/1/2M/E7E7E7E7EA')
deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)
logfile = open(log_path, 'w+')

position_estimate = [0, 0]

DEFAULT_HEIGHT = 0.3
BOX_LIMIT = 0.3

start_time = time.time()
def log_pos_callback(timestamp, data, logconf):
    cur_time = time.time()
    elapsed_time = str(cur_time - start_time)
    log = str('x:'+ str(round(data['stateEstimate.x'],5))+ '  '+
          'y:'+ str(round(data['stateEstimate.y'],5))+ '  '+
          'z:'+ str(round(data['stateEstimate.z'],5))+ '  ' +
          'vx:'+ str(round(data['stateEstimate.vx'],5))+ '  '+
          'vy:'+ str(round(data['stateEstimate.vy'],5))+ '  '+
          'vz:'+ str(round(data['stateEstimate.vz'],5)))
    logfile.write(str('time' + elapsed_time))
    logfile.write(log)
    logfile.write('\n')
    print(log)

    # print('x:', round(data['stateEstimate.x'],5), '  ',
    #       'y:', round(data['stateEstimate.y'],5), '  ',
    #       'z:', round(data['stateEstimate.z'],5), '  '
    #       'vx:', round(data['stateEstimate.vx'],5), '  ',
    #       'vy:', round(data['stateEstimate.vy'],5), '  ',
    #       'vz:', round(data['stateEstimate.vz'],5))
    print('\n')
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']

def param_deck_flow(_, value_str):
    value = int(value_str)
    if value:
        deck_attached_event.set()
    else:
        print('No flow deck attached!')

def move_box_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        while True:
            if position_estimate[0] > BOX_LIMIT:
                mc.start_back()
            elif position_estimate[0] < -BOX_LIMIT:
                mc.start_forward()
            time.sleep(0.1)

def move_box_limit_2(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.2
        body_y_cmd = 0.1
        max_vel = 1.5
        while True:
            if position_estimate[0] > BOX_LIMIT:
                body_x_cmd = -max_vel
            elif position_estimate[0] < -BOX_LIMIT:
                body_x_cmd = max_vel
            if position_estimate[1] > BOX_LIMIT:
                body_y_cmd = -max_vel
            elif position_estimate[1] < -BOX_LIMIT:
                body_y_cmd = max_vel
            
            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)

            time.sleep(0.1)

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
        time.sleep(3)
        mc.land(targetHeight=0.05, duration=10)
        mc.stop()

def stand_simple(scf):
    with MotionCommander(scf, default_height=2) as mc:
        while True:
            time.sleep(0.1)
        time.sleep(3)
        # mc.land(targetHeight=0.05, duration=10)
        mc.stop()


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                        cb=param_deck_flow)
        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')

        logconf.add_variable('stateEstimate.vx', 'float')
        logconf.add_variable('stateEstimate.vy', 'float')
        logconf.add_variable('stateEstimate.vz', 'float')

        # logconf.add_variable('stateEstimate.ax', 'float')
        # logconf.add_variable('stateEstimate.ay', 'float')
        # logconf.add_variable('stateEstimate.az', 'float')

        # logconf.add_variable('stateEstimate.roll', 'float')
        # logconf.add_variable('stateEstimate.pitch', 'float')
        # logconf.add_variable('stateEstimate.yaw', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)


        if not deck_attached_event.wait(timeout=5):
            sys.exit(1)

        logconf.start()
            
        # take_off_simple(scf)
        # move_simple(scf)
        # stand_simple(scf)
        # move_box_limit(scf)
        # move_box_limit_2(scf)
        time.sleep(1)

        logconf.stop()