# Speaker-Recognition
Speaker recognition is the process of automatically recognizing who is speaking on the basis of individual information included in speech waves. This technique makes it possible
to use the speaker's voice to verify their identity and control access to services such as voice dialing, banking by telephone, telephone shopping, database access services, 
information services, voice mail, security control for confidential information areas, and remote access to computers.This document describes how to build a simple, yet complete 
and representative automatic speaker recognition system.  Such a speaker recognition system has potential in many security applications.  For example, users have to speak a 
PIN (Personal Identification Number) in order to gain access to the laboratory door, or users have to speak their credit card number over the telephone line to verify their 
identity.  By checking the voice characteristics of the input utterance, using an automatic speaker recognition system similar to the one that we will describe, the system is 
able to add an extra level of security.
This project contains framing of signal, mel cepstral coefficients, linear prediction coefficients, lbg algorithm and finally feature matching
First of all we import wav file from scipy.io so that by using wavfile.read we convert audio signal into a numpy array
# FRAMING OF SIGNAL
A single audio signal is blocked into frames of N samples and succeeding will start after M samples, means there is overlap of N-M sammples.
And following are the steps required
1) A function named framing is defined such that it takes sampling frequency, numpy array of a audio signal, frame size and frame start as inputs.
2) In this function signal is padded with zeros so that the audio signal is evenly divided into frames with N samples each.
3) Now using  for loop and with techniques of python indexing the whole numpy array is blocked into frames.
4) Multiply frames with hamming window.
# Power spectrum of frames
Import rfft,dct from scipy.fft so that calculation of fourier transform is required.
1) Calculate fourier transform for all frames using rfft function and apply modulus function for the output array.
2) calculate power series using the formula power series = (output array after applying modulus) / no of dfts
# Mel frequency cepstral coefficients
The energy of signals entraped in this filters respectively gives mfccs.The final step to computing filter banks is applying triangular filters, typically 26 filters, nfilt = 26 on a Mel-scale to the power spectrum to extract frequency bands. The Mel-Scale aims to mimic the non-linear human ear perception of sound, by being more discriminative at lower frequenceis and less discriminative at higher frequencies. The following are the steps required.
1) First of all create two functions for convertion of mel frequency to frequency and viceversa.
2) Fix a lower limit and upper limit of frequiences (300 and fs/2) convert them into mel scale and divide into 26 evenly spaced parts.(28 mel points were obtained).
3) Convert 28 melpoints into frequency scale.
4) Design the filter bank with nested for loop and if loops.
5) Now do the dot product between power series and transform of filter bank, filter bank energies were obtained.
6) Apply logarithm and discrete cosine transform to the filter bank energies.
7) These are  26 mfccs but only 1 to 13 mfccs were required. Take only 1 to 13 mfccs and leave the others.
All these steps are arranged in mfcc_final function.
# Linear prediction coefficients
LPCs are another popular feature for speaker recognition. To understand LPCs, we must first understand the Autoregressive model of speech. Speech can be modelled as a pth order AR process, where each sample is given by:LPCs are another popular feature for speaker recognition. To understand LPCs, we must first understand the Autoregressive model of speech. Speech can be modelled as a pth order AR process, where each sample is given by:

![image](https://user-images.githubusercontent.com/92499855/137575266-aea81ee9-fec4-4b3b-a81d-0512bd33f700.png)

LPCS are also derived on frames calculated in framing part
auto correlation as a function of shift R(l):

![image](https://user-images.githubusercontent.com/92499855/137575337-8aa9049d-f48d-448d-90ca-f22a0eed5f11.png)

followimg are the steps required:
1) Instead of using np.correlate define a auto correlation function because we are required to calculate R(l) for only l=0 to l=12or13.(reducing compuation complexity)
2) Auto correlation function is implemented with for loop and R(l) formula
3) Create yule wlaker symmetric matrix by using output array obtained in auto correlation function(this is a function generating yule walker symmetric matrix)
4) LPCS are result of dot product between inverse of yule walker symmetric matrix and matrix obtained in auto correlation function.
# LBG(Linde-Buzo-Gray) algorithm
LBG algorithm is used to generate codebook for respective speaker's audio signals.

![image](https://user-images.githubusercontent.com/92499855/137582517-65127a8f-14ce-489c-b97c-46f7d26f3777.png)


Since LBG algorithm contains lot of steps divide each step into a function.
### Code book splitting
1) The function cb_splitting takes current codebook as input.
2) By using a while loop this function splits each vector in the codebook into two new vectors based on the given threshold value.
3) It finally returns a new codebook with size two times of the input codebook.
### Clustering data(mfccs or lpcs)
The function cluster_vectors(data,codebooks,m) takes mfccs/lpcs,current codebook and current value of 'm'.
1) Using nested for loops the distance between  each vector and code words are calculated and stored in a list.
2) Using sort function for each vector nearest code word is determined.
3) This function returns list of tuples and tuple format is ( index of code word, min distance, acoustic vector).
4) This function also returns mean distortion for data and codebook.
5) Outputs of this function is used to calculate centroids for resepective clusters.( totally m clusters will be obtained)

### Finding centroids for clustered data
 The function finding_centroids(clustervec,codebooks,m,z) takes clustered vectors list(output of cluster_vectors function),codebook, current value of m and length of acoustic vectors as inputs.
 1) There are totally 'm' clusters in the cluster_vectors list.
 2) Mean of each and every cluster is calculated (centroids).
 3) Now this centroids together form a new updated code book which is output of this function.

### Calculating mean distortion
The function distortion(data,codebooks,m) takes mfccs or lpcs, current codebook and currrent value of m as inputs.
1) With help of nested for loops the distance between acoustic vector and codewords is calculated and stored in a list.
2) By using sort function minmum distance is derived and added to a distortion(a variable).
3) Repeat same procedure for all acoustic vectors 
4) To obtain mean_distortion the distortion is divided with number of acoustic vectors.

As given in LBG algorithm picture these four functions are arranged using two while loops.
# Training 
In training codebooks for each and every speaker is derived.
OS is imported to obatin names of the audio files
1) By using directories we will get access to training data set.
2) First of all input audio signal is readed using wavfile.read function.
3) Now input signal is blocked into frames using framing function.
4) For this frames mfccs and lpcs are calculated and stored in seperate lists.
5) mfccs and lpcs are passed to lbg algorithm inorder to obtain their codebooks and these codebooks are also appended to two seperate lists.
6) Above stated steps are repeated for each and every speaker in tarning set using a for loop.
# Testing
The unknown audio signals in testing data sets are matched with their speakers in training data sets.
1) By using directories we will get access to testing data set.
2) First of all input audio signal is readed using wavfile.read function.
3) Now input signal is blocked into frames using framing function.
4) For this frames mfccs and lpcs are calculated and appended in seperate lists.
5) Above steps are repeated for all unknown audio signals using for loop.
6) Now distortion between mfccs and codebooks are calculated.
7) Find for which code book minimum distortion is occuring and conclude that codebook speaker and current unknown speaker are same.(speaker identification)
8) Repeat 6,7 steps with lpcs also.


















