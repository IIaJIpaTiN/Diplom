import os, shutil
import numpy as np
from matplotlib import pyplot as plt
import librosa
from librosa import display


def get_len(dir_path, save_dir, class_cnt, rate):
    labels = ['открыть', 'номер', 'один', 'два', 'три', 'закрыть', 'мой', 'компьютер',
              'проводник', 'блокнот', 'настройки', 'диспетчер', 'задач', '*****', 'свернуть']
    for i in range(class_cnt):
        cur_dir = dir_path + '{:02}'.format(i) + '//'
        files = os.listdir(cur_dir)
        times = []
        for audio in files:
            x , sr = librosa.load(cur_dir + audio, sr=rate)
            t = x.shape[0] / sr
            times.append(t)
        fig, ax = plt.subplots()
        ax.hist(times)
        ax.set_title(labels[i])
        plt.show()

        print('Write limit')
        min_len = float(input())
        max_len = float(input())
        cnt = 0
        for audio in files:
            x , sr = librosa.load(cur_dir + audio, sr=rate)
            t = x.shape[0] / sr
            if t >= min_len and t <= max_len:
                shutil.copy(cur_dir + audio, save_dir + '\\' + '{:02}'.format(i) + '\\' + audio)
                cnt += 1
        print(cnt, '\n')

def create_plot(path):
    test_data = [0 for i in range(2000)]
    train_data = [0 for i in range(2000)]
    x = [i for i in range(1900)]
    with open(path,'r') as file:
        data = file.readlines()
        for i in range(len(data)):
            test_data[i], train_data[i] = data[i].split()
            test_data[i] = float(test_data[i])
            train_data[i] = float(train_data[i])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title("Функция потерь", fontsize=16)
    ax.set_xlabel("Эпоха", fontsize=14)
    ax.plot(train_data[:1500], label='Обучающая выборка')
    ax.plot(test_data[:1500], label='Тестовая выборка')
    ax.legend(fontsize=12)
    plt.show()


main_dor = r'D:\SUSU\Diplom\Dataset\Main2\\'
save_dir = r'D:\SUSU\Diplom\Dataset\Main3\\'
#get_len(main_dor, save_dir, 15, 16000)
acc_path = r'D:\SUSU\Diplom\Code\accuracy_history.txt'
loss_path = r'D:\SUSU\Diplom\Code\loss_history.txt'
create_plot(loss_path)