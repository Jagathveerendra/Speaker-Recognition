# -*- coding: utf-8 -*-
"""iv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16VKGnKsKSLIzhPb2LHCrmERc7BjNCEFG
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft,dct
import math
import os

def framing(sig,fs,frame_size,frame_start):
  # sig is readed data of a signal, fs is sampling frequency,frame_size is duration of a frame
  # frame start indicates after what duration another frame starts.
 # compute frame length and frame step (convert from seconds to samples)
  frame_length = frame_size * fs
  frame_step = frame_start * fs
  signal_length = len(sig)
  frames_overlap = frame_length - frame_step

  num_frames = np.abs(signal_length - frames_overlap) // np.abs(frame_step)
  rest_samples = np.abs(signal_length - frames_overlap) % np.abs(frame_step)

# Pad Signal to make sure that all frames have equal number of samples
# without truncating any samples from the original signal
  if rest_samples != 0:
      pad_signal_length = int(frame_step - rest_samples)
      z = np.zeros((pad_signal_length))
      pad_signal = np.append(sig, z)
      num_frames += 1
  else:
      pad_signal = sig

     # make sure to use integers as indices
  frame_length = int(frame_length)
  frame_step = int(frame_step)
  num_frames = int(num_frames)
  frames=np.zeros((num_frames,frame_length))
  k=0
  for i in range(num_frames):
    frames[i]=pad_signal[k:k+frame_length]
    k+=frame_step
  return frames


def power(frames,nfft,frame_size,fs):
  
  frame_length = int(frame_size*fs)
  frames=frames * np.hamming(frame_length)
  ftrans=rfft(frames,nfft)
  fmod=np.absolute(ftrans)
  pwer=(fmod**2)/512
  return pwer


def freqtomel(f):
   mel=1125*math.log(1+f/700)
   return mel
def meltofreq(mel):
  freq=700*(math.exp(m/1125)-1)
  return freq
# nfilt is number of filters   usually 26 is choosen
# nfft is number of fast fourier transform points usually 512 is choosen
def melfreqpoints(fs,nfilt,nfft):
  f_up=fs/2
  f_low=300
  m_up=freqtomel(f_up)
  m_low=freqtomel(f_low)
  nfilt=26
  mel_points=np.linspace(m_low,m_up,nfilt+2)
  mel_freq_points=700*np.exp(mel_points/1125)-700
  fp=np.floor((nfft)*mel_freq_points/fs)
  return fp

def filterbank(fp,nfilt,nfft):
  # fp is filter frequency bin points
  h=np.empty((nfilt,int(nfft/2 + 1)))#h is filter bank
  for i in range(nfilt):
    for k in range(int(nfft/2 + 1)):
     
       if k < fp[i]:
           h[i][k]=0
       elif fp[i]<=k and k<=fp[i+1]:
           h[i][k]=(k-fp[i])/(fp[i+1]-fp[i])
       elif fp[i+1]<k and k<=fp[i+2]:
           h[i][k]=(fp[i+2]-k)/(fp[i+2]-fp[i+1])
       elif k>fp[i+2] and k<=256:
           h[i][k]=0
  return h


def mfccs(pwer,h):

  f_energy=np.dot(pwer,h.T)# multiplying 
  log_f_energy=np.log(f_energy)
  mfcc=(dct(log_f_energy))[:,1:13]
  return mfcc
def mfcc_final(sig,fs):
  
  frame_size=0.025
  frame_start=0.01
  nfft = 512
  nfilt = 26
  frames = framing(sig,fs,frame_size,frame_start)
  pwerframes = power(frames,nfft,frame_size,fs)
  #print(pwerframes)
  fp = melfreqpoints(fs,nfilt,nfft)
  #print(fp)
  filter_bank = filterbank(fp,nfilt,nfft)
  #print(filter_bank[0])
  mfcc = mfccs(pwerframes,filter_bank)
  return mfcc

######### lbg algoritm dist = np.linalg.norm(point1 - point2)
e = 0.01

def cb_splitting(codebook,ugm,e,z):# ugm = upgraded m and z is length of acoustic vectors
   i,j = 0,0
   new_codebook = np.empty((ugm,z))
   while (i < ugm):
     temp = codebook[j]
     new_codebook[i] =  temp *(1+e)
     new_codebook[i+1] = temp*(1-e)
     j+=1
     i+=2
   return new_codebook  
def cluster_vectors(data,codebooks,m):
  # data is mfccs or lpcs 
  clustervec = []
  distortion = 0
  for i in range(len(data)):
     distance = []
     for j in range(m):
        dist = np.linalg.norm(data[i] - codebooks[j])
        distance.append((j,dist,data[i]))
     distance.sort(key=lambda tup:tup[1])
     distortion += distance[0][1]
     clustervec.append(distance[0])
  mean_distr = distortion/len(clustervec)
  return clustervec,mean_distr
def finding_centroids(clustervec,codebooks,m,z):
    centroids = np.zeros((m,z))
    count = np.zeros(m)
    for clusthelp in clustervec:
        for j in range(m):
          if clusthelp[0] == j:
            centroids[j] += clusthelp[2]
            count[j] +=1
          else:
            0
    for j in range(m):
      if count[j]!=0:
         centroids[j] = centroids[j]/count[j]
    return centroids
def distortion(data,codebooks,m):
  distortion = 0
  for i in range(len(data)):
     distance = []
     for j in range(m):
        dist = np.linalg.norm(data[i] - codebooks[j])
        distance.append((j,dist))
     distance.sort(key=lambda tup:tup[1])
     distortion += distance[0][1]
  mean_distr = distortion/len(data)
  return mean_distr


def codebook(mfcc,M,z):
  code_book = np.zeros((1,z))
  code_book[0]= np.mean(mfcc,axis=0)
  m = 1
  e = 0.01
  thrshld = 0.01
  while (m<M):
    m = 2*m
    code_book = cb_splitting(code_book,m,e,z)
    stop = 1
    while (stop):
      cluster_vec,d = cluster_vectors(mfcc,code_book,m)
      code_book = finding_centroids(cluster_vec,code_book,m,z)
      d1 = distortion(mfcc,code_book,m)#distr_list.append(distortion(mfcc,code_book,m))
      #cond = (distr_list[-2] - distr_list[-1])/distr_list[-1]
      cond = (d-d1)/d1
      if cond < thrshld :
        stop = 0
  return code_book

#*******************end of lbg**************8
# print(code_book)
# print(distr_list)
# #print(cond)

# from google.colab import drive
# drive.mount('/content/drive')

directory='/content/drive/MyDrive/dataset/data/train'# change this directory if you want to run on your device
M = 8
z = 12
distr_limit = 30
train_speakers = os.listdir(directory)
codebooklist = []
for i in train_speakers:
  fs,sig = wavfile.read(directory+'/'+i)
  mfcc = mfcc_final(sig,fs)
  codebooklist.append(codebook(mfcc,M,z))
# print(codebooklist[1])
# print(train_speakers)
test_directory = '/content/drive/MyDrive/dataset/data/test'
test_speakers = os.listdir(test_directory)
speaker_features = []
# print(test_speakers)
for i in test_speakers:
  fs,sig = wavfile.read(test_directory+'/'+i)
  mfcc = mfcc_final(sig,fs)
  speaker_features.append(mfcc)
for i in range(len(test_speakers)):
  distortion_list = []
  for j in range(len(train_speakers)):
    distortion_list.append((j,distortion(speaker_features[i],codebooklist[j],M)))
  distortion_list.sort(key=lambda tup:tup[1])
  if distortion_list[0][1]<distr_limit:
      print( test_speakers[i] + " is matching with " +train_speakers[distortion_list[0][0]])
  else:
      print( test_speakers[i] + " is an imposter and min distortion obtained is  " +str(distortion_list[0][1]))

###linear prediction coefficients

def autocorrelation(frame,p):
  corr = np.zeros(p+1)
  n = len(frame)
  pad_frame = np.pad(frame,(0,p))
  for i in range(p+1):
    shift_frame = np.zeros(n+p)
    shift_frame[i:n+i] = frame
    corr[i] = sum(pad_frame*shift_frame)
  return corr
def yulewalker_matrix(x,p):# x is correlation output for 1 frame
  R = np.empty((p,p)) 
  for i in range(p): 
    for j in range(p): 
      R[i,j] = x[np.abs(j-i)]   

  return R
def lpc(frames,p):
  lpcs = np.zeros((len(frames),p))
  n = len(frames[0])
  for i in range(len(frames)):
    corr_for_1frame = autocorrelation(frames[i],p)
    R = yulewalker_matrix(corr_for_1frame,p)
    r = -corr_for_1frame[1:]
    lpcs[i] = np.dot(np.linalg.inv(R),r.T)
    lpcs[i] = lpcs[i] / np.max(np.abs(lpcs[i]))
  lpcs = lpcs#/np.max(lpcs)
  return lpcs
# fs,sig = wavfile.read('s1.wav')
# frames = framing(sig,fs,0.025,0.01)
# lpcs = lpc(frames,13)
# print(lpcs)
#print(frames)
# frame = np.arange(1,10,1)
# print(frame)
# print(autocorrelation(frame,5))

directory='/content/drive/MyDrive/dataset/data/train'
M = 8
distr_limit = 0.7
train_speakers = os.listdir(directory)
codebooklist = []
for i in train_speakers:
  fs,sig = wavfile.read(directory+'/'+i)
  frames = framing(sig,fs,0.025,0.01)
  lpcs = lpc(frames,13)
  codebooklist.append(codebook(lpcs,M,13))

test_directory = '/content/drive/MyDrive/dataset/data/test'
test_speakers = os.listdir(test_directory)
speaker_features = []
#print(test_speakers)
for i in test_speakers:
  fs,sig = wavfile.read(test_directory+'/'+i)
  frames = framing(sig,fs,0.025,0.01)
  lpcs = lpc(frames,13)
  speaker_features.append(lpcs)
for i in range(len(test_speakers)):
  distortion_list = []
  for j in range(len(train_speakers)):
    distortion_list.append((j,distortion(speaker_features[i],codebooklist[j],M)))
  distortion_list.sort(key=lambda tup:tup[1])
  if distortion_list[0][1]<distr_limit:
      print( test_speakers[i] + " is matching with " +train_speakers[distortion_list[0][0]] + "distortion is "+str(distortion_list[0][1]))
  else:
      print( test_speakers[i] + " is an imposter and min distortion obtained is  " +str(distortion_list[0][1]))