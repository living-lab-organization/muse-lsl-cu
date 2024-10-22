import pandas as pd
import numpy as np
from scipy.signal import welch, get_window, butter, filtfilt
import joblib


# Constants
fs = 256  # Sampling frequency (Hz)
window_size = 256  # samples per window
channels = ['TP9', 'AF7', 'AF8', 'TP10']
bands = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30)}

# Function to apply a band-pass filter to clean EEG data
def apply_bandpass_filter(data, lowcut=1, highcut=60, fs=256, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Function to calculate sliding window PSD
def calculate_psd_for_window(data, fs, window_size, channels, bands):
    results = {}
    window = get_window('hamming', window_size)

    for channel in channels:
        segment_data = data[channel].values
        f, psd = welch(segment_data, fs=fs, window=window, nperseg=window_size)
        for band, (low, high) in bands.items():
            idx_band = (f >= low) & (f <= high)
            if f'avg_{band}_psd' not in results:
                results[f'avg_{band}_psd'] = []
            results[f'avg_{band}_psd'].append(np.mean(psd[idx_band]))

    # Average PSD values across all channels for each band
    for band in bands.keys():
        results[f'avg_{band}_psd'] = np.mean(results[f'avg_{band}_psd'])

    return results

# Function to process new data for prediction
def process_new_data(file_path,index=0):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Take the last 512 rows of data
    df_last_512 = df.tail(256*6)

    # Apply bandpass filtering to each channel
    for channel in channels:
        df_last_512[channel] = apply_bandpass_filter(df_last_512[channel].values, fs=fs)

    # Calculate PSD and average over the 512 rows
    psd_values = calculate_psd_for_window(df_last_512, fs, window_size, channels, bands)

    # Convert to a DataFrame (1 row)
    input_df = pd.DataFrame([psd_values])
    print(input_df.head())
    return input_df

# Function to make predictions using the saved SVM model
def make_prediction(input_data, model_filename):
    # Load the saved SVM model and scaler
    classifier = joblib.load(model_filename)
    scaler = joblib.load(model_filename.replace('.joblib', '_scaler.joblib'))

    # Scale the input data
    input_data_scaled = scaler.transform(input_data)

    # Predict the probability of class 1 (engagement)
    prob = classifier.predict_proba(input_data_scaled)[:, 1]

    return prob[0]

# Example Usage
if __name__ == "__main__":
    # Path to the new CSV file
    new_data_file = 'path_to_your_new_data.csv'

    # Process the new data
    processed_input = process_new_data(new_data_file)

    # Make a prediction using the saved SVM model
    probability_of_engagement = make_prediction(processed_input, 'svm_model_subject_023.joblib')

    print(f"Predicted probability of engagement (class 1): {probability_of_engagement:.4f}")
