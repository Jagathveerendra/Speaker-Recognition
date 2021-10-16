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
LBG algorithm is used to generate codebook for respective speaker's audio signals























