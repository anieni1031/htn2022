import argparse
from msilib.schema import File

from pydub import AudioSegment
import pydub.scipy_effects
import numpy as np
import scipy
import matplotlib.pyplot as plt

from utils import (
    frequency_spectrum,
    calculate_distance,
    classify_note_attempt_1,
    classify_note_attempt_2,
    classify_note_attempt_3,
)

def main(file, note_file=None, note_starts_file=None, plot_starts=False, plot_fft_indices=[]):
     # If a note file and/or actual start times are supplied read them in
    actual_starts = []
    '''if note_starts_file:
        with open(note_starts_file) as f:
            for line in f:
                actual_starts.append(float(line.strip()))'''

    actual_notes = []
    if note_file:
        with open(note_file) as f:
            for line in f:
                actual_notes.append(line.strip())

    song = AudioSegment.from_file(file)
    song = song.high_pass_filter(80, order=4)

    starts = predict_note_starts(song, plot_starts, actual_starts)

    predicted_notes = predict_notes(song, starts, actual_notes, plot_fft_indices)

    print("")
    if actual_notes:
        print("Actual Notes")
        print(actual_notes)
    print("Predicted Notes")
    print(predicted_notes)

    if actual_notes:
        lev_distance = calculate_distance(predicted_notes, actual_notes)
        print("Levenshtein distance: {}/{}".format(lev_distance, len(actual_notes)))

def predict_note_starts(song, plot, actual_starts):
    #size of segments to break song into volume calculations
    SEGMENT_MS = 50
    #min volume to be considered a note
    #sus
    VOLUME_THRESHOLD = -45
    #min increase from one segment to the next to be considered a note
    EDGE_THRESHOLD = 5
    #min time diff between notes
    MIN_MS_BETWEEN = 100

    #filter out bg noise
    song = song.high_pass_filter(80, order=4)

    #dBFS is decibals relative to max volume possible
    volume = [segment.dBFS for segment in song[::SEGMENT_MS]]

    #calculates start times
    predicted_starts = []
    for i in range(1, len(volume)):
        if(
            volume [i] > VOLUME_THRESHOLD and
            volume [i] - volume[i-1] > EDGE_THRESHOLD
        ):
            ms = i * SEGMENT_MS
            #ignore any too close together
            if(
                len(predicted_starts) == 0 or
                ms - predicted_starts[-1] >= MIN_MS_BETWEEN 
            ):
                predicted_starts.append(ms)
    
    if len(actual_starts) > 0:
        print("Approximate actual note start times ({})".format(len(actual_starts)))
        print(" ".join(["{:5.2f}".format(s) for s in actual_starts]))
        print("Predicted note start times ({})".format(len(predicted_starts)))
        print(" ".join(["{:5.2f}".format(ms / 1000) for ms in predicted_starts]))

    # plot the graph things
    if plot:
        x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
        plt.plot(x_axis, volume)
        # add colorful lines for predicted note starts and actual note starts
        for s in actual_starts:
            plt.axvline(x=s, color="r", linewidth=0.5, linestyle="-")
        for ms in predicted_starts:
            plt.axvline(x=(ms / 1000), color="g", linewidth=0.5, linestyle=":")
        plt.show()
    return predicted_starts

print(predict_note_starts(AudioSegment.from_file("uploads/twink.m4a"), False, []))

def predict_notes(song, starts, actual_notes, plot_fft_indices):
    predicted_notes = []
    for i, start in enumerate(starts):
        sample_from = start + 50
        sample_to = start + 550
        if i < len(starts) - 1:
            sample_to = min(starts[i + 1], sample_to)
        segment = song[sample_from:sample_to]
        freqs, freq_magnitudes = frequency_spectrum(segment)

        predicted = classify_note_attempt_3(freqs, freq_magnitudes)
        predicted_notes.append(predicted or "U")

        # Print general info
        print("")
        print("Note: {}".format(i))
        if i < len(actual_notes):
            print("Predicted: {} Actual: {}".format(predicted, actual_notes[i]))
        else:
            print("Predicted: {}".format(predicted))
        print("Predicted start: {}".format(start))
        length = sample_to - sample_from
        print("Sampled from {} to {} ({} ms)".format(sample_from, sample_to, length))
        print("Frequency sample period: {}hz".format(freqs[1]))

        # Print peak info
        peak_indicies, props = scipy.signal.find_peaks(freq_magnitudes, height=0.015)
        print("Peaks of more than 1.5 percent of total frequency contribution:")
        for j, peak in enumerate(peak_indicies):
            freq = freqs[peak]
            magnitude = props["peak_heights"][j]
            print("{:.1f}hz with magnitude {:.3f}".format(freq, magnitude))

        if i in plot_fft_indices:
            plt.plot(freqs, freq_magnitudes, "b")
            plt.xlabel("Freq (Hz)")
            plt.ylabel("|X(freq)|")
            plt.show()
    return predicted_notes

print(predict_notes(AudioSegment.from_file("uploads/twink.m4a"), predict_note_starts(AudioSegment.from_file("uploads/twink.m4a"), False, []), [0], [0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--note-file", type=str)
    parser.add_argument("--note-starts-file", type=str)
    parser.add_argument("--plot-starts", action="store_true")
    parser.add_argument(
        "--plot-fft-index",
        type=int,
        nargs="*",
        help="Index of detected note to plot graph of FFT for",
    )
    args = parser.parse_args()
    main(
        args.file,
        note_file=args.note_file,
        note_starts_file=args.note_starts_file,
        plot_starts=args.plot_starts,
        plot_fft_indices=(args.plot_fft_index or []),
    )