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
2) In this function signal is padded with zeros so that the function is evenly divided into frames with N samples each.
3) Now using  for loop and with techniques of python indexing the whole numpy array is blocked into frames.
4) Multiply frames with hamming window.
# Power spectrum of frames
Import rfft,dct from scipy.fft so that calculation of fourier transform is required.
1) Calculate fourier transform for all frames using rfft function and apply modulus function for the output array.
2) calculate power series using the formula power series = (output array after applying modulus) / no of dfts
# creating a filter bank
The energy of signals entraped in this filters respectively gives mfccs.The final step to computing filter banks is applying triangular filters, typically 26 filters, nfilt = 26 on a Mel-scale to the power spectrum to extract frequency bands. The Mel-Scale aims to mimic the non-linear human ear perception of sound, by being more discriminative at lower frequenceis and less discriminative at higher frequencies. The following are the steps required.
1) First of all create two functions for convertion of mel frequency to frequency and viceversa.
2) 
