import os
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt


#Creates images from the movie chunk
rootdir = '/Users/home1/CS4269/hw4/videos'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        s = str(os.path.join(subdir, file))
        first, second = s.split('.')
        if 'mp4' == second or 'akv' == second:
            newdir = first + "/images/"
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            os.system("ffmpeg -i " + s + " -s 480x360 -pix_fmt yuv420p -f image2 " +newdir+"%05d.bmp")

'''
for subdir, dirs, files in os.walk(rootdir):
    for sbd in dirs:
        if len(sbd) >= 6 and str(sbd)[-6:] == 'images':
            print str(sbd)
            full = str(os.path.join(subdir, sbd))
            nums = []
            vectortimes = []
            for junk1, junk2, files2 in os.walk(full):
                for f2 in files2:
                    temp = str(f2).split('.')
                    nums.append(temp[0])
            sorted(nums, key=int)
            gray = np.zeros((360, 480))
            for i in range(len(nums)):
                if i % 8 == 0:
                    gray += misc.imread(full + '/' + nums[i] + ".bmp", flatten=True)
                if i% 48 == 0 and i > 1:
                    gray = np.multiply(gray, 1.0/6.0)
                    composite = np.zeros((30, 40))
                    for k in range(360):
                        for j in range(480):
                            composite[k/12][j/12]+=gray[k][j]
                    fin = []
                    for k in range(30):
                        for j in range(40):
                            composite[k][j] = composite[k][j] / 144.0
                    for k in range(30):
                        for j in range(40):
                            fin.append(composite[k][j])
                    vectortimes.append((i/24, fin[:]))
            with open(os.path.join(subdir, sbd)+"vector.txt", 'w') as outfile:
                for tup in vectortimes:
                    s = str(tup[0])
                    for elem in tup[1]:
                        s+= " " + str(elem)
                    outfile.write(s)
                    outfile.write('\n')
'''


train = {"Monty-Python-and-the-Holy-Grail-1.txt": "mpathg1",
     "Monty-Python-and-the-Holy-Grail-2.txt": "mpathg2",
     "Monty-Python-and-the-Holy-Grail-3.txt": "mpathg3",
     "Monty-Python-and-the-Holy-Grail-4.txt": "mpathg4",
     "Monty-Python-and-the-Holy-Grail-5.txt": "mpathg5"
     }
invecvals = []
outvecvals = []
veclength = 0
for subdir, dirs, files in os.walk("/Users/home1/CS4269/hw4/videos/montypython"):
    for f3 in files:
        if str(f3) in train:
            labels = {}
            with open(str(os.path.join(subdir, f3)),'r') as openfile:
                for line in openfile:
                    time, lab = map(int,line.split(" "))
                    arr = np.zeros((5, 1))
                    arr[lab] = 1.0
                    labels[time]=arr
            openfile.close()
            with open(str(os.path.join(subdir, train[str(f3)]))
                    +"/imagesvector.txt", 'r') as openfile:
                for line in openfile:
                    bigstrings = line.split(" ")
                    t = int(bigstrings[0])
                    bigstrings = np.array(map(float, bigstrings[1:]))
                    veclength = len(bigstrings)
                    invecvals.append(bigstrings)
                    if t in labels:
                        outvecvals.append(labels[t])
                    else:
                        outvecvals.append(np.zeros((5, 1)))
            openfile.close()

training_inputs = [np.reshape(x, (1200, 1)) for x in invecvals]
training_data = zip(training_inputs, outvecvals)
