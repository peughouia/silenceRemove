import matplotlib.pyplot as plt
from wave_file_manager import *

SILENCE_THRESHOLD = 50
GLITCH_MAX_LEN = int(441*0.6) #6ms
SILENCE_MIN_LEN = 4410 * 4 # 400MS
MARGIN_START = 4410 * 1 # 100MS
MARGIN_END = 4410 * 1 # 100MS

def normalize_samples(samples, max_value):
    max_sample = max(abs(max(samples)), abs(min(samples)))
    f = max_value / max_sample
    return [s * f for s in samples]

def get_silences_points(samples, threshold, glitch_max_len, silence_min_len, margin_start, margin_end):
    points = []
    in_silence_zone = False
    chunk_count = 0
    chunk_len = 441 # 10ms
    start = 0

    if (MARGIN_START + MARGIN_END) > SILENCE_MIN_LEN:
        print("ERREUR: MARGIN_START + MARGIN_END superieur a SILENCE_MIN_LEN")
        return None

    for i in range(len(samples)):
        s = abs(samples[i])
        if not in_silence_zone:
            if s <= threshold:
                if chunk_count == 0:
                    start = i
                chunk_count += 1
                if chunk_count >= chunk_len:
                    in_silence_zone = True
            else:
                chunk_count = 0
        else:
            if s > threshold:
                chunk_count = 0
                in_silence_zone = False
                if len(points) > 0 and start - points[-1][1] <= glitch_max_len:
                    points[-1] = (points[-1][0], i)
                else:
                    points.append((start, i))
    
    points = [(p[0]+margin_start, p[1]-margin_end) for p in points if p[1]-p[0] >= silence_min_len]

    return points

def get_samples_without_silences_from_point(samples,silences_points):
    out_samples = []

    start = 0
    for p in silences_points:
        if p[0] > start:
            out_samples += samples[start:p[0]]
            start = p[1]
    
    if start < len(samples)-1:
        out_samples += samples[start:]

    return out_samples


def get_samples_without_silences(samples):
    # normaliser les samples
    wav_sample_norm = normalize_samples(samples, 1000)
    silences_points = get_silences_points(wav_sample_norm, SILENCE_THRESHOLD, GLITCH_MAX_LEN, SILENCE_MIN_LEN,MARGIN_START,MARGIN_END)
    out_sample = get_samples_without_silences_from_point(samples, silences_points)
    
    # matplotlib
    """a = [1, 10, 5, 2]
    b = [0, 5, 3, 4]
    plt.plot(b, label="Graphe B")
    plt.plot(a, label="Graphe A")
    plt.axhline(y=4, color = 'r')
    plt.axvline(x=2, color = 'y')
    plt.legend()
    plt.show()"""

    """plt.plot(wav_sample_norm)
    plt.axhline(y= SILENCE_THRESHOLD, color = 'r')
    plt.axhline(y= -SILENCE_THRESHOLD, color = 'r')

    for p in silences_points:
        plt.axvline(x=p[0], color = 'r')
        plt.axvline(x=p[1], color = 'y')

    plt.show()"""

    return out_sample
    