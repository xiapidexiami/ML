import os
import sys
import random
import numpy as np

random.seed(100)

noise_dir = '/media/yangxiaoxia/Seagate Expansion Drive/chime3/Chime/data/noise/'
clean_dir = '/media/yangxiaoxia/Seagate Expansion Drive/deepLearning/pit-speech-separation/wavformat_all/wsj0/sd_tr_s/'
mix_dir = '/media/yangxiaoxia/Seagate Expansion Drive/chime3/Chime/data/mix/sd_tr_s/'

if os.path.exists(mix_dir):
    print("---  There is this folder!  ---")
else:
    os.makedirs(mix_dir)

noise_vols_min = 0.0
noise_vols_max = 0.1

def get_wav_len(wav_name):
    wav_name = wav_name.replace(' ', '\ ')
    command = 'sox ' + wav_name + ' -n stat 2>&1 | sed -n \'s#^Length (seconds):[^0-9]*\([0-9.]*\)$#\\1#p\''
    process = os.popen(command)
    wav_len = process.read().strip()
    process.close()
    return float(wav_len)

def get_noise_wav(noise_name, noise_len, clean_len, trim_noise_name):
    noise_vol = noise_vols_min + random.random() * noise_vols_max
    noise_start = random.random() * (noise_len - clean_len)
    noise_name = noise_name.replace(' ', '\ ')
    trim_noise_name = trim_noise_name.replace(' ', '\ ')
    command = 'sox -v %f %s %s trim %f %f' % (noise_vol, noise_name, trim_noise_name, noise_start, clean_len)
    # command = 'sox -v ' + str(noise_vol) + ' ' + wav_name + ' noise_use.wav trim ' + str(noise_start) + ' ' + str(clean_len)
    # print(command)
    os.system(command)

def add_noise_with_vol(clean_name, noise_name, mix_name):
    clean_name = clean_name.replace(' ', '\ ')
    noise_name = noise_name.replace(' ', '\ ')
    mix_name = mix_name.replace(' ', '\ ')
    command = 'sox -m -v 1 %s %s -t wav %s' % (clean_name, noise_name, mix_name)
    # print(command)
    os.system(command)



def main():
    noise_dir_list = os.listdir(noise_dir)
    noise_dir_len = len(noise_dir_list)
    noise_wav_len = np.zeros(shape=(noise_dir_len,))
    for j in range(noise_dir_len):
        noise_scenes_dir = os.path.join(noise_dir, noise_dir_list[j])
        noise_file = os.path.join(noise_scenes_dir, 'noise.wav')
        noise_wav_len[j] = get_wav_len(noise_file)

    # noise_file_list = os.listdir(os.path.join(noise_dir, noise_dir_list[0]))

    clean_dir_list = os.listdir(clean_dir)
    for i in range(6, len(clean_dir_list), 1):
        print("%d folders", i)
        clean_dir_use = os.path.join(clean_dir, clean_dir_list[i])
        clean_file_list = os.listdir(clean_dir_use)
        for j in range(len(clean_file_list)):
            clean_name = os.path.join(clean_dir_use, clean_file_list[j])
            wav_len = get_wav_len(clean_name)

            noise_index = random.randint(0, noise_dir_len-1)
            noise_scenes_dir = os.path.join(noise_dir, noise_dir_list[noise_index])
            noise_file = os.path.join(noise_scenes_dir, 'noise.wav')

            trim_noise_name = 'trim_noise.wav'
            get_noise_wav(noise_file, noise_wav_len[noise_index], wav_len, trim_noise_name)

            mix_name = os.path.join(mix_dir, clean_file_list[j])

            add_noise_with_vol(clean_name, trim_noise_name, mix_name)



if __name__ == '__main__':
    main()


#
# command = 'sox /media/yangxiaoxia/Seagate\ Expansion\ Drive/chime3/Chime/data/audio/16kHz/backgrounds/BGD_150203_010_CAF.CH4.wav -r 8000 -b 16 output.wav'
# os.system(command)
