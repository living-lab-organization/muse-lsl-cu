from psychopy import visual, event, core, gui
import time
import os
import pandas as pd
import subprocess
from make_prediction import process_new_data, make_prediction
import random  # For generating random values in offline mode
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)

##### Remember to change the participant number #####
participant_number = '301'
lecture_video_path = 'C:\\Users\\thb12\\OneDrive\\Desktop\\muse-lsl-cu\\AiL_Videos\\Navigation.mp4'


def find_eeg_csv(participant_number):
    # Define the base directory path
    base_dir = f'C:\\Users\\thb12\\OneDrive\\Desktop\\rtfin-data\\sub-{participant_number}\\Muse_data'
    print("base dir is ", base_dir)

    # Check if the base directory exists
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist.")
        return None

    # Loop through files in the directory and search for the one containing 'EEG_recording'
    for file_name in os.listdir(base_dir):
        if 'EEG_recording' in file_name and file_name.endswith('.csv'):
            csv_file_path = os.path.join(base_dir, file_name)
            return csv_file_path

    print("No appropriate CSV file found.")
    return None


# Path to the model file used for predictions
model_file = 'C:\\Users\\thb12\\OneDrive\\Desktop\\muse-lsl-cu\\svm_model_subject_023.joblib'


# Function to update bar based on ML prediction or random values (offline mode)
def update_bar(csv_file, model_file, offline_mode):
    if offline_mode:
        # Return a random prediction value between 0 and 1 every 5 seconds in offline mode
        return random.uniform(0, 1)
    else:
        # Check if the CSV file exists
        if os.path.exists(csv_file):
            try:
                # Read the CSV file
                df = pd.read_csv(csv_file)
                # Check if we have at least 512 rows
                if len(df) >= 512:
                    # Process the last 512 rows for prediction
                    processed_input = process_new_data(csv_file)

                    # Make prediction using the SVM model
                    prediction = make_prediction(processed_input, model_file)

                    # Return prediction (a value between 0 and 1)
                    return prediction
            except pd.errors.EmptyDataError:
                pass
        return None


info = {'participant': '001',
        'offline-mode': 'True'}

# Create a dialog box
infoDlg = gui.DlgFromDict(dictionary=info, title='Participant Information')
# Toggle offline mode (True for random values, False for real data)
offline_mode = info['offline-mode'] == 'True'
# Check if the user closed the dialog box
if infoDlg.OK:
    csv_file = find_eeg_csv(participant_number)
    win = visual.Window([1920, 1080], fullscr=True)
    video = visual.MovieStim(
        win, name='lecture_sections',
        filename=lecture_video_path, movieLib='ffpyplayer',
        loop=False, volume=0.8, noAudio=False,
        pos=(0, 0), size=(1.1, 1), units=win.units,
        ori=0.0, anchor='center', opacity=None, contrast=1.0,
        depth=0
    )

    # Create a white background rectangle for the bar
    bar_background = visual.Rect(
        win, width=0.4, height=0.05, fillColor='white', pos=(-0.20, -0.7), lineColor=None, anchor='left'
    )

    # Create a black rectangle for the bar that will change its width
    bar_foreground = visual.Rect(
        win, width=0.0, height=0.05, fillColor='blue', pos=(-0.20, -0.7), lineColor=None, anchor='left'
    )

    # Add title above the bar
    title = visual.TextStim(win, text="Attend Score", pos=(0, -0.55), height=0.05, color='white')

    # Add labels at the beginning and end of the bar
    label_0 = visual.TextStim(win, text="0", pos=(-0.22, -0.7), height=0.04, color='black')
    label_10 = visual.TextStim(win, text="10", pos=(0.22, -0.7), height=0.04, color='black')

    # Variable to track the last update time
    last_update_time = time.time()
    update_interval = 8  # Time interval for updating the bar (8 seconds)
    record_duration = 600

    # Initial bar width based on the first prediction (starts at 0)
    current_prediction = 0.0
    new_prediction = 0.0  # To hold the newly fetched prediction
    initial_prediction = current_prediction  # To hold the starting prediction for animation
    animation_duration = 5  # Total time for animation
    animation_start_time = None  # Time when the animation starts

    # Function to get the color based on current_prediction
    def get_color(current_prediction):
        if current_prediction <= 0.5:
            R = 1
            G = current_prediction / 0.5  # G from 0 to 1
            B = 0
        else:
            R = 1 - (current_prediction - 0.5) / 0.5  # R from 1 to 0
            G = 1
            B = 0
        # Convert to PsychoPy color space (-1 to 1)
        R_psychopy = 2 * R - 1
        G_psychopy = 2 * G - 1
        B_psychopy = 2 * B - 1
        return [R_psychopy, G_psychopy, B_psychopy]

    # Main loop to display video and update the bar width based on predictions
    outlet.push_sample([100], time.time())
    while video.status != visual.FINISHED:
        current_time = time.time()

        # If the last update was more than update_interval seconds ago, fetch a new prediction
        if current_time - last_update_time >= update_interval:
            # Fetch a new prediction
            new_prediction = update_bar(csv_file, model_file, offline_mode)
            last_update_time = current_time
            animation_start_time = current_time  # Start the animation
            initial_prediction = current_prediction  # Store the current prediction as the initial value

        # Animate the transition from the initial_prediction to the new_prediction
        if animation_start_time is not None:
            elapsed_time = current_time - animation_start_time
            t = elapsed_time / animation_duration
            if t <= 1:
                # Linear interpolation between initial_prediction and new_prediction
                current_prediction = initial_prediction + (new_prediction - initial_prediction) * t
            else:
                # Once the animation is over, set current_prediction to new_prediction
                current_prediction = new_prediction

        # Update the bar color based on the current_prediction
        bar_foreground.fillColor = get_color(current_prediction)
        bar_foreground.opacity = 0.6  # Make the bar less visible

        # Bar width ranges from 0 (0 width) to 1 (full width of the background)
        bar_foreground.width = 0.4 * current_prediction  # Scale prediction to the bar's maximum width
        print(f"Current Score (0-1 scale): {current_prediction}")

        # Draw the video, title, labels, and the bar
        video.draw()
        title.draw()
        label_0.draw()
        label_10.draw()
        bar_background.draw()
        bar_foreground.draw()

        # Flip the window to update the screen
        win.flip()

        # Check for quit key (escape) or time limit
        if event.getKeys(keyList=["escape"]) or current_time - last_update_time > record_duration:
            break

    # Clean up
    outlet.push_sample([999], time.time())
    win.close()
    core.quit()
