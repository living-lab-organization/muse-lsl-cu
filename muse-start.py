import muselsl
import time
import datetime
import numpy as np
import subprocess
import os
import psutil
import muselsl.winctrlc

t_init = int(datetime.datetime(2023, 5, 11, 14, 43, 0).timestamp())  # Year, Month, Day, Hour, Minutes
participant = '101'
name = 'MuseS-7A18'
cwd = os.getcwd()
venv_path = ''.join(['\"', os.path.join(cwd, 'venv', 'Scripts', 'activate.bat'), '\"'])
data_folder = os.path.join(cwd, '..', 'Data')
try:
    os.makedirs(data_folder)
except OSError as error:
    print(error)
data_path_relative = os.path.join('..', 'Data', 'sub-' + participant)
data_path = os.path.join(cwd, data_path_relative)
try:
    os.makedirs(data_path)
except OSError as error:
    print(error)

data_path_quotes = '\"' + data_path + '\"'
stream_command = ''.join(['muselsl stream -n ', name, ' -p -c -g'])
record_command = ''.join(['muselsl record -s ', str(t_init),
                          ' -p ', participant, ' -t'])
filename = os.path.join(data_path, "%s_%s_recording_%s.csv" %
                            (''.join(['sub-', participant]),
                             'EEG',
                             time.strftime('%Y-%m-%d-%H.%M.%S', time.gmtime())))

command = ''.join(['start ', venv_path, ' ; .\\venv\\Scripts\\python.exe EEG_course_student_script_ver003.py -p ', participant, ' -s ', str(t_init)])
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
time.sleep(5)

# stream_p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
stream_p = muselsl.winctrlc.Popen(stream_command, cwd)
time.sleep(15)

ppg_command = ''.join([record_command, ' PPG'])
ppg_p = muselsl.winctrlc.Popen(ppg_command, cwd)

acc_command = ''.join([record_command, ' ACC'])
acc_p = muselsl.winctrlc.Popen(acc_command, cwd)

gyro_command = ''.join([record_command, ' GYRO'])
gyro_p = muselsl.winctrlc.Popen(gyro_command, cwd)

[inlet, inlet_marker, chunk_length, ch, ch_names] = muselsl.start_record(t_init=t_init)

res = []
timestamps = []
markers = []
flag = 0
data_flag = 1
time_correction = inlet.time_correction()
last_written_timestamp = None
print('Start recording at time t=%.3f' % t_init)
print('Time correction: ', time_correction)

while 1:
    old_len = len(timestamps)
    flag += 1
    try:
        data, timestamp = inlet.pull_chunk(
            timeout=1.0, max_samples=chunk_length)
        if timestamp:
            res.append(data)
            timestamps.extend(timestamp)
            tr = time.time()
        marker, timestamp = inlet_marker.pull_sample(timeout=0.0)
        if timestamp:
            markers.append([marker, timestamp])
        if "999" in markers:
            break

        # Save every 5s
        if data_flag == 1:
            pass
        elif last_written_timestamp is None or last_written_timestamp + 5 < timestamps[-1]:
            muselsl.save_ongoing(
                res,
                timestamps,
                time_correction,
                True,
                inlet_marker,
                markers,
                ch_names,
                last_written_timestamp=last_written_timestamp,
                participant=participant,
                filename=filename
            )
            last_written_timestamp = timestamps[-1]

        if len(timestamps) > old_len:
            flag = 0
            if len(timestamps) > 256:
                data_flag = np.sum(np.asarray(res[-1]))
        if data_flag != 0 and flag <= 5:
            pass
        else:
            print(data_flag, flag, len(timestamps))
            flag = 0
            data_flag = 1
            ppg_p.send_ctrl_c()
            acc_p.send_ctrl_c()
            gyro_p.send_ctrl_c()
            stream_p.send_ctrl_c()
            time.sleep(10)
            print(command)
            stream_p = muselsl.winctrlc.Popen(stream_command, cwd)
            time.sleep(15)
            ppg_p = muselsl.winctrlc.Popen(ppg_command, cwd)
            acc_p = muselsl.winctrlc.Popen(acc_command, cwd)
            gyro_p = muselsl.winctrlc.Popen(gyro_command, cwd)
    except KeyboardInterrupt:
        break

muselsl.save_ongoing(
                res,
                timestamps,
                time_correction,
                True,
                inlet_marker,
                markers,
                ch_names,
                last_written_timestamp=last_written_timestamp,
                participant=participant,
                filename=filename
            )

ppg_p.send_ctrl_c()
acc_p.send_ctrl_c()
gyro_p.send_ctrl_c()
stream_p.send_ctrl_c()



