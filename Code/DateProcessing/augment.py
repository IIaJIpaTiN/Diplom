import random
import subprocess
import os, shutil








def augment(in_path, out_path, dir_cnt, num):

    for i in range(dir_cnt):
        cur_in_dir = in_path + '\\' '{:02}'.format(i)
        cur_out_dir = out_path + '\\' '{:02}'.format(i)
        audios = os.listdir(cur_in_dir)
        for audio in audios:
            cur_audio_path = cur_in_dir + '\\' + audio
            shutil.copy(cur_audio_path, cur_out_dir + '\\' + audio)
            for j in range(num):
                out_audio_path = cur_out_dir + '\\' + str(j) + audio
                augment_logic(cur_audio_path, out_audio_path)


def augment_logic(in_str, out_str):

    if random.randint(0, 1) == 0:
        stretch_rate = (random.random() / 4.5) + 1.11
    else:
        stretch_rate = random.randint(750, 900) / 1000
    if random.randint(0, 1) == 0:
        pitch_rate = random.randint(200, 500)
    else:
        pitch_rate = random.randint(-500, -200)

    subprocess.call(["sox", in_str, out_str, "tempo", "-s", '{0:.2f}'.format(stretch_rate), "pitch", str(pitch_rate)])

def create_dir(save_data_path):
    for i in range(13):
        if not os.path.isdir(save_data_path + '\\' + str(i)):
            os.mkdir(save_data_path + '\\' + '{:02}'.format(i))

in_dir = r'D:\SUSU\Diplom\Dataset\NewMain'
out_dir = r'D:\SUSU\Diplom\Dataset\NewMain2'

create_dir(out_dir)
augment(in_dir, out_dir, 13, 3)

out_str = r'D:\SUSU\Diplom\Code\1_6c71f8225687_01.wav'
#subprocess.call(["sox", path, out_str, "pitch", '500'])
#print(os.path.pardir)

