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
    "G" : 10,
    "G#" : 11,
}

#hsv values for each interval provided in a dictionary
intervalDict = {
    0: [0,50,10],
    1: [0,50,10],
    2: [0,50,10],
    3: [0,50,10],
    4: [0,50,10],
    5: [0,50,10],
    6: [0,50,10], 
    7:[0,50,10],
    8: [0,50,10],
    9: [0,50,10],
    10: [0,50,10],
    11: [0,50,10],
    12: [0,50,10],
}

#takes in a string array of notes
#returns an array of all the intervals
def allIntervals(arr):
    if(arr.length<=1):
        return [1]
    i=len(arr)-1
    intervalArray=[]
    while(i>0):
        intervalArray.append(abs(noteDict[arr[i]]-noteDict[arr[i-1]]))
        i-=1
    return intervalArray

#takes top k number of most frequent elements + returns them in an int array
def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for i in range(len(nums) + 1)]

        for n in nums:
            count[n] = 1 + count.get(n, 0)
        for n, c in count.items():
            freq[c].append(n)

        res = []
        i = len(freq) - 1
        while k > 0:
            if freq[i] != [] and k-len(freq[i]) >= 0:
                res.extend(freq[i])
                k -= len(freq[i])
            i -= 1
        return res

#returns an array with random-ish hue, saturation, brightness levels
def hsvInRange(hsv:List[int], major:bool, spd:int):
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