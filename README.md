# Speaker-Recognition
Speaker recognition is the process of automatically recognizing who is speaking on the basis of individual information included in speech waves. This technique makes it possible
to use the speaker's voice to verify their identity and control access to services such as voice dialing, banking by telephone, telephone shopping, database access services, 
information services, voice mail, security control for confidential information areas, and remote access to computers.This document describes how to build a simple, yet complete 
and representative automatic speaker recognition system.  Such a speaker recognition system has potential in many security applications.  For example, users have to speak a 
PIN (Personal Identification Number) in order to gain access to the laboratory door, or users have to speak their credit card number over the telephone line to verify their 
identity.  By checking the voice characteristics of the input utterance, using an automatic speaker recognition system similar to the one that we will describe, the system is 
able to add an extra level of security.
![image](https://user-images.githubusercontent.com/92499855/137593881-06a6708a-43bf-4cec-bb01-7f21da458ae5.png)

This project contains framing of signal, mel cepstral coefficients, linear prediction coefficients, lbg algorithm for feature matching

# FRAMING OF SIGNAL
A single audio signal is blocked into frames of N samples and succeeding will start after M samples, means there is overlap of N-M sammples.

<img width="792" alt="d7Rdx" src="https://user-images.githubusercontent.com/92499855/137594110-5141da60-3600-4c4f-bce7-59c33a17b1e1.png">

# Mel frequency cepstral coefficients
Mel-frequency cepstral coefficients (MFCCs) are coefficients that collectively make up an MFC. They are derived from a type of cepstral representation of the audio clip (a nonlinear "spectrum-of-a-spectrum"). The difference between the cepstrum and the mel-frequency cepstrum is that in the MFC, the frequency bands are equally spaced on the mel scale, which approximates the human auditory system's response. 
# Linear prediction coefficients
LPCs are another popular feature for speaker recognition. To understand LPCs, we must first understand the Autoregressive model of speech. Speech can be modelled as a pth order AR process.These coefficeients give characteristics of input audio signal.
# LBG(Linde-Buzo-Gray)algorithm
Linde-Buzo-Gray (LBG) Algorithm is used for designing of Codebook efficiently which has minimum distortion and error.It is an iterative procedure and the basic idea is to divide the group of training vectors and use it to find the most representative vector from one group. These representative vectors from each group are gathered to form the codebook.

![LBG-algorithm-1-Plan-a-1-vector-codebook-This-is-the-centroid-of-the-whole-arrangement](https://user-images.githubusercontent.com/92499855/137594525-9cda13f8-ae9d-4e91-8d77-0203b8657693.png)

# Training 
In training codebooks for known speakers were derived. These are the steps followed

1) By using directories we will get access to training data set.
2) First of all convert input audio signal into numpy array.
3) Now input signal is blocked into frames.
4) For this frames mfccs and lpcs are calculated and stored in seperate lists.
5) mfccs and lpcs are passed to lbg algorithm inorder to obtain their codebooks.
# Testing
After the whole training process is completed we now test our model on unseen data.We will feed the model with testing data sets and find out which speakers from training data sets are matching with testing data sets respectively. These are the steps followed
1) By using directories we will get access to testing data set.
2) First of all convert input audio signal into numpy array.
3) Now input signal is blocked into frames.
4) For this frames mfccs and lpcs were calculated.
5) Above steps are repeated for all unknown audio signals.
6) Now distortion between mfccs and codebooks were calculated.
7) Find for which code book minimum distortion is occuring and conclude that codebook speaker and current unknown speaker are same.(speaker identification)
8) Repeat 6,7 steps with lpcs also.
# Results
### with mfccs (on a small data set)
CantinaBand3.wav is an imposter and min distortion obtained is  35.682684442694686.  
preamble.wav is an imposter and min distortion obtained is  51.289708061181415.  
s1.wav is matching with s1.wav.  
s2.wav is matching with s2.wav.  
s3.wav is matching with s3.wav.  
s4.wav is matching with s4.wav.  
s5.wav is matching with s5.wav.  
s6.wav is matching with s6.wav.  
s7.wav is matching with s7.wav.  
s8.wav is matching with s8.wav.  
hlo.wav is an imposter and min distortion obtained is  39.99087208226558.  
accuracy is 100%.
### with lpcs (on a small data set)
CantinaBand3.wav is matching with s6.wavdistortion is 0.5286803207154015.  
preamble.wav is matching with s6.wavdistortion is 0.5364160083938064.  
s1.wav is matching with s1.wavdistortion is 0.6027632594509406.  
s2.wav is matching with s2.wavdistortion is 0.6032151789313441.  
s3.wav is matching with s3.wavdistortion is 0.40566458090020546.  
s4.wav is matching with s4.wavdistortion is 0.4295005610203914.  
s5.wav is matching with s5.wavdistortion is 0.4759311723269076.  
s6.wav is matching with s6.wavdistortion is 0.3966163272334043.  
s7.wav is matching with s7.wavdistortion is 0.49357017233170875.  
s8.wav is matching with s8.wavdistortion is 0.4767425609636654.  
hlo.wav is matching with s2.wavdistortion is 0.6624632281338751.  
accuracy is 73%.

















