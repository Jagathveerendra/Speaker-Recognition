# Speaker-Recognition
Speaker recognition is the process of automatically recognizing who is speaking on the basis of individual information included in speech waves. This technique makes it possible
to use the speaker's voice to verify their identity and control access to mobile, a data set,bank accounts and in many security applications.  
For example, users have to speak a PIN (Personal Identification Number) in order to gain access to the laboratory door, or users have to speak their credit card number over the telephone line to verify their identity.  By checking the voice characteristics of the input utterance, using an automatic speaker recognition system similar to the one that we will describe, the system is able to add an extra level of security.
![image](https://user-images.githubusercontent.com/92499855/137593881-06a6708a-43bf-4cec-bb01-7f21da458ae5.png)

This project contains framing of signal, mel frequency cepstral coefficients and linear prediction coefficients for feature extraction, lbg algorithm for feature matching.

# FRAMING OF SIGNAL
A single audio signal is blocked into frames of N samples and succeeding will start after M samples, means there is overlap of N-M sammples.

# Mel frequency cepstral coefficients
Mel-frequency cepstral coefficients (MFCCs) are coefficients that collectively make up an MFC. They are derived from a type of cepstral representation of the audio clip. The difference between the cepstrum and the mel-frequency cepstrum is that in the MFC, the frequency bands are equally spaced on the mel scale, which approximates the human auditory system's response. we have choosen Mfccs for feature extraction because they shows more significant variation from speaker to speaker since they are derived on logarithmic scale.
# Linear prediction coefficients
LPCs are another popular feature for speaker recognition. To understand LPCs, we must first understand the Autoregressive model of speech. Speech can be modelled as a pth order AR process.These coefficeients give characteristics of input audio signal.
# LBG(Linde-Buzo-Gray)algorithm
Linde-Buzo-Gray (LBG) Algorithm is used for designing of Codebook efficiently which has minimum distortion and error.It is an iterative procedure and the basic idea is to divide the group of training vectors and use it to find the most representative vector from one group. These representative vectors from each group are gathered to form the codebook. Since codebook derived from LBG shows min distortion we have choosen this.


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
accuracy for model is 100 % for both mfccs and lpcs. 


















