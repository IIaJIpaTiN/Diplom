from threading import Thread, Lock, Event
import librosa
import numpy as np
from listener import Recorder
from model import MySTTnet
import torch
import win32gui, win32con
import os

audios = []
audio_lock = Lock()
rate = 16000

words = ['******', 'закрыть', 'свернуть', 'открыть', 'номер', 'один', 'два', 'три', 'проводник',
         'блокнот', 'настройки', 'диспетчер', 'задач']

class Executor(Thread):

    def __init__(self, matrix):
        Thread.__init__(self)
        self.daemon = True
        self.net = MySTTnet()
        self.net.load_state_dict(torch.load(r'D:\SUSU\Diplom\Code\weights\acc=tensor(0.8875)_loss=tensor(0.5180).pth', map_location=torch.device('cpu')))
        self.matrix = matrix
        self._stop = Event()

    def stop(self):
        self._stop.set()
        self.rec.stop()

    def stopped(self):
        return self._stop.isSet()

    def predict(self, x):

        data = np.zeros(rate)
        if x.shape[0] <= rate:
            data[rate // 2 - x.shape[0] // 2 : rate // 2 - x.shape[0] // 2 + x.shape[0]] = x
        else:
            data = x[(x.shape[0] - rate) // 2 : (x.shape[0] - rate) // 2 + rate]

        X = np.abs(librosa.stft(data, n_fft=321, hop_length=160))
        Xdb = librosa.amplitude_to_db(X)[:160]

        t_tens = torch.FloatTensor(Xdb)
        t_tens = t_tens.unsqueeze(0).float()
        t_tens = t_tens.unsqueeze(0).float()
        preds = self.net.forward(t_tens)

        return int(preds[0].argmax().data)

    def run(self):
        self.rec = Recorder(audios, audio_lock)
        self.rec.start()
        st = 0

        while not self.stopped():
            audio_lock.acquire()
            n = len(audios)
            audio_lock.release()
            if n > 0:
                audio_lock.acquire()
                x = audios[0].copy()
                del audios[0]
                audio_lock.release()

                word = self.predict(x)
                print(words[word])

                if st == 0 and word == 1:
                    win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)
                elif st == 0 and word == 2:
                    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)
                elif st == 0 and word == 3:
                    st = 1
                elif st >= 1 and word >= 4 and word <= 12:
                    command = self.matrix[st - 1][word - 4]
                    if command.isdigit():
                        st = int(command)
                    else:
                        os.system(command)
                        st = 0
                else:
                    st = 0
