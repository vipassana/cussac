# -*- coding: utf-8 -*-
"""
need to create a 16 x 1 million (or so, or however users I have) matrix, 
where each user is represented with a length 16 numpy array of 1s and 0s, standing 
for whether they follow each of the social landmarks. Also add a 1 million long numpy 
array of Trues and Falses, standing for whether they are a 'new yorker' by our 
estimation, and finally another million-long numpy array of the UserIDs. Obviously, 
these all need to be ordered the same way.
"""
import os
import sys
import pandas as pd
import numpy as np
import glob
# from binarysearch import binary_search

def binary_search(L, v):
    lengthOfL = len(L)
    imin = 0
    imax = lengthOfL # imax always points to end of array (non inclusive).
    while imin < imax:
        # Computes midpoint for roughly equal partition.
        imid = int((imin + imax) / 2)
        if v == L[imid]:   # v found at index imid.
            return L[imid]
            break
        elif v < L[imid]:  # Changes imax index to search lower subarray.
            imax = imid
        else:              # Changes imin index to search upper subarray.
            imin = imid + 1
    
    if imin < imax:      # Found v
        # Handles repetitions: makes imid point to 1st greater than v.
        while imid < lengthOfL and v == L[imid]:
            imid += 1
        # Return userid
        # return L[imid]
        return True
    else:
        # if userid isn't in list, return -1
        # return -1
        return False

#Getting just the UserID column from my csv file that aggregates every csv of Search API
#results, generated by my readalltweets.py script. This might not be the way to go--
#might be better to take the code from that script and put it directly in here. 
allUserIDs = pd.read_csv('concat.csv', usecols = ['UserID'], error_bad_lines = False, 
    warn_bad_lines = True)

#Going through the file for each social landmark that contains just the UserIDs for their
#followers, storing that list in a dataframe, which is stored within the list 
# 'sociallandmarkFollowers'
numberOfSocialLandmarks = 0
socialLandmarkFollowers = []
socialLandmarkNames = []
for csvfile in glob.glob('sociallandmarks/*followerids.csv'):
    socialLandmarkHandle = csvfile[16:-15]
    print socialLandmarkHandle
    socialLandmarkNames.append(socialLandmarkHandle)
    df = pd.read_csv(csvfile, usecols=['UserID'])
    #adding the social landmarks to a list of lists. The user ids for each 
    #social landmark is sorted so I can use binary search when creating
    #the matrix
    socialLandmarkFollowers.append([socialLandmarkHandle, sorted(df['UserID'].values)])
    print max(df['UserID'].values)
    #adding the user ids from the social landmark list to my master list of
    #user ids (including the user ids pulled from the twitter Search API)
    allUserIDs = allUserIDs.append(df)
    numberOfSocialLandmarks += 1

# print 'sorting social landmark followers list of lists'
sociallandmarkFollowers = sorted(socialLandmarkFollowers, key=lambda x: x[0])

print 'dropping duplicates from all user ids list'
allUserIDs = allUserIDs.drop_duplicates(['UserID'])

print 'converting all user id dataframe to numpy array'
allUserIDs = allUserIDs['UserID'].values

# #what I'm going through here is each userID we have from the search API, checking to see
# #if that UserID is in any of the sociallandmark follower lists by going through the
# #list of followers of each social landmark. 


numberOfUserIDs = len(allUserIDs)

matrix = np.zeros((numberOfUserIDs, numberOfSocialLandmarks))
sortedUserIDs = sorted(allUserIDs)

countofFoundUserIDs = 0

for i in range(numberOfUserIDs):
# for i in range(77):
    socialLandmarkCount = 0
    for socialLandmark in socialLandmarkFollowers:
        if binary_search(socialLandmark[1], sortedUserIDs[i]):
            # matrix[socialLandmarkCount,i] = 1
            matrix[i, socialLandmarkCount] = 1
            print i, sortedUserIDs[i], socialLandmark[0]
            countofFoundUserIDs += 1
        socialLandmarkCount +=1
    socialLandmarkCount = 0

dfmatrix = pd.DataFrame(data=matrix, index=sortedUserIDs, columns=socialLandmarkNames)

dfmatrix.to_csv('mastermatrix.csv', index_label='UserID')

print countofFoundUserIDs
