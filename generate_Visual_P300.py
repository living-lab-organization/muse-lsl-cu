import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event, gui
import time
from optparse import OptionParser
from pylsl import StreamInfo, StreamOutlet, local_clock
from glob import glob
from random import choice

parser = OptionParser()
parser.add_option("-d", "--duration",
                  dest="duration", type='int', default=360,
                  help="duration of the recording in seconds.")

(options, args) = parser.parse_args()

# create
info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')

# next make an outlet
outlet = StreamOutlet(info)

markernames = [1, 2]

start = time.time()

n_trials = 2010
iti = .3
soa = 0.2
jitter = 0.2
record_duration = np.float32(options.duration)

# Setup log
position = np.random.binomial(1, 0.15, n_trials)

trials = DataFrame(dict(position=position,
                        timestamp=np.zeros(n_trials)))


# graphics



# Dialog box for participant information
info = {'participant': '001', 'session': '001'}
infoDlg = gui.DlgFromDict(dictionary=info, title='Participant Information')
if infoDlg.OK:
    mywin = visual.Window([1920, 1080], monitor="testMonitor", units="deg",
                          fullscr=True)


    def loadImage(filename):
        return visual.ImageStim(win=mywin, image=filename)


    targets = list(map(loadImage, glob('cats_dogs/target-*.jpg')))
    nontargets = list(map(loadImage, glob('cats_dogs/nontarget-*.jpg')))
    for ii, trial in trials.iterrows():
        # inter trial interval
        core.wait(iti + np.random.rand() * jitter)

        # onset
        pos = trials['position'].iloc[ii]
        image = choice(targets if pos == 1 else nontargets)
        image.draw()
        timestamp = time.time()
        outlet.push_sample([markernames[pos]], timestamp)
        mywin.flip()

        # offset
        core.wait(soa)
        mywin.flip()
        if len(event.getKeys()) > 0 or (time.time() - start) > record_duration:
            break
        event.clearEvents()

# Cleanup

    mywin.close()
markernames = {'experiment_stopped': 999}
outlet.push_sample([markernames['experiment_stopped']], time.time())
