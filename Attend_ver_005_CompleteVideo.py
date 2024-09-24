#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on June 05, 2024, at 14:50
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""
import queue


# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from Setting_up
import pandas as pd
import time
import winsound


# Run 'Before Experiment' code from code
from pylsl import StreamInfo, StreamOutlet, local_clock
info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
# next make an outlet
outlet = StreamOutlet(info)
# create a new marker list
def load_markernames(filename):
    df = pd.read_csv(filename, index_col=0)
    return df['Value'].to_dict()
markernames = load_markernames('C:\\Users\\TheLivingLab_Attend\\Desktop\\muse-lsl-cu-main\\markernames.csv')

# --- Import Video Camera Part ---#
import threading
from datetime import datetime
import cv2
def record_camera(camera_index, filename, frame_queue, event_stop):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while not event_stop.is_set():
        ret, frame = cap.read()
        if ret:
            # Instead of writing immediately, put frame into queue
            frame_queue.put(frame)
            # Set frame to None after it's put into the queue
            frame = None
        else:
            break
    # Indicate that capturing is done
    frame_queue.put(None)
    cap.release()

def write_video(filename, frame_queue):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 30.0, (1920, 1080))
    while True:
        frame = frame_queue.get()
        if frame is None:
            # None is the signal that capturing has finished
            break
        out.write(frame)
        frame_queue.task_done()

    out.release()



    # --- End of Video Camera Part ---#`



# --- Setup global variables (available in all functions) ---
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'Attend_ver_005'  # from the Builder filename that created this script
expInfo = {
    'participant': '000',
    'Video_Choice': ['1: Cognitive_Neuroscience_Methods', '2: Attention and Awareness', '3: Nature Nurture', '4: Music', '5: Navigation', '6: Number'],
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    dataDir = 'C:\\Users\\TheLivingLab_Attend\\Desktop'
    filename = u'Data/sub-%s/Psychopy_Logs/%s_PsychopyLogs' % (expInfo['participant'], expInfo['participant'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\TheLivingLab_Attend\\Desktop\\muse-lsl-cu-main\\Attend_in_Lab_Psychopy\\Attend_ver_005.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('', )
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1707, 1067], fullscr=True, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='ioHub')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "welcome_page" ---
    Welcome_text = visual.TextStim(win=win, name='Welcome_text',
        text='This is a WELCOME page. \n\nPress the Space Bar when you are ready to go on.',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    welcome_key = keyboard.Keyboard()
    # Run 'Begin Experiment' code from Setting_up
    video_options = {
        '1: Cognitive_Neuroscience_Methods': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Method.mp4',
        '2: Attention and Awareness': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Awareness.mp4',
        '3: Nature Nurture': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Nature.mp4',
        '4: Music': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Music.mp4',
        '5: Navigation': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Navigation.mp4',
        '6: Number': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Videos/Number.mp4'
    }
    question_options = {
        '1: Cognitive_Neuroscience_Methods': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Method.csv',
        '2: Attention and Awareness': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Awareness.csv',
        '3: Nature Nurture': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Nature.csv',
        '4: Music': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Music.csv',
        '5: Navigation': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Navigation.csv',
        '6: Number': 'C:/Users/TheLivingLab_Attend/Desktop/muse-lsl-cu-main/AiL_Question_sets/Shuffled_Question_Number.csv'
    }
    selected_video_path = video_options[expInfo['Video_Choice']]
    selected_question_path = question_options[expInfo['Video_Choice']]
    
    # --- Initialize components for Routine "Resting_State" ---
    Resting_text = visual.TextStim(win=win, name='Resting_text',
        text='This is a Resting State Page.\n\nPlease Close your eyes for 4 minutes and relax. \n\n',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    skip_button = keyboard.Keyboard()
    
    # --- Initialize components for Routine "Fixation_with_sound" ---
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='The next page will be a Resting State Page. \n\n You will need to close your eyes and relax for 4 minutes. \n\nWhen time is up, you will hear a notification sound. \n\n Please press Space if you are ready to begin',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_button = keyboard.Keyboard()
    
    # --- Initialize components for Routine "video_sections_1" ---
    lecture_sections = visual.MovieStim(
        win, name='lecture_sections',
        filename=selected_video_path, movieLib='ffpyplayer',
        loop=False, volume=0.8, noAudio=False,
        pos=(0, 0), size=(1.3, 0.8), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    skip_video = keyboard.Keyboard()
    # Run 'Begin Experiment' code from code
    qp = 0
    qn = 0
    starts= []
    lens= []
    video_pick = expInfo.get('Video_Choice')
    if '1: Cognitive_Neuroscience_Methods' in video_pick:
        starts = [98, 279, 680, 931, 1156, 1438, 2062, 2243, 2424, 2605, 2781, 2946, 3121, 3301, 3483]
        lens = [180, 199, 250, 224, 194, 176, 180, 180, 180, 180, 164, 174, 179, 182, 147]
    if '2: Attention and Awareness' in video_pick:
        starts = [0, 279, 680, 931, 1156, 1130, 1303, 1517, 1673, 1897, 2034, 2204, 2405, 2755, 2926]
        lens = [205, 199, 250, 224, 194, 172, 213, 156, 223, 136, 169, 200, 157, 170, 230]
    if '3: Nature Nurture' in video_pick:
        starts = [163, 382, 550, 736, 1003, 1130, 1276, 1457, 1689, 1939, 2193, 2322, 2418, 2537, 3313]
        lens = [219, 168, 186, 267, 127, 146, 181, 232, 250, 254, 129, 96, 119, 279, 128]
    if '4: Music' in video_pick:
        starts = [475, 660, 840, 945, 1125, 1365, 1545, 1670, 1830, 2100, 2265, 2520, 2670, 2910, 3105]
    
        lens = [185, 180, 30, 180, 240, 180, 125, 160, 270, 165, 255, 150, 240, 195, 165]
    if '5: Navigation' in video_pick:
        starts = [793, 974, 1164, 1342, 1511, 1710, 1881, 2083, 2251, 2442, 2600, 2759, 2968, 3160, 3354]
        lens = [180, 190, 178, 169, 199, 171, 202, 168, 191, 158, 159, 209, 192, 194, 222]
    if '6: Number' in video_pick:
        starts = [190, 390, 621, 840, 1054, 1287, 1478, 1659, 1882, 2144, 2415, 2615, 2802, 3008, 3251]
        lens = [200, 231, 219, 207, 233, 191, 181, 223, 262, 204, 200, 187, 206, 243, 192]
    
    
    pointer = starts[qp]   
    du = lens[qp]
    
    
    
    # --- Initialize components for Routine "Engagement_1" ---
    Engagement = visual.TextStim(win=win, name='Engagement',
        text='How engaged were you during the most recent video clip?',
        font='Open Sans',
        units='norm', pos=(0, 0.75), height=0.09, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    E_option1 = visual.TextStim(win=win, name='E_option1',
        text='1. Very engaged',
        font='Open Sans',
        units='norm', pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    E_option2 = visual.TextStim(win=win, name='E_option2',
        text='2. Not very engaged',
        font='Open Sans',
        units='norm', pos=(0, -0.3), height=0.08, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    E_answers = keyboard.Keyboard()
    
    # --- Initialize components for Routine "DS_or_AS" ---
    # Run 'Begin Experiment' code from code_3
    row_num = 0
    selected_rows = f"{row_num}: {row_num + 2}"
    text_questions = visual.TextStim(win=win, name='text_questions',
        text='',
        font='Open Sans',
        units='norm', pos=(0, 0.8), height=0.08, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_option1 = visual.TextStim(win=win, name='text_option1',
        text='',
        font='Open Sans',
        units='norm', pos=(0, 0.35), height=0.06, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    text_option2 = visual.TextStim(win=win, name='text_option2',
        text='',
        font='Open Sans',
        units='norm', pos=(0,0), height=0.06, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None,
        languageStyle='LTR',
        depth=-3.0);
    text_option3 = visual.TextStim(win=win, name='text_option3',
        text='',
        font='Open Sans',
        units='norm', pos=(0, -0.4), height=0.06, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    text_option4 = visual.TextStim(win=win, name='text_option4',
        text='',
        font='Open Sans',
        units='norm', pos=(0, -0.75), height=0.06, wrapWidth=1.6, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    key_resp = keyboard.Keyboard()
    
    # --- Initialize components for Routine "S_question" ---
    Source = visual.TextStim(win=win, name='Source',
        text='How did you answer the previous question?',
        font='Open Sans',
        units='norm', pos=(0, 0.75), height=0.09, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    S_option1 = visual.TextStim(win=win, name='S_option1',
        text='',
        font='Open Sans',
        units='norm', pos=(0, 0.3), height=0.07, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    S_option2 = visual.TextStim(win=win, name='S_option2',
        text='2. I already knew it before the lecture',
        font='Open Sans',
        units='norm', pos=(0, 0), height=0.07, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    S_option3 = visual.TextStim(win=win, name='S_option3',
        text='3.  I totally guessed.',
        font='Open Sans',
        units='norm', pos=(0, -0.3), height=0.07, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    C_resp = keyboard.Keyboard()
    
    # --- Initialize components for Routine "C_question" ---
    Confidence = visual.TextStim(win=win, name='Confidence',
        text='',
        font='Open Sans',
        units='norm', pos=(0, 0.75), height=0.09, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    C_option1 = visual.TextStim(win=win, name='C_option1',
        text='',
        font='Open Sans',
        units='norm', pos=(0, 0), height=0.08, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    C_option2 = visual.TextStim(win=win, name='C_option2',
        text='',
        font='Open Sans',
        units='norm', pos=(0, -0.3), height=0.08, wrapWidth=1.8, ori=0.0,
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    C_answers = keyboard.Keyboard()
    
    # --- Initialize components for Routine "fixation" ---
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.5, 0.5),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "Resting_State" ---
    Resting_text = visual.TextStim(win=win, name='Resting_text',
        text='This is a Resting State Page.\n\nPlease Close your eyes for 4 minutes and relax. \n\nWhen time is on, you will hear a notification sound.',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    skip_button = keyboard.Keyboard()
    
    # --- Initialize components for Routine "Fixation_with_sound" ---
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='Now, to continue, press Space',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_button = keyboard.Keyboard()
    
    # --- Initialize components for Routine "End_page" ---
    text = visual.TextStim(win=win, name='text',
        text="You are done.\n\nThank you for participation.\n\nPress 'Space' to exit",
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    exit_key = keyboard.Keyboard()
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)
    
    # --- Prepare to start Routine "welcome_page" ---
    continueRoutine = True
    # update component parameters for each repeat
    markername = 'welcome_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    welcome_key.keys = []
    welcome_key.rt = []
    _welcome_key_allKeys = []
    # keep track of which components have finished
    welcome_pageComponents = [Welcome_text, welcome_key]
    for thisComponent in welcome_pageComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "welcome_page" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Welcome_text* updates
        
        # if Welcome_text is starting this frame...
        if Welcome_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Welcome_text.frameNStart = frameN  # exact frame index
            Welcome_text.tStart = t  # local t and not account for scr refresh
            Welcome_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Welcome_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Welcome_text.started')
            # update status
            Welcome_text.status = STARTED
            Welcome_text.setAutoDraw(True)
        
        # if Welcome_text is active this frame...
        if Welcome_text.status == STARTED:
            # update params
            pass
        
        # *welcome_key* updates
        waitOnFlip = False
        
        # if welcome_key is starting this frame...
        if welcome_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            welcome_key.frameNStart = frameN  # exact frame index
            welcome_key.tStart = t  # local t and not account for scr refresh
            welcome_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcome_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcome_key.started')
            # update status
            welcome_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(welcome_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(welcome_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if welcome_key.status == STARTED and not waitOnFlip:
            theseKeys = welcome_key.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _welcome_key_allKeys.extend(theseKeys)
            if len(_welcome_key_allKeys):
                welcome_key.keys = _welcome_key_allKeys[-1].name  # just the last key pressed
                welcome_key.rt = _welcome_key_allKeys[-1].rt
                welcome_key.duration = _welcome_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in welcome_pageComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "welcome_page" ---
    for thisComponent in welcome_pageComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    markername = 'welcome_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if welcome_key.keys in ['', [], None]:  # No response was made
        welcome_key.keys = None
    thisExp.addData('welcome_key.keys',welcome_key.keys)
    if welcome_key.keys != None:  # we had a response
        thisExp.addData('welcome_key.rt', welcome_key.rt)
        thisExp.addData('welcome_key.duration', welcome_key.duration)
    thisExp.nextEntry()
    # the Routine "welcome_page" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    time.sleep(1)
    # --- Prepare to start Routine "Resting_State" ---
    continueRoutine = True
    markername = 'pre_rest_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    skip_button.keys = []
    skip_button.rt = []
    _skip_button_allKeys = []
    # keep track of which components have finished
    Resting_StateComponents = [Resting_text, skip_button]
    for thisComponent in Resting_StateComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Resting_State" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # is it time to end the Routine? (based on local clock)
        if tThisFlip > 240-frameTolerance:
            continueRoutine = False
        
        # *Resting_text* updates
        
        # if Resting_text is starting this frame...
        if Resting_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Resting_text.frameNStart = frameN  # exact frame index
            Resting_text.tStart = t  # local t and not account for scr refresh
            Resting_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Resting_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Resting_text.started')
            # update status
            Resting_text.status = STARTED
            Resting_text.setAutoDraw(True)
        
        # if Resting_text is active this frame...
        if Resting_text.status == STARTED:
            # update params
            pass
        
        # if Resting_text is stopping this frame...
        if Resting_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Resting_text.tStartRefresh + 240-frameTolerance:
                # keep track of stop time/frame for later
                Resting_text.tStop = t  # not accounting for scr refresh
                Resting_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Resting_text.stopped')
                # update status
                Resting_text.status = FINISHED
                Resting_text.setAutoDraw(False)
        
        # *skip_button* updates
        waitOnFlip = False
        
        # if skip_button is starting this frame...
        if skip_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            skip_button.frameNStart = frameN  # exact frame index
            skip_button.tStart = t  # local t and not account for scr refresh
            skip_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(skip_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'skip_button.started')
            # update status
            skip_button.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(skip_button.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(skip_button.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if skip_button.status == STARTED and not waitOnFlip:
            theseKeys = skip_button.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _skip_button_allKeys.extend(theseKeys)
            if len(_skip_button_allKeys):
                skip_button.keys = _skip_button_allKeys[-1].name  # just the last key pressed
                skip_button.rt = _skip_button_allKeys[-1].rt
                skip_button.duration = _skip_button_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Resting_StateComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Resting_State" ---
    for thisComponent in Resting_StateComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    markername = 'pre_rest_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if skip_button.keys in ['', [], None]:  # No response was made
        skip_button.keys = None
    thisExp.addData('skip_button.keys',skip_button.keys)
    if skip_button.keys != None:  # we had a response
        thisExp.addData('skip_button.rt', skip_button.rt)
        thisExp.addData('skip_button.duration', skip_button.duration)
    thisExp.nextEntry()
    # the Routine "Resting_State" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Fixation_with_sound" ---
    continueRoutine = True
    # update component parameters for each repeat
    markername = 'fixation_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    key_button.keys = []
    key_button.rt = []
    _key_button_allKeys = []
    # Run 'Begin Routine' code from play_beep

    winsound.PlaySound('C://Users//TheLivingLab_Attend//Desktop//muse-lsl-cu-main//beep-09.wav', winsound.SND_FILENAME)
    # keep track of which components have finished
    Fixation_with_soundComponents = [Fixation, key_button]
    for thisComponent in Fixation_with_soundComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Fixation_with_sound" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Fixation* updates
        
        # if Fixation is starting this frame...
        if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Fixation.frameNStart = frameN  # exact frame index
            Fixation.tStart = t  # local t and not account for scr refresh
            Fixation.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Fixation.started')
            # update status
            Fixation.status = STARTED
            Fixation.setAutoDraw(True)
        
        # if Fixation is active this frame...
        if Fixation.status == STARTED:
            # update params
            pass
        
        # *key_button* updates
        waitOnFlip = False
        
        # if key_button is starting this frame...
        if key_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_button.frameNStart = frameN  # exact frame index
            key_button.tStart = t  # local t and not account for scr refresh
            key_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_button.started')
            # update status
            key_button.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_button.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_button.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_button.status == STARTED and not waitOnFlip:
            theseKeys = key_button.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_button_allKeys.extend(theseKeys)
            if len(_key_button_allKeys):
                key_button.keys = _key_button_allKeys[-1].name  # just the last key pressed
                key_button.rt = _key_button_allKeys[-1].rt
                key_button.duration = _key_button_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Fixation_with_soundComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Fixation_with_sound" ---
    for thisComponent in Fixation_with_soundComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    markername = 'fixation_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if key_button.keys in ['', [], None]:  # No response was made
        key_button.keys = None
    thisExp.addData('key_button.keys',key_button.keys)
    if key_button.keys != None:  # we had a response
        thisExp.addData('key_button.rt', key_button.rt)
        thisExp.addData('key_button.duration', key_button.duration)
    thisExp.nextEntry()
    # the Routine "Fixation_with_sound" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    Lecture_trials = data.TrialHandler(nReps=3.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='Lecture_trials')
    thisExp.addLoop(Lecture_trials)  # add the loop to the experiment
    thisLecture_trial = Lecture_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLecture_trial.rgb)
    if thisLecture_trial != None:
        for paramName in thisLecture_trial:
            globals()[paramName] = thisLecture_trial[paramName]
    
    for thisLecture_trial in Lecture_trials:
        currentLoop = Lecture_trials
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisLecture_trial.rgb)
        if thisLecture_trial != None:
            for paramName in thisLecture_trial:
                globals()[paramName] = thisLecture_trial[paramName]
        
        # set up handler to look after randomisation of conditions etc
        Section_trials = data.TrialHandler(nReps=5.0, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='Section_trials')
        thisExp.addLoop(Section_trials)  # add the loop to the experiment
        thisSection_trial = Section_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSection_trial.rgb)
        if thisSection_trial != None:
            for paramName in thisSection_trial:
                globals()[paramName] = thisSection_trial[paramName]
        
        for thisSection_trial in Section_trials:
            currentLoop = Section_trials
            thisExp.timestampOnFlip(win, 'thisRow.t')
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    inputs=inputs, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisSection_trial.rgb)
            if thisSection_trial != None:
                for paramName in thisSection_trial:
                    globals()[paramName] = thisSection_trial[paramName]
            
            # --- Prepare to start Routine "video_sections_1" ---
            continueRoutine = True
            # update component parameters for each repeat
            thisExp.addData('video_sections_1.started', globalClock.getTime())
            skip_video.keys = []
            skip_video.rt = []
            _skip_video_allKeys = []
            # Run 'Begin Routine' code from code
            lecture_sections.seek(pointer)
            # keep track of which components have finished
            video_sections_1Components = [lecture_sections, skip_video]
            for thisComponent in video_sections_1Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "video_sections_1" ---
            routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *lecture_sections* updates
                
                # if lecture_sections is starting this frame...
                if lecture_sections.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    lecture_sections.frameNStart = frameN  # exact frame index
                    lecture_sections.tStart = t  # local t and not account for scr refresh
                    lecture_sections.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(lecture_sections, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'lecture_sections.started')
                    # update status
                    lecture_sections.status = STARTED
                    lecture_sections.setAutoDraw(True)
                    marker_name = 'VideoStim{}_started'.format(qp+1)
                    outlet.push_sample([markernames[marker_name]], time.time())
                    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                    thisExp.addData(marker_name, absolute_timestamp)
                    lecture_sections.play()
                
                # if lecture_sections is stopping this frame...
                if lecture_sections.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > lecture_sections.tStartRefresh + du-frameTolerance:
                        # keep track of stop time/frame for later
                        lecture_sections.tStop = t  # not accounting for scr refresh
                        lecture_sections.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'lecture_sections.stopped')
                        # update status
                        lecture_sections.status = FINISHED
                        lecture_sections.setAutoDraw(False)
                        lecture_sections.stop()
                if lecture_sections.isFinished:  # force-end the Routine
                    continueRoutine = False
                
                # *skip_video* updates
                waitOnFlip = False
                
                # if skip_video is starting this frame...
                if skip_video.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    skip_video.frameNStart = frameN  # exact frame index
                    skip_video.tStart = t  # local t and not account for scr refresh
                    skip_video.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(skip_video, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'skip_video.started')
                    # update status
                    skip_video.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(skip_video.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(skip_video.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if skip_video.status == STARTED and not waitOnFlip:
                    theseKeys = skip_video.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
                    _skip_video_allKeys.extend(theseKeys)
                    if len(_skip_video_allKeys):
                        skip_video.keys = _skip_video_allKeys[-1].name  # just the last key pressed
                        skip_video.rt = _skip_video_allKeys[-1].rt
                        skip_video.duration = _skip_video_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, inputs=inputs, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in video_sections_1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "video_sections_1" ---
            for thisComponent in video_sections_1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            thisExp.addData('video_sections_1.stopped', globalClock.getTime())

            lecture_sections.stop()  # ensure movie has stopped at end of Routine
            absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
            marker_name = 'VideoStim{}_stopped'.format(qp+1)
            outlet.push_sample([markernames[marker_name]], time.time())
            thisExp.addData(marker_name, absolute_timestamp)
            # check responses
            if skip_video.keys in ['', [], None]:  # No response was made
                skip_video.keys = None
            Section_trials.addData('skip_video.keys',skip_video.keys)
            if skip_video.keys != None:  # we had a response
                Section_trials.addData('skip_video.rt', skip_video.rt)
                Section_trials.addData('skip_video.duration', skip_video.duration)
            # Run 'End Routine' code from code
            if qp <=13:
                qp+=1
            pointer = starts[qp]   
            du = lens[qp]
            # the Routine "video_sections_1" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            time.sleep(1)

            # --- Prepare to start Routine "Engagement_1" ---
            continueRoutine = True
            # update component parameters for each repeat
            absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
            marker_name = f'question{qn+1}_started'
            thisExp.addData(marker_name, absolute_timestamp)
            outlet.push_sample([markernames[marker_name]], time.time())
            E_answers.keys = []
            E_answers.rt = []
            _E_answers_allKeys = []
            # keep track of which components have finished
            Engagement_1Components = [Engagement, E_option1, E_option2, E_answers]
            for thisComponent in Engagement_1Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Engagement_1" ---
            routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # is it time to end the Routine? (based on local clock)
                if tThisFlip > 75-frameTolerance:
                    continueRoutine = False
                
                # *Engagement* updates
                
                # if Engagement is starting this frame...
                if Engagement.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    Engagement.frameNStart = frameN  # exact frame index
                    Engagement.tStart = t  # local t and not account for scr refresh
                    Engagement.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(Engagement, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Engagement.started')
                    # update status
                    Engagement.status = STARTED
                    Engagement.setAutoDraw(True)
                
                # if Engagement is active this frame...
                if Engagement.status == STARTED:
                    # update params
                    pass
                
                # *E_option1* updates
                
                # if E_option1 is starting this frame...
                if E_option1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    E_option1.frameNStart = frameN  # exact frame index
                    E_option1.tStart = t  # local t and not account for scr refresh
                    E_option1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(E_option1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'E_option1.started')
                    # update status
                    E_option1.status = STARTED
                    E_option1.setAutoDraw(True)
                
                # if E_option1 is active this frame...
                if E_option1.status == STARTED:
                    # update params
                    pass
                
                # *E_option2* updates
                
                # if E_option2 is starting this frame...
                if E_option2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    E_option2.frameNStart = frameN  # exact frame index
                    E_option2.tStart = t  # local t and not account for scr refresh
                    E_option2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(E_option2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'E_option2.started')
                    # update status
                    E_option2.status = STARTED
                    E_option2.setAutoDraw(True)
                
                # if E_option2 is active this frame...
                if E_option2.status == STARTED:
                    # update params
                    pass
                
                # *E_answers* updates
                waitOnFlip = False
                
                # if E_answers is starting this frame...
                if E_answers.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    E_answers.frameNStart = frameN  # exact frame index
                    E_answers.tStart = t  # local t and not account for scr refresh
                    E_answers.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(E_answers, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'E_answers.started')
                    # update status
                    E_answers.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(E_answers.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(E_answers.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if E_answers.status == STARTED and not waitOnFlip:
                    theseKeys = E_answers.getKeys(keyList=['1','2'], ignoreKeys=["escape"], waitRelease=False)
                    _E_answers_allKeys.extend(theseKeys)
                    if len(_E_answers_allKeys):
                        E_answers.keys = _E_answers_allKeys[-1].name  # just the last key pressed
                        E_answers.rt = _E_answers_allKeys[-1].rt
                        E_answers.duration = _E_answers_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, inputs=inputs, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Engagement_1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Engagement_1" ---
            for thisComponent in Engagement_1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
            marker_name = f'question{qn+1}_stopped'
            qn += 1
            thisExp.addData(marker_name, absolute_timestamp)
            outlet.push_sample([markernames[marker_name]], time.time())
            # check responses
            if E_answers.keys in ['', [], None]:  # No response was made
                E_answers.keys = None
            Section_trials.addData('E_answers.keys',E_answers.keys)
            if E_answers.keys != None:  # we had a response
                Section_trials.addData('E_answers.rt', E_answers.rt)
                Section_trials.addData('E_answers.duration', E_answers.duration)
            # Run 'End Routine' code from code_2

            # the Routine "Engagement_1" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
        # completed 5.0 repeats of 'Section_trials'
        
        
        # set up handler to look after randomisation of conditions etc
        Question_trials = data.TrialHandler(nReps=5.0, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='Question_trials')
        thisExp.addLoop(Question_trials)  # add the loop to the experiment
        thisQuestion_trial = Question_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisQuestion_trial.rgb)
        if thisQuestion_trial != None:
            for paramName in thisQuestion_trial:
                globals()[paramName] = thisQuestion_trial[paramName]
        
        for thisQuestion_trial in Question_trials:
            currentLoop = Question_trials
            thisExp.timestampOnFlip(win, 'thisRow.t')
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    inputs=inputs, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
            )
            # abbreviate parameter names if possible (e.g. rgb = thisQuestion_trial.rgb)
            if thisQuestion_trial != None:
                for paramName in thisQuestion_trial:
                    globals()[paramName] = thisQuestion_trial[paramName]
            
            # set up handler to look after randomisation of conditions etc
            DSCASC_loop = data.TrialHandler(nReps=1.0, method='sequential', 
                extraInfo=expInfo, originPath=-1,
                trialList=data.importConditions(selected_question_path, selection=selected_rows),
                seed=None, name='DSCASC_loop')
            thisExp.addLoop(DSCASC_loop)  # add the loop to the experiment
            thisDSCASC_loop = DSCASC_loop.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisDSCASC_loop.rgb)
            if thisDSCASC_loop != None:
                for paramName in thisDSCASC_loop:
                    globals()[paramName] = thisDSCASC_loop[paramName]
            
            for thisDSCASC_loop in DSCASC_loop:
                currentLoop = DSCASC_loop
                thisExp.timestampOnFlip(win, 'thisRow.t')
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        inputs=inputs, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                )
                # abbreviate parameter names if possible (e.g. rgb = thisDSCASC_loop.rgb)
                if thisDSCASC_loop != None:
                    for paramName in thisDSCASC_loop:
                        globals()[paramName] = thisDSCASC_loop[paramName]
                time.sleep(1)

                # --- Prepare to start Routine "DS_or_AS" ---
                continueRoutine = True
                # update component parameters for each repeat
                absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                marker_name = f'question{qn+1}_started'
                thisExp.addData(marker_name, absolute_timestamp)
                outlet.push_sample([markernames[marker_name]], time.time())
                text_questions.setText(Questions)
                text_option1.setText(option1)
                text_option2.setText(option2
                )
                text_option3.setText(option3
                )
                text_option4.setText(option4
                )
                text_option1.alignText='left'
                text_option2.alignText ='left'
                text_option3.alignText ='left'
                text_option4.alignText ='left'
                key_resp.keys = []
                key_resp.rt = []
                _key_resp_allKeys = []
                # keep track of which components have finished
                DS_or_ASComponents = [text_questions, text_option1, text_option2, text_option3, text_option4, key_resp]
                for thisComponent in DS_or_ASComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "DS_or_AS" ---
                routineForceEnded = not continueRoutine
                while continueRoutine:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    # is it time to end the Routine? (based on local clock)
                    if tThisFlip > 75-frameTolerance:
                        continueRoutine = False
                    
                    # *text_questions* updates
                    
                    # if text_questions is starting this frame...
                    if text_questions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_questions.frameNStart = frameN  # exact frame index
                        text_questions.tStart = t  # local t and not account for scr refresh
                        text_questions.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_questions, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_questions.started')
                        # update status
                        text_questions.status = STARTED
                        text_questions.setAutoDraw(True)
                    
                    # if text_questions is active this frame...
                    if text_questions.status == STARTED:
                        # update params
                        pass
                    
                    # *text_option1* updates
                    
                    # if text_option1 is starting this frame...
                    if text_option1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_option1.frameNStart = frameN  # exact frame index
                        text_option1.tStart = t  # local t and not account for scr refresh
                        text_option1.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_option1, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_option1.started')
                        # update status
                        text_option1.status = STARTED
                        text_option1.setAutoDraw(True)
                    
                    # if text_option1 is active this frame...
                    if text_option1.status == STARTED:
                        # update params
                        pass
                    
                    # *text_option2* updates
                    
                    # if text_option2 is starting this frame...
                    if text_option2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_option2.frameNStart = frameN  # exact frame index
                        text_option2.tStart = t  # local t and not account for scr refresh
                        text_option2.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_option2, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_option2.started')
                        # update status
                        text_option2.status = STARTED
                        text_option2.setAutoDraw(True)
                    
                    # if text_option2 is active this frame...
                    if text_option2.status == STARTED:
                        # update params
                        pass
                    
                    # *text_option3* updates
                    
                    # if text_option3 is starting this frame...
                    if text_option3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_option3.frameNStart = frameN  # exact frame index
                        text_option3.tStart = t  # local t and not account for scr refresh
                        text_option3.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_option3, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_option3.started')
                        # update status
                        text_option3.status = STARTED
                        text_option3.setAutoDraw(True)
                    
                    # if text_option3 is active this frame...
                    if text_option3.status == STARTED:
                        # update params
                        pass
                    
                    # *text_option4* updates
                    
                    # if text_option4 is starting this frame...
                    if text_option4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_option4.frameNStart = frameN  # exact frame index
                        text_option4.tStart = t  # local t and not account for scr refresh
                        text_option4.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_option4, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_option4.started')
                        # update status
                        text_option4.status = STARTED
                        text_option4.setAutoDraw(True)
                    
                    # if text_option4 is active this frame...
                    if text_option4.status == STARTED:
                        # update params
                        pass
                    
                    # *key_resp* updates
                    waitOnFlip = False
                    
                    # if key_resp is starting this frame...
                    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        key_resp.frameNStart = frameN  # exact frame index
                        key_resp.tStart = t  # local t and not account for scr refresh
                        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'key_resp.started')
                        # update status
                        key_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if key_resp.status == STARTED and not waitOnFlip:
                        theseKeys = key_resp.getKeys(keyList=['1','2','3','4'], ignoreKeys=["escape"], waitRelease=False)
                        _key_resp_allKeys.extend(theseKeys)
                        if len(_key_resp_allKeys):
                            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                            key_resp.rt = _key_resp_allKeys[-1].rt
                            key_resp.duration = _key_resp_allKeys[-1].duration
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, inputs=inputs, win=win)
                        return
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in DS_or_ASComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "DS_or_AS" ---
                for thisComponent in DS_or_ASComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                marker_name = f'question{qn+1}_stopped'
                qn+=1
                thisExp.addData(marker_name, absolute_timestamp)
                outlet.push_sample([markernames[marker_name]], time.time())
                # check responses
                if key_resp.keys in ['', [], None]:  # No response was made
                    key_resp.keys = None
                DSCASC_loop.addData('key_resp.keys',key_resp.keys)
                if key_resp.keys != None:  # we had a response
                    DSCASC_loop.addData('key_resp.rt', key_resp.rt)
                    DSCASC_loop.addData('key_resp.duration', key_resp.duration)
                # the Routine "DS_or_AS" was not non-slip safe, so reset the non-slip timer
                if str(key_resp.keys) == str(CorrectAnswer):
                    DSCASC_loop.addData('AnswerCorrect', 'True')
                else:
                    DSCASC_loop.addData('AnswerCorrect', 'False')
                routineTimer.reset()
                time.sleep(1)
                
                # --- Prepare to start Routine "S_question" ---
                continueRoutine = True
                # update component parameters for each repeat
                absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                marker_name = f'question{qn+1}_started'
                thisExp.addData(marker_name, absolute_timestamp)
                outlet.push_sample([markernames[marker_name]], time.time())
                S_option1.setText('1. I learned the answer during the lecture.')
                # Run 'Begin Routine' code from code_5
                skipC = False
                C_resp.keys = []
                C_resp.rt = []
                _C_resp_allKeys = []
                # keep track of which components have finished
                S_questionComponents = [Source, S_option1, S_option2, S_option3, C_resp]
                for thisComponent in S_questionComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "S_question" ---
                routineForceEnded = not continueRoutine
                while continueRoutine:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    # is it time to end the Routine? (based on local clock)
                    if tThisFlip > 75-frameTolerance:
                        continueRoutine = False
                    
                    # *Source* updates
                    
                    # if Source is starting this frame...
                    if Source.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        Source.frameNStart = frameN  # exact frame index
                        Source.tStart = t  # local t and not account for scr refresh
                        Source.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(Source, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Source.started')
                        # update status
                        Source.status = STARTED
                        Source.setAutoDraw(True)
                    
                    # if Source is active this frame...
                    if Source.status == STARTED:
                        # update params
                        pass
                    
                    # *S_option1* updates
                    
                    # if S_option1 is starting this frame...
                    if S_option1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        S_option1.frameNStart = frameN  # exact frame index
                        S_option1.tStart = t  # local t and not account for scr refresh
                        S_option1.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(S_option1, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'S_option1.started')
                        # update status
                        S_option1.status = STARTED
                        S_option1.setAutoDraw(True)
                    
                    # if S_option1 is active this frame...
                    if S_option1.status == STARTED:
                        # update params
                        pass
                    
                    # *S_option2* updates
                    
                    # if S_option2 is starting this frame...
                    if S_option2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        S_option2.frameNStart = frameN  # exact frame index
                        S_option2.tStart = t  # local t and not account for scr refresh
                        S_option2.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(S_option2, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'S_option2.started')
                        # update status
                        S_option2.status = STARTED
                        S_option2.setAutoDraw(True)
                    
                    # if S_option2 is active this frame...
                    if S_option2.status == STARTED:
                        # update params
                        pass
                    
                    # *S_option3* updates
                    
                    # if S_option3 is starting this frame...
                    if S_option3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        S_option3.frameNStart = frameN  # exact frame index
                        S_option3.tStart = t  # local t and not account for scr refresh
                        S_option3.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(S_option3, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'S_option3.started')
                        # update status
                        S_option3.status = STARTED
                        S_option3.setAutoDraw(True)
                    
                    # if S_option3 is active this frame...
                    if S_option3.status == STARTED:
                        # update params
                        pass
                    
                    # *C_resp* updates
                    waitOnFlip = False
                    
                    # if C_resp is starting this frame...
                    if C_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        C_resp.frameNStart = frameN  # exact frame index
                        C_resp.tStart = t  # local t and not account for scr refresh
                        C_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(C_resp, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'C_resp.started')
                        # update status
                        C_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(C_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(C_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if C_resp.status == STARTED and not waitOnFlip:
                        theseKeys = C_resp.getKeys(keyList=['1','2','3'], ignoreKeys=["escape"], waitRelease=False)
                        _C_resp_allKeys.extend(theseKeys)
                        if len(_C_resp_allKeys):
                            C_resp.keys = _C_resp_allKeys[-1].name  # just the last key pressed
                            C_resp.rt = _C_resp_allKeys[-1].rt
                            C_resp.duration = _C_resp_allKeys[-1].duration
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, inputs=inputs, win=win)
                        return
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in S_questionComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "S_question" ---
                for thisComponent in S_questionComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                marker_name = f'question{qn+1}_stopped'
                thisExp.addData(marker_name, absolute_timestamp)
                outlet.push_sample([markernames[marker_name]], time.time())
                # Run 'End Routine' code from code_5
                qn+=1
                if '1' not in C_resp.keys:
                    skipC = True
                
                # check responses
                if C_resp.keys in ['', [], None]:  # No response was made
                    C_resp.keys = None
                DSCASC_loop.addData('C_resp.keys',C_resp.keys)
                if C_resp.keys != None:  # we had a response
                    DSCASC_loop.addData('C_resp.rt', C_resp.rt)
                    DSCASC_loop.addData('C_resp.duration', C_resp.duration)
                # the Routine "S_question" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                time.sleep(1)

                # --- Prepare to start Routine "C_question" ---
                continueRoutine = True
                # update component parameters for each repeat
                if skipC is True:
                    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                    thisExp.addData(f'question{qn + 1}_skipped', absolute_timestamp)
                else:
                    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                    marker_name = f'question{qn+1}_started'
                    thisExp.addData(marker_name, absolute_timestamp)
                    outlet.push_sample([markernames[marker_name]], time.time())
                # skip this Routine if its 'Skip if' condition is True
                continueRoutine = continueRoutine and not (skipC)
                Confidence.setText('How confident are you that the response you chose is correct? ')
                C_option1.setText('1. Very Confident')
                C_option2.setText('2. Not very confident')
                C_answers.keys = []
                C_answers.rt = []
                _C_answers_allKeys = []
                # keep track of which components have finished
                C_questionComponents = [Confidence, C_option1, C_option2, C_answers]
                for thisComponent in C_questionComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "C_question" ---
                routineForceEnded = not continueRoutine
                while continueRoutine:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    # is it time to end the Routine? (based on local clock)
                    if tThisFlip > 75-frameTolerance:
                        continueRoutine = False
                    
                    # *Confidence* updates
                    
                    # if Confidence is starting this frame...
                    if Confidence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        Confidence.frameNStart = frameN  # exact frame index
                        Confidence.tStart = t  # local t and not account for scr refresh
                        Confidence.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(Confidence, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Confidence.started')
                        # update status
                        Confidence.status = STARTED
                        Confidence.setAutoDraw(True)
                    
                    # if Confidence is active this frame...
                    if Confidence.status == STARTED:
                        # update params
                        pass
                    
                    # *C_option1* updates
                    
                    # if C_option1 is starting this frame...
                    if C_option1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        C_option1.frameNStart = frameN  # exact frame index
                        C_option1.tStart = t  # local t and not account for scr refresh
                        C_option1.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(C_option1, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'C_option1.started')
                        # update status
                        C_option1.status = STARTED
                        C_option1.setAutoDraw(True)
                    
                    # if C_option1 is active this frame...
                    if C_option1.status == STARTED:
                        # update params
                        pass
                    
                    # *C_option2* updates
                    
                    # if C_option2 is starting this frame...
                    if C_option2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        C_option2.frameNStart = frameN  # exact frame index
                        C_option2.tStart = t  # local t and not account for scr refresh
                        C_option2.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(C_option2, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'C_option2.started')
                        # update status
                        C_option2.status = STARTED
                        C_option2.setAutoDraw(True)
                    
                    # if C_option2 is active this frame...
                    if C_option2.status == STARTED:
                        # update params
                        pass
                    
                    # *C_answers* updates
                    waitOnFlip = False
                    
                    # if C_answers is starting this frame...
                    if C_answers.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        C_answers.frameNStart = frameN  # exact frame index
                        C_answers.tStart = t  # local t and not account for scr refresh
                        C_answers.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(C_answers, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'C_answers.started')
                        # update status
                        C_answers.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(C_answers.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(C_answers.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if C_answers.status == STARTED and not waitOnFlip:
                        theseKeys = C_answers.getKeys(keyList=['1','2'], ignoreKeys=["escape"], waitRelease=False)
                        _C_answers_allKeys.extend(theseKeys)
                        if len(_C_answers_allKeys):
                            C_answers.keys = _C_answers_allKeys[-1].name  # just the last key pressed
                            C_answers.rt = _C_answers_allKeys[-1].rt
                            C_answers.duration = _C_answers_allKeys[-1].duration
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, inputs=inputs, win=win)
                        return
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in C_questionComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "C_question" ---
                for thisComponent in C_questionComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                if skipC is False:
                    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
                    marker_name = f'question{qn+1}_stopped'
                    thisExp.addData(marker_name, absolute_timestamp)
                    outlet.push_sample([markernames[marker_name]], time.time())
                qn += 1
                # check responses
                if C_answers.keys in ['', [], None]:  # No response was made
                    C_answers.keys = None
                DSCASC_loop.addData('C_answers.keys',C_answers.keys)
                if C_answers.keys != None:  # we had a response
                    DSCASC_loop.addData('C_answers.rt', C_answers.rt)
                    DSCASC_loop.addData('C_answers.duration', C_answers.duration)
                # the Routine "C_question" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
                if thisSession is not None:
                    # if running in a Session with a Liaison client, send data up to now
                    thisSession.sendExperimentData()
                time.sleep(1)
            # completed 1.0 repeats of 'DSCASC_loop'


            # --- Prepare to start Routine "fixation" ---
            continueRoutine = True
            # update component parameters for each repeat
            markername = 'fixation_started'
            absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
            thisExp.addData(markername, absolute_timestamp)
            outlet.push_sample([markernames[markername]], time.time())
            # Run 'Begin Routine' code from code_6
            row_num += 2
            selected_rows = f"{row_num}:{row_num + 2}"
            # keep track of which components have finished
            fixationComponents = [polygon]
            for thisComponent in fixationComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "fixation" ---
            routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 1.0:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # is it time to end the Routine? (based on local clock)
                if tThisFlip > 1-frameTolerance:
                    continueRoutine = False
                
                # *polygon* updates
                
                # if polygon is starting this frame...
                if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.tStart = t  # local t and not account for scr refresh
                    polygon.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon.started')
                    # update status
                    polygon.status = STARTED
                    polygon.setAutoDraw(True)
                
                # if polygon is active this frame...
                if polygon.status == STARTED:
                    # update params
                    pass
                
                # if polygon is stopping this frame...
                if polygon.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > polygon.tStartRefresh + 1.0-frameTolerance:
                        # keep track of stop time/frame for later
                        polygon.tStop = t  # not accounting for scr refresh
                        polygon.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'polygon.stopped')
                        # update status
                        polygon.status = FINISHED
                        polygon.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, inputs=inputs, win=win)
                    return
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in fixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "fixation" ---
            for thisComponent in fixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            markername = 'fixation_stopped'
            absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
            thisExp.addData(markername, absolute_timestamp)
            outlet.push_sample([markernames[markername]], time.time())
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if routineForceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-1.000000)
            thisExp.nextEntry()
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
        # completed 5.0 repeats of 'Question_trials'
        
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 3.0 repeats of 'Lecture_trials'
    
    
    # --- Prepare to start Routine "Resting_State" ---
    continueRoutine = True
    # update component parameters for each repeat
    markername = 'post_rest_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    skip_button.keys = []
    skip_button.rt = []
    _skip_button_allKeys = []
    # keep track of which components have finished
    Resting_StateComponents = [Resting_text, skip_button]
    for thisComponent in Resting_StateComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Resting_State" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # is it time to end the Routine? (based on local clock)
        if tThisFlip > 240-frameTolerance:
            continueRoutine = False
        
        # *Resting_text* updates
        
        # if Resting_text is starting this frame...
        if Resting_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Resting_text.frameNStart = frameN  # exact frame index
            Resting_text.tStart = t  # local t and not account for scr refresh
            Resting_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Resting_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Resting_text.started')
            # update status
            Resting_text.status = STARTED
            Resting_text.setAutoDraw(True)
        
        # if Resting_text is active this frame...
        if Resting_text.status == STARTED:
            # update params
            pass
        
        # if Resting_text is stopping this frame...
        if Resting_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Resting_text.tStartRefresh + 240-frameTolerance:
                # keep track of stop time/frame for later
                Resting_text.tStop = t  # not accounting for scr refresh
                Resting_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Resting_text.stopped')
                # update status
                Resting_text.status = FINISHED
                Resting_text.setAutoDraw(False)
        
        # *skip_button* updates
        waitOnFlip = False
        
        # if skip_button is starting this frame...
        if skip_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            skip_button.frameNStart = frameN  # exact frame index
            skip_button.tStart = t  # local t and not account for scr refresh
            skip_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(skip_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'skip_button.started')
            # update status
            skip_button.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(skip_button.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(skip_button.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if skip_button.status == STARTED and not waitOnFlip:
            theseKeys = skip_button.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _skip_button_allKeys.extend(theseKeys)
            if len(_skip_button_allKeys):
                skip_button.keys = _skip_button_allKeys[-1].name  # just the last key pressed
                skip_button.rt = _skip_button_allKeys[-1].rt
                skip_button.duration = _skip_button_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Resting_StateComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Resting_State" ---
    for thisComponent in Resting_StateComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    markername = 'post_rest_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if skip_button.keys in ['', [], None]:  # No response was made
        skip_button.keys = None
    thisExp.addData('skip_button.keys',skip_button.keys)
    if skip_button.keys != None:  # we had a response
        thisExp.addData('skip_button.rt', skip_button.rt)
        thisExp.addData('skip_button.duration', skip_button.duration)
    thisExp.nextEntry()
    # the Routine "Resting_State" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    time.sleep(1)
    # --- Prepare to start Routine "Fixation_with_sound" ---
    continueRoutine = True
    # update component parameters for each repeat
    markername = 'fixation_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    key_button.keys = []
    key_button.rt = []
    _key_button_allKeys = []
    # Run 'Begin Routine' code from play_beep

    winsound.PlaySound('C://Users//TheLivingLab_Attend//Desktop//muse-lsl-cu-main//beep-09.wav', winsound.SND_FILENAME)
    # keep track of which components have finished
    Fixation_with_soundComponents = [Fixation, key_button]
    for thisComponent in Fixation_with_soundComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Fixation_with_sound" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Fixation* updates
        
        # if Fixation is starting this frame...
        if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Fixation.frameNStart = frameN  # exact frame index
            Fixation.tStart = t  # local t and not account for scr refresh
            Fixation.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Fixation.started')
            # update status
            Fixation.status = STARTED
            Fixation.setAutoDraw(True)
        
        # if Fixation is active this frame...
        if Fixation.status == STARTED:
            # update params
            pass
        
        # *key_button* updates
        waitOnFlip = False
        
        # if key_button is starting this frame...
        if key_button.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_button.frameNStart = frameN  # exact frame index
            key_button.tStart = t  # local t and not account for scr refresh
            key_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_button.started')
            # update status
            key_button.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_button.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_button.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_button.status == STARTED and not waitOnFlip:
            theseKeys = key_button.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_button_allKeys.extend(theseKeys)
            if len(_key_button_allKeys):
                key_button.keys = _key_button_allKeys[-1].name  # just the last key pressed
                key_button.rt = _key_button_allKeys[-1].rt
                key_button.duration = _key_button_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Fixation_with_soundComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Fixation_with_sound" ---
    for thisComponent in Fixation_with_soundComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    markername = 'fixation_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if key_button.keys in ['', [], None]:  # No response was made
        key_button.keys = None
    thisExp.addData('key_button.keys',key_button.keys)
    if key_button.keys != None:  # we had a response
        thisExp.addData('key_button.rt', key_button.rt)
        thisExp.addData('key_button.duration', key_button.duration)
    thisExp.nextEntry()
    # the Routine "Fixation_with_sound" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "End_page" ---
    continueRoutine = True
    # update component parameters for each repeat
    markername = 'goodbye_started'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    exit_key.keys = []
    exit_key.rt = []
    _exit_key_allKeys = []
    # keep track of which components have finished
    End_pageComponents = [text, exit_key]
    for thisComponent in End_pageComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "End_page" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # is it time to end the Routine? (based on local clock)
        if tThisFlip > 10-frameTolerance:
            continueRoutine = False
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # if text is stopping this frame...
        if text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text.tStop = t  # not accounting for scr refresh
                text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.stopped')
                # update status
                text.status = FINISHED
                text.setAutoDraw(False)
        
        # *exit_key* updates
        waitOnFlip = False
        
        # if exit_key is starting this frame...
        if exit_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            exit_key.frameNStart = frameN  # exact frame index
            exit_key.tStart = t  # local t and not account for scr refresh
            exit_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(exit_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'exit_key.started')
            # update status
            exit_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(exit_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(exit_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if exit_key.status == STARTED and not waitOnFlip:
            theseKeys = exit_key.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _exit_key_allKeys.extend(theseKeys)
            if len(_exit_key_allKeys):
                exit_key.keys = _exit_key_allKeys[-1].name  # just the last key pressed
                exit_key.rt = _exit_key_allKeys[-1].rt
                exit_key.duration = _exit_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in End_pageComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "End_page" ---
    for thisComponent in End_pageComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    markername = 'goodbye_stopped'
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(markername, absolute_timestamp)
    outlet.push_sample([markernames[markername]], time.time())
    # check responses
    if exit_key.keys in ['', [], None]:  # No response was made
        exit_key.keys = None
    thisExp.addData('exit_key.keys',exit_key.keys)
    if exit_key.keys != None:  # we had a response
        thisExp.addData('exit_key.rt', exit_key.rt)
        thisExp.addData('exit_key.duration', exit_key.duration)
    thisExp.nextEntry()
    # the Routine "End_page" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)

    event_stop = threading.Event()
    Captured_directory = f"C:\\Users\\TheLivingLab_Attend\\Desktop\\Data\\sub-{expInfo['participant']}\\Video_Captured"
    # Create the directory if it does not exist
    if not os.path.exists(Captured_directory):
        os.makedirs(Captured_directory)
    frame_queues = [queue.Queue(maxsize=60), queue.Queue(maxsize=60)]

    if not os.path.exists(Captured_directory):
        os.makedirs(Captured_directory)
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(f'Recording Started', absolute_timestamp)
    camera_threads = []
    record_filenames = [os.path.join(Captured_directory, f"Sub-{expInfo['participant']}_CAM{i}.avi")
                     for i in range(2)]
    for i in range(2):
        tt = threading.Thread(target=record_camera, args=(i, record_filenames[i], frame_queues[i], event_stop))
        camera_threads.append(tt)
        tt.start()
    # Start writer threads
    writer_threads = []
    for i in range(2):
        tt = threading.Thread(target=write_video, args=(record_filenames[i], frame_queues[i]))
        writer_threads.append(tt)
        tt.start()

    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    event_stop.set()
    for tt in camera_threads:
        tt.join()
    # Wait for all frames to be processed
    for tt in writer_threads:
        tt.join()
    absolute_timestamp = datetime.now().strftime('%H:%M:%S:%f')
    thisExp.addData(f'Recording Saved', absolute_timestamp)
    for q in frame_queues:
        while not q.empty():
            try:
                q.get_nowait()
            except queue.Empty:
                break
    outlet.push_sample([markernames['experiment_stopped']], time.time())
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)
