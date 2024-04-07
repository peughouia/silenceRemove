import wave

WAV_FORMAT_N_CHANNELS = 1 # mono
WAV_FORMAT_SAMPLE_WIDTH = 2 # 16bit
WAV_FORMAT_FRAMERATE = 44100

def get_bytes_sample_from_16bits_sample(sample_16bits):
    unsigned_sample = sample_16bits
    if sample_16bits < 0:
        unsigned_sample = sample_16bits + 65536
    
    bytes_ms = unsigned_sample//256
    bytes_ls = unsigned_sample - bytes_ms * 256
    return bytes_ls, bytes_ms

def get_bytes_samples_from_16bits_samples(sample_16bits):
    bytes = []
    for s in sample_16bits:
        ls, ms = get_bytes_sample_from_16bits_sample(s)
        bytes.append(ls)
        bytes.append(ms)
    return bytes


#---------------------------------------------
def get_16bits_sample_from_bytes(byteLs, byteMs):
    unsigned = byteLs + byteMs*256
    signed = unsigned
    if unsigned > 32767:
        signed = unsigned-65536
    return signed

def get_16bits_samples_from_bytes(bytes):
    samples = []
    for i in range(0, len(bytes)-1, 2):
        sample = get_16bits_sample_from_bytes(bytes[i], bytes[i+1])
        samples.append(sample)
    return samples

def wave_file_read_sample(filename):
    wr = wave.open(filename, mode="rb")
    if wr.getnchannels() != WAV_FORMAT_N_CHANNELS:
        print('ERREUR: utiliser un fichier mono')
        return None
    
    if wr.getsampwidth() != WAV_FORMAT_SAMPLE_WIDTH:
        print('ERREUR: utiliser le format 16bits')
        return None
    
    if wr.getframerate() != WAV_FORMAT_FRAMERATE:
        print('ERREUR: utiliser 44100Hz')
        return None

    nframes = wr.getnframes()
    print("nframes",nframes)
    frames_as_byte = wr.readframes(nframes)

    # TO DO : convertir les samples
    samples_16bits = get_16bits_samples_from_bytes(frames_as_byte)

    wr.close()
    return samples_16bits



# sample format 16bit
def wave_file_write_samples(filename, samples):
    ww = wave.open(filename, mode="wb")

    ww.setnchannels(WAV_FORMAT_N_CHANNELS)
    ww.setsampwidth(WAV_FORMAT_SAMPLE_WIDTH)
    ww.setframerate(WAV_FORMAT_FRAMERATE)

    ww.setnframes(len(samples))
    #donnéés 8bits
    bytes = get_bytes_samples_from_16bits_samples(samples)

    ww.writeframesraw(bytearray(bytes))

    ww.close()