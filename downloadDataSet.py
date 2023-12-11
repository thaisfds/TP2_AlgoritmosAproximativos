import os

file = open('./tp2_datasets.txt', 'r')

names = []

for line in file.readlines():
    name = line.split()[0]
    names.append(name)

url = 'http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/'

for name in names:
    cmd = 'wget ' + url + name + '.tsp.gz'
    os.system(cmd)

    cmd = 'gzip -d ' + name + '.tsp.gz'
    os.system(cmd)