"""
Generate Steady-State Visually Evoked Potential (SSVEP)
=======================================================

Steady-State Visually Evoked Potential (SSVEP) stimulus presentation.

"""
from datetime import datetime
import time
from optparse import OptionParser
import pandas as pd
import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet, local_clock
from psychopy import gui
parser = OptionParser()
parser.add_option("-d", "--duration",
                  dest="duration", type='int', default=360,
                  help="duration of the recording in seconds.")

(options, args) = parser.parse_args()

# Create markers stream outlet
info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)
datalog = pd.DataFrame(columns=['Timestamp', 'Marker', 'Frequency'])
markernames = [1, 2]
start = time.time()


# Set up trial parameters
n_trials = 2010
iti = 0.5
soa = 6.0
jitter = 0.2
record_duration = np.float32(options.duration)

# Set up trial list
stim_freq = np.random.binomial(1, 0.5, n_trials)
trials = DataFrame(dict(stim_freq=stim_freq, timestamp=np.zeros(n_trials)))




def get_possible_ssvep_freqs(frame_rate, stim_type='single'):
    """Get possible SSVEP stimulation frequencies.

    Utility function that returns the possible SSVEP stimulation
    frequencies and on/off pattern based on screen refresh rate.

    Args:
        frame_rate (float): screen frame rate, in Hz

    Keyword Args:
        stim_type (str): type of stimulation
            'single'-> single graphic stimulus (the displayed object
                appears and disappears in the background.)
            'reversal' -> pattern reversal stimulus (the displayed object
                appears and is replaced by its opposite.)

    Returns:
        (dict): keys are stimulation frequencies (in Hz), and values are
            lists of tuples, where each tuple is the number of (on, off)
            periods of one stimulation cycle

    For more info on stimulation patterns, see Section 2 of:
        Danhua Zhu, Jordi Bieger, Gary Garcia Molina, and Ronald M. Aarts,
        "A Survey of Stimulation Methods Used in SSVEP-Based BCIs,"
        Computational Intelligence and Neuroscience, vol. 2010, 12 pages,
        2010.
    """

    max_period_nb = int(frame_rate / 6)
    periods = np.arange(max_period_nb) + 1

    if stim_type == 'single':
        freqs = dict()
        for p1 in periods:
            for p2 in periods:
                f = frame_rate / (p1 + p2)
                try:
                    freqs[f].append((p1, p2))
                except:
                    freqs[f] = [(p1, p2)]
    elif stim_type == 'reversal':
        freqs = {frame_rate / p: [(p, p)] for p in periods[::-1]}

    return freqs


def init_flicker_stim(frame_rate, cycle, soa):
    """Initialize flickering stimulus.

    Get parameters for a flickering stimulus, based on the screen refresh
    rate and the desired stimulation cycle.

    Args:
        frame_rate (float): screen frame rate, in Hz
        cycle (tuple or int): if tuple (on, off), represents the number of
            'on' periods and 'off' periods in one flickering cycle. This
            supposes a "single graphic" stimulus, where the displayed object
            appears and disappears in the background.
            If int, represents the number of total periods in one cycle.
            This supposes a "pattern reversal" stimulus, where the
            displayed object appears and is replaced by its opposite.
        soa (float): stimulus duration, in s

    Returns:
        (dict): dictionary with keys
            'cycle' -> tuple of (on, off) periods in a cycle
            'freq' -> stimulus frequency
            'n_cycles' -> number of cycles in one stimulus trial

    """
    if isinstance(cycle, tuple):
        stim_freq = frame_rate / sum(cycle)
        n_cycles = int(soa * stim_freq)
    else:
        stim_freq = frame_rate / cycle
        cycle = (cycle, cycle)
        n_cycles = int(soa * stim_freq) / 2

    return {'cycle': cycle,
            'freq': stim_freq,
            'n_cycles': n_cycles}




# Create a dictionary to store the information you want to collect
info = {'participant':'201', 'session':'001'}

# Create a dialog box
infoDlg = gui.DlgFromDict(dictionary=info, title='Participant Information')

# Check if the user closed the dialog box
if infoDlg.OK:
    # Set up graphics
    mywin = visual.Window([1920, 1080], monitor='testMonitor', units='deg',
                          fullscr=True)
    grating = visual.GratingStim(win=mywin, mask='circle', size=200, sf=0.1)
    grating_neg = visual.GratingStim(win=mywin, mask='circle', size=200, sf=0.1,
                                     phase=0.5)
    fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0, 0], sf=0,
                                  color=[1, 0, 0], autoDraw=True)

    # Set up stimuli
    frame_rate = np.round(mywin.getActualFrameRate())  # Frame rate, in Hz
    freqs = get_possible_ssvep_freqs(frame_rate, stim_type='reversal')
    # print(freqs)

# TO change frequencies, change the values in the list below. Right now it is set to 20 and 30 Hz. It is 60/2=30 and 60/3=20 since our frame rate is 60.
    stim_patterns = [init_flicker_stim(frame_rate, 2, soa),
                     init_flicker_stim(frame_rate, 3, soa)]

    print('Flickering frequencies (Hz): {}\n'.format(
        [stim_patterns[0]['freq'], stim_patterns[1]['freq']]))
    for ii, trial in trials.iterrows():
        # Intertrial interval
        core.wait(iti + np.random.rand() * jitter)

        # Select stimulus frequency
        ind = trials['stim_freq'].iloc[ii]
        outlet.push_sample([markernames[ind]], time.time())
        # Send start marker
        datalog = datalog.append(
            {'Timestamp': time.time(), 'Marker': markernames[ind], 'Frequency': stim_patterns[ind]['freq']},
            ignore_index=True)

        # Present flickering stimulus
        for _ in range(int(stim_patterns[ind]['n_cycles'])):
            grating.setAutoDraw(True)
            for _ in range(int(stim_patterns[ind]['cycle'][0])):
                mywin.flip()
            grating.setAutoDraw(False)
            grating_neg.setAutoDraw(True)
            for _ in range(int(stim_patterns[ind]['cycle'][1])):
                mywin.flip()
            grating_neg.setAutoDraw(False)


        # offset
        mywin.flip()
        if len(event.getKeys()) > 0 or (time.time() - start) > record_duration:
            break
        event.clearEvents()
    # send the stopped trigger, adding by hxf 10/12/2021

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logname = f'C:\\Users\\TheLivingLab_Attend\\Desktop\\Data\\sub-{info["participant"]}\\sub-{info["session"]}_SSVEP_Log_{date}.csv'
    datalog.to_csv(logname, index=False)

    outlet.push_sample([999], time.time())
    time.sleep(0.5)

    # ending by hxf 10/12/2021

    # Cleanup
    mywin.close()
