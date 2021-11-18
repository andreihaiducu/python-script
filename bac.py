import BAC0
from collections import defaultdict
from datetime import datetime

import threading
import json

bacnet = BAC0.connect('10.80.3.70/24')
discovered = bacnet.discover(networks='known')

def set_interval(func,sec):
    def func_wrapper():
        set_interval(func,sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
def FileSave(filename,content):
    with open(filename, "a") as myfile:
        myfile.write(content)
def save_datapoints(controller, deviceId, deviceIp):
    for point in controller.points:
        x = {
                'device_id': deviceId,
                'device_ip': deviceIp,
                'datapoint_name': point.read_property('objectName'),
                'datapoint_value': point.value,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        json_string = json.dumps(x)
        FileSave('logfile.json', json_string + ',\n' )

def run_process():
    print('Start')
    for device in discovered:
        (deviceIp, deviceId) = device
        controller = BAC0.device(deviceIp, deviceId, bacnet)
        save_datapoints(controller, deviceId, deviceIp)

set_interval(run_process,10)
