# Bart KL: Neural Network for Deep Music Generation

# 1. Introduction
The project consists of generating music using an AI system. For this purpose we had to make several choices, not only about the type of AI we would use, but also which representation we will use to represent 'music'.

## 1.1. Choosing a data representation
Representing music can be done in different ways. For example, we have MIDI1 (Musical Instrument Digital Interface). MIDI is a kind of electronic 'notation'. It therefore does not contain the entire sound spectrum, but only instructions for (electronically imitated) instruments.

However, this representation is not flexible, and so there was a need for a representation of music that offered much more freedom. Furthermore, we also found it difficult to judge whether the result
of a MIDI file is 'good' or not, which is highly subjective, whereas with an effective audio file we can simply judge whether it resembles music or not.

This is how we ended up with WAV (Waveform Audio file Format). WAV files represent sound by a series of amplitudes, possibly for several channels at once (mono/stereo). This representation offers much more freedom. One drawback, however, is that this representation is not compressed, and thus contains huge amounts of data. This problem is discussed further in section 2.

Due to the difficult nature of this topic, there are generally few working implementations to be found. However, there are some networks that obtain quite good results, such as OpenAI Jukebox.

## 1.2. Choosing the type of AI system
Choosing which type of AI system we will use is part of our research. We will create, train and test different types of AI systems.

## 1.3. Choice of genres for training data
We almost immediately decided to train the network on electronic music, because these naturally contain quite a lot of noise and distortion. Our expectations were that this would be easier to get acceptable results, because very dirty, ugly signals would be closer than real instruments Mimicking an acoustic guitar or a violin is much harder, and the AI should put less effort into creating a synthesiser. 

Electronic music is a very wide spectrum, however, so the next choice was specific genres and styles to train on. For this, we decided to go for house and techno, because these are generally very minimalist and repetitive. A very complex song seemed difficult, while a small track where little happens that repeats continuously would probably produce a result sooner. If a song is very simple, the AI can more easily create something similar. Furthermore, we should not worry about things like notes, chords, keys (not all notes may always be used together), and so on.

# 2. The data problem
We start this section with an example. If we have a WAV file that contains a audio fragment of 10s at a sample rate of 44,100 samples per second per channel, in stereo, then the data is an array of 880,000 floats. So it is clearly computationally very intensive.

## 2.1. Solutions to the data problem

### 2.1.1. Downsampling
An obvious, solution to the data problem is downsampling. Downsampling is lowering the sample rate of an audio file, causing information (and thus quality) to be lost. So we store the same WAV file, but with fewer samples per second.

This is not an optimal solution, and will certainly not by itself solve the data problem. Even if we take 1/5th of the original sample rate, there is still a relatively large amount of data. But then the quality is no longer acceptable. So we are looking for an optimal sample rate with 'listenable' quality - this is subjective - and is 'processable' in terms of data size. 

We opted for 10 kHz, or 10,000 samples per second.

### 2.1.2. From stereo to mono
As mentioned, stereo sound has two channels, and thus contains twice as much data. An easy and obvious solution is thus to merge the two channels into a single channel, thus making the audio mono. The output will then probably also be mono, but we don't really think this is a problem. If stereo output is desired, the mono track can simply be duplicated, and then the output will be stereo. By using mono audio, we halve our data.

### 2.1.3. Choosing specific fragments from the files
By cutting short fragments of a few seconds from the WAV files, we reduce the amount of data there is. However, this has a second advantage: by selecting a specific piece selected from a song, the network will (hopefully) be able to train more easily since there is less variation in the data. If a song contains an intro, choruses, etc.Then it will become much harder for the network to see a connection between the training data, whereas two choruses are likely to have a similar structure. In this way, the network should also not try to generate an entire song, but only a small fragment. Further techniques for reducing the size of the data are covered in section 3 because they are specifically devised for the networks we used.

# 3 Experiments
## 3.1. Simple Auto Encoder
Our first network was a very simple Auto Encoder that we gradually extended with more layers. Due to the simple nature of this network, our expectations for the results were not so high because very complex networks are needed to process this data.

## 3.2. Generation of spectrograms
Much of the information that can be found online about generative AI models is about generating images. This data is 2-dimensional, unlike our musical data, which is 1-dimensional. So examples and reading material are scarce on this topic. The structure of generative networks for images is often not useful on our musical data.

<img src="posts/2021/bartkl_spectrogram.png" alt="bartkl_spectrogram" style="width:50%;"/>

_An example of a spectogram_

So we were looking for a way to still be able to somewhat use these generative networks for 2-dimensional networks with some modifications. Spectrograms are graphs (generated by e.g. Fast Fourier Transforms) in which the sound frequency is plotted against time. In this way our data became 2-dimensional. We got the idea of working with spectrograms by studying WaveGAN and SpecGan, which implement a similar method. It does not aim to effectively generate images, though. 

Although the subject does seem very interesting, it is almost impossible to convert the image back to an audiofragment. This is because the resolution of the spectrogram would again have to be immensely high (so then again we would have too much data to be processable). As an example, enough vertical resolution would be needed to see the gradations between, say, 12,000Hz and 12,001Hz.

Furthermore, these images are built up backwards from 2-dimensional data, so generating of images would be equivalent to:

1D → 2D → 2D (image) ⇒ Network ⇒ 2D (image) → 2D → 1D

So we transform 2-dimensional data into other 2-dimensional data, with loss of information. This makes no sense, so we might as well use the data from which the images are constructed are constructed from.

When generating the spectrogram data, the phasing information of the audio file is lost. Normally, this would be bad for the result, as the quality drops even more, but thanks to the earlier downsampling (section 2.1.1), the quality is already so low that the difference is
is not audible. So this is nice for us, as we again have a little less
data to process without any real disadvantage.

So now we had 2-dimensional data, and could use the same techniques as are used for images.

### 3.2.1. Spectrograms via GANs
For the network that would generate the spectrograms we chose a GAN, because Generative Adversarial Networks are generally the most powerful generative models, that can achieve the best results if you can train them properly.

However, training GANs is a notoriously difficult problem and it is very common that even the most carefully drafted GAN learns absolutely nothing useful

### 3.2.2 Spectrograms via UAEs
As mentioned at the end of the previous subsection, GANs are quite difficult to train, and it is difficult to get good results from them. Therefore, we also ̈experimented with VAEs, to investigate whether these results would be better. VAEs do not yield as good results as GANs, but because they are easier to train, they are definitely worth trying.

## 3.3 Bpm
A subsequent experiment sought to make use of the 'structure' of the songs on which the model was trained on. This is how we tried working with the bpm, which stands for beats per minute.

We now split the song into small pieces based on the bpm. For example, we have an audio clip of 100s with a bpm of 120. So 1 beat lasts 60s/min 120bpm = 0.5s. If we have a samplerate of 44,100 our audio clip is divided into 200 samples( 100 seconds / 0.5 seconds per sample ) each 0.5s long. 

We thought that this would help the network more easily recognise a rhythm, beat or structure.

A disadvantage of this is that the preprocessing time increases, and the shape of each split audiofragment is different. Indeed, the bpm is not the same for each song, which makes the implementation of a neural network more difficult (because the training data does not always have the same shape).

We implemented this for an AE, but instead of training the network on different files with different bpm's, we trained the network on 1 file (with thus the bpm remaining the same). This way, we avoided the difficulty of making an implementation that works for different
files with different bpm's. We then compared training with the original file vs. training with the data split based on the bpm.

# 4 Results.
### Simple Auto Encoder
The Auto Encoder mainly produces noise with huge amounts of distortion. There is however, a certain rhythm audible in the background. Although this rhythm is quite quiet, it is present. This result gave us good courage for subsequent experiments with more complex networks.

### Spectrograms via GANs
We have tried for a very long time to set up a good structure for the network, but we ultimately failed to get good results from it. 

This network did however produce more and better results than our other attempts: it doesn't just get noise out, but again there is rhythm in it. This is the case with the Auto Encoder too, but in a different way: the Auto Encoder had a rhythm _behind_ the noise, while the GAN has a rhythm _in_ the noise.

This results in a sound that looks a bit like the sound of a helicopter. However, we cannot not say for sure if this is due to the network or if it is a coincidence. Furthermore, the noise is much quieter and softer, unlike the Auto Encoder whose results contain a lot of distortion. 

The results from the GAN contained virtually no distortion. However, the result was still just noise, and hence not music.

### Spectrograms via VAEs
Music did come out of the VAE, but the result is simply all training data on top of each other with noise over it. So this network generated nothing new, but simply returned what we trained it on. So here again, no real results to report.

### Bpm splitting via AEs
As expected, this gave better results than the ordinary AE. The
difference, however, was very minimal: as with the ordinary AE, we got noise with a lot of distortion and a rhythm in the background. 

The improvement is that the rhythm is now more clearly audible. This
minimal improvement, together with the drawbacks of the preprocessing time and the difficulty of the implementation, made us abandon bpm-based splitting.

# 5 Conclusion
WAV files are hugely interesting research subjects, but at the same time also very difficult to deal with. Not only do they contain a huge amount of data, and are therefore heavy to give to an AI model.

This data is also one-dimensional so very little useful information can be found. We have come up with some clever techniques to more easily deal with these problems, but there is no real solution.

We ourselves have not succeeded in generating music through our neural networks, but this does certainly not to say that it is impossible. There are a number of successful implementations such as WaveGAN and OpenAI Jukebox, for example. This is just a hugely difficult subject that requires a lot of experience and expertise, which we do not currently have.

The results we have achieved disappoint us a little bit. When we started researching this topic, we did know that it was a very difficult choice, but we would still would have liked a real sample generated. However, for us the results stayed at (rhythmic) noise.
