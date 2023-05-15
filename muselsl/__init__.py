from .stream import stream, list_muses, connect, find_muse
from .record import record, record_direct, start_record, save_ongoing
from .view import view
from .muse import Muse
from .constants import MUSE_SCAN_TIMEOUT, AUTO_DISCONNECT_DELAY,  \
    MUSE_NB_EEG_CHANNELS, MUSE_SAMPLING_EEG_RATE, LSL_EEG_CHUNK,  \
    MUSE_NB_PPG_CHANNELS, MUSE_SAMPLING_PPG_RATE, LSL_PPG_CHUNK, \
    MUSE_NB_ACC_CHANNELS, MUSE_SAMPLING_ACC_RATE, LSL_ACC_CHUNK, \
    MUSE_NB_GYRO_CHANNELS, MUSE_SAMPLING_GYRO_RATE, LSL_GYRO_CHUNK
__version__ = "1.0.0"
