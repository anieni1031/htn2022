from collections import Counter, defaultdict
import note_recognition

#returns an array of all of the intervals
from ast import List
import random

#integer value for each note
noteDict={
    "A" : 1,
    "A#" : 2,
    "B" : 3,
    "C" : 4,
    "C#" : 5,
    "D" : 6,
    "D#" : 7,
    "E" : 8,
    "F" : 9,
    "F#": 10,
    "G" : 11,
    "G#" : 12
}

#hsv values for each interval provided in a dictionary
intervalDict = {
    1: [83,60,40],
    2: [280,79,63],
    3: [221,43,49],
    4: [37,79,87],
    5: [50,100,100],
    6: [187,80,61],
    7: [204,54,84], 
    8:[0,100,44],
    9: [0,100,86],
    10: [84,100,80],
    11: [290,65,29],
    12: [32,100,92]
}


#takes in a string array of notes
#returns an array of all the intervals
def allIntervals(arr):
    if(len(arr)<=1):
        return [1]
    i=len(arr)-1
    intervalArray=[]
    while(i>0):
        add = abs(noteDict[arr[i]]-noteDict[arr[i-1]])%8
        intervalArray.append(add)
        i-=1
    return intervalArray

#takes top k number of most frequent elements + returns them in an int array
def topKFrequent(nums, k):
        frq = defaultdict(list)
        for key, cnt in Counter(nums).items():
            if key != 0:
                frq[cnt].append(key)

        res = []
        for times in reversed(range(len(nums) + 1)):
            res.extend(frq[times])
            if len(res) >= k: return res[:k]

        return res[:k]

#returns an array with random-ish hue, saturation, brightness levels
def hsvInRange(hsv, major, spd):
    hsv[0] += random.randint(-1,1)*random.randint(0,20)
    if hsv[0] <0:
        hsv[0] += 360
    elif hsv[0] >360 :
        hsv[0] -=360
    
    if major:
        hsv[1] += random.randint(0,30)
        if hsv[1] >100:
            hsv[1] = 0
    else:
        hsv[1] -= random.randint(0,30)
        if hsv[1] >100:
            hsv[1] = 100
    hsv[2] += random.randint(0, int(spd/2))
    if hsv[2]>100:
        hsv[2] =100

    return hsv

intervals = allIntervals(note_recognition.predict_notes(note_recognition.AudioSegment.from_file("uploads/twink.m4a"), note_recognition.predict_note_starts(note_recognition.AudioSegment.from_file("uploads/twink.m4a"), False, []), [], []))
frequents = topKFrequent(intervals, 5)

# spd

major = false
majorC = 0
for i in range(frequents):
    cur = frequents[i]
    if cur == 2 or cur == 4 or cur == 5 or cur == 6 or cur==7 or cur==9 or cur==11 or cur==12:
        majorC+=1
if(majorC>len(frequents)/2):
    major = True;


colours = []
for i in range(frequents):
    colours.append(hsvInRange(intervalDict[frequents[i]], major))
print(colours)
