# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def split_audio(audio, name, save):
    # Load your audio.
    song = AudioSegment.from_wav(audio)

    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 200,
        # Consider a chunk silent if it quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -40
    )

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):

        print(name + "_{0}.wav.".format(i))
        chunk.export(
            save + '\\' + name + "_{0}.wav.".format(i),
            bitrate = "16k",
            format = "wav"
        )

path = r'E:\Data\archive\audio_dataset\audio_files'
save_path = r'D:\SUSU\Diplom\Dataset\InWork'

audio = os.listdir(path)

for i in range(100):
    split_audio(path + '\\' + audio[i], audio[i].replace('.wav', ''), save_path)