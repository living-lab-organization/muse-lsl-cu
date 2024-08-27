from psychopy import visual, core, event, gui
from datetime import datetime
import time
import numpy as np
import pandas as pd
from pandas import DataFrame
from pylsl import StreamInfo, StreamOutlet, local_clock
from optparse import OptionParser

# Parse command-line options
parser = OptionParser()
parser.add_option("-d", "--duration", dest="duration", type='int', default=360, help="duration of the recording in seconds.")
(options, args) = parser.parse_args()

# Create markers stream outlet
info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)
datalog = pd.DataFrame(columns=['Timestamp', 'Marker', 'Frequency'])
markernames = [1, 2]
start = time.time()

# Setup trial parameters
n_trials = 2010
iti = 0.5
soa = 3.0
jitter = 0.2
record_duration = np.float32(options.duration)

# Setup trial list
stim_freq = np.random.binomial(1, 0.5, n_trials)
trials = DataFrame(dict(stim_freq=stim_freq, timestamp=np.zeros(n_trials)))

# Setup graphics


# Dialog box for participant information
info = {'participant': '001', 'session': '001'}
infoDlg = gui.DlgFromDict(dictionary=info, title='Participant Information')

if infoDlg.OK:
    mywin = visual.Window([1920, 1080], monitor='testMonitor', units='deg', fullscr=True)
    circle = visual.Circle(mywin, radius=10, fillColor=[1, 1, 1], lineColor=[1, 1, 1])
    frame_rate = mywin.getActualFrameRate()
    if frame_rate is None:
        frame_rate = 60  # Assume a default if unable to detect
    print("Frame Rate: ", frame_rate)
    # Define frequencies1
    frequencies = [20, 30]  # Frequencies for the blinking circle
    for ii, trial in trials.iterrows():
        core.wait(iti + np.random.rand() * jitter)
        ind = trials['stim_freq'].iloc[ii]
        freq = frequencies[ind]
        n_cycles = int(soa * freq)
        n_frames_on_off = int(frame_rate / (2 * freq))

        # Send start marker
        timestamp = time.time()
        outlet.push_sample([markernames[ind]], timestamp)

        # Present flickering stimulus
        circle.setAutoDraw(True)
        for _ in range(n_cycles):
            for _ in range(n_frames_on_off):  # On phase
                mywin.flip()
            circle.setAutoDraw(False)
            for _ in range(n_frames_on_off):  # Off phase
                mywin.flip()
            circle.setAutoDraw(True)

        # Record data
        datalog = datalog.append({'Timestamp': time.time(), 'Marker': markernames[ind], 'Frequency': freq},
                                 ignore_index=True)

        # Ensure the circle is off after the trial
        circle.setAutoDraw(False)
        mywin.flip()

        # Break if necessary
        if len(event.getKeys()) > 0 or (time.time() - start) > record_duration:
            break
        event.clearEvents()

    # Cleanup and data saving

    outlet.push_sample([999], time.time())

    mywin.close()