import requests
import pandas as pd
import numpy as np
import time
from threading import Thread

ip_address = '192.168.1.232' #can find IP in app under "device info"
thread_running = True

##FEATURES (METRICS)##
metrics = ['apower', 'voltage', 'current']
power_data = {metric:np.array([]) for metric in metrics}

##LABELS (STATES)##\
state_id = 0
state_data = []
#TODO: DEFINE OUR STATE ID's
#WHICH ACTION CORRESPONDS TO WHAT ID

##INDEX (TIME)##
time_data = []


def measure_power(ip, metrics):
    r = requests.get('http://' + ip_address + '/rpc/Shelly.getStatus').json()
    switch = r['switch:0'] #print(switch) for other power data, e.g. voltage
    return {metric:switch[metric] for metric in metrics}

def collect_data():
    global thread_running
    global state_id

    while thread_running:
        power_measurement = measure_power(ip=ip_address, metrics=metrics)

        time_data.append(int(time.time()))
        for metric in metrics:
            power_data[metric] = np.append(power_data[metric], power_measurement[metric])

        state_data.append(state_id)
        state_id = 0
        time.sleep(1)

def input_state():
    #use x to stop threads
    global state_id

    while state_id != 'x':
        state_id = input('input state: ')


if __name__ == '__main__':
    t1 = Thread(target=collect_data)
    t2 = Thread(target=input_state)

    t1.start()
    t2.start()

    t2.join()  # interpreter will wait until your process get completed or terminated
    thread_running = False

    print('Saving data...')

    power_data['time'] = time_data
    power_data['state'] = state_data

    df = pd.DataFrame(data=power_data)
    df.to_csv('power_consumption_data.csv', header=True, index=False)
    print('Done!')
