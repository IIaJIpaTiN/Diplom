import pyaudio
import math
import struct
import wave
import time
import os
from threading import Thread, Lock, Event
import numpy as np

Threshold = 12

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 0.2
f_name_directory = r'D:\SUSU\Diplom\Code\test'

class Recorder(Thread):

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self, audios:list, audio_lock:Lock):
        Thread.__init__(self)
        self.daemon = True
        self.audios = audios
        self.audio_lock = audio_lock
        self.p = pyaudio.PyAudio()
        self._stop = Event()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input_device_index=2,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def stop(self):
        self._stop.set()
        print('Listening stop')

    def stopped(self):
        return self._stop.isSet()

    def record(self, rec:list):
        print('Noise detected, recording beginning')
        #rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH
        for_save = []

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            fr = np.frombuffer(data, np.int16)
            rec.extend(list(fr))

            for_save.append(data)
            current = time.time()

        rec = (np.array(rec, dtype=float) / (2 ** 15))[:len(rec) - int(RATE * 0.1)]
        if rec.shape[0] > RATE * 0.25 and rec.shape[0] < RATE:
            self.audio_lock.acquire()
            self.audios.append(rec)
            self.audio_lock.release()

        #self.write(b''.join(for_save))

    def write(self, recording):
        n_files = len(os.listdir('test'))

        filename = os.path.join('test', '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')


    def run(self):
        print('Listening beginning')
        buffer = [[], [], []]
        while not self.stopped():

            # self.work_lock.acquire()
            # if not self.isWork:
            #     continue
            # self.work_lock.release()

            input = self.stream.read(chunk)
            buffer[0] = buffer[1]
            buffer[1] = buffer[2]
            buffer[2] = input
            rms_val = self.rms(input)
            if rms_val > Threshold:
                b = list(np.frombuffer(buffer[0], np.int16))
                b.extend(list(np.frombuffer(buffer[1], np.int16)))
                b.extend(list(np.frombuffer(buffer[2], np.int16)))
                self.record(b)

# a = Recorder([], Lock())
# a.join()
# print("App stop")