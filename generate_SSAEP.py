"""
Generate Steady-State Auditory Evoked Potential (SSAEP)
=======================================================

Steady-State Auditory Evoked Potential (SSAEP) - also known as Auditory
Steady-State Response (ASSR) - stimulus presentation.

"""

import time
from optparse import OptionParser

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event, sound, gui
from pylsl import StreamInfo, StreamOutlet, local_clock
from scipy import stats
import pandas as pd

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
soa = 3.0
jitter = 0.2
record_duration = np.float32(options.duration)

# Set up trial list
stim_freq = np.random.binomial(1, 0.5, n_trials)
trials = DataFrame(dict(stim_freq=stim_freq, timestamp=np.zeros(n_trials)))


def generate_am_waveform(carrier_freq, am_freq, secs=1, sample_rate=44100,
                         am_type='gaussian', gaussian_std_ratio=8):
    """Generate an amplitude-modulated waveform.

    Generate a sine wave amplitude-modulated by a second sine wave or a
    Gaussian envelope with standard deviation = period_AM/8.

    Args:
        carrier_freq (float): carrier wave frequency, in Hz
        am_freq (float): amplitude modulation frequency, in Hz

    Keyword Args:
        secs (float): duration of the stimulus, in seconds
        sample_rate (float): sampling rate of the sound, in Hz
        am_type (str): amplitude-modulation type
            'gaussian' -> Gaussian with std defined by `gaussian_std`
            'sine' -> sine wave
        gaussian_std_ratio (float): only used if `am_type` is 'gaussian'.
            Ratio between AM period and std of the Gaussian envelope. E.g.,
            gaussian_std = 8 means the Gaussian window has 8 standard
            deviations around its mean inside one AM period.

    Returns:
        (numpy.ndarray): sound samples
    """
    t = np.arange(0, secs, 1./sample_rate)

    if am_type == 'gaussian':
        period = int(sample_rate / am_freq)
        std = period / gaussian_std_ratio
        norm_window = stats.norm.pdf(np.arange(period), period / 2, std)
        norm_window /= np.max(norm_window)
        n_windows = int(np.ceil(secs * am_freq))
        am = np.tile(norm_window, n_windows)
        am = am[:len(t)]

    elif am_type == 'sine':
        am = np.sin(2 * np.pi * am_freq * t)

    carrier = 0.5 * np.sin(2 * np.pi * carrier_freq * t) + 0.5
    am_out = carrier * am

    return am_out

# Create a dictionary to store the information you want to collect
info = {'participant':'001'}

# Create a dialog box
infoDlg = gui.DlgFromDict(dictionary=info, title='Participant Information')

# Check if the user closed the dialog box
if infoDlg.OK:

    # Setup graphics
    mywin = visual.Window([1920, 1080], monitor='testMonitor', units='deg',
                          fullscr=True)
    fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0, 0], sf=0,
                                  rgb=[1, 0, 0])
    fixation.setAutoDraw(True)

    # Generate stimuli
    am1 = generate_am_waveform(900, 45, secs=soa, sample_rate=44100)
    am2 = generate_am_waveform(770, 40.018, secs=soa, sample_rate=44100)

    aud1 = sound.Sound(am1, sampleRate=44100)
    aud1.setVolume(0.8)
    aud2 = sound.Sound(am2, sampleRate=44100)
    aud2.setVolume(0.8)
    auds = [aud1, aud2]

    mywin.flip()

    for ii, trial in trials.iterrows():
        # Intertrial interval
        core.wait(iti + np.random.rand() * jitter)

        # Select stimulus frequency
        ind = trials['stim_freq'].iloc[ii]
        auds[ind].play()

        # Send start marker
        timestamp = time.time()
        outlet.push_sample([markernames[ind]], time.time())

        # offset
        core.wait(soa)
        mywin.flip()
        if len(event.getKeys()) > 0 or (time.time() - start) > record_duration:
            break
        event.clearEvents()
    outlet.push_sample([999], time.time())

    # Cleanup
    mywin.close()