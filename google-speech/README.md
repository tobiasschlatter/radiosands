# Voice Recognition with Google Speech API

Google Speech API is a good option for online voice recognition.

## Installing on Raspberry Pi

Follow these two installation instructions [1](https://pythonspot.com/speech-recognition-using-google-speech-api/) and [2](https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/) to compile pyaudio etc. on the raspberry pi. Summary:

#### Prerequisites

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get installl libportaudio-dev
sudo apt-get install python-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install flac
sudo pip3 install SpeechRecognition

git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio
sudo python setup.py install
```


# Testing using python3

```
#Python program to transcribe an Audio file using google speech
import speech_recognition as sr

# use the audio file as the audio source  
AUDIO_FILE = ("./mini.wav") 

r = sr.Recognizer()
 
with sr.AudioFile(AUDIO_FILE) as source:
    #reads the audio file. Here we use record instead of
    #listen
    audio = r.record(source)  
 
try:
    print("The audio file contains: " + r.recognize_google(audio, language="de-DE", key="put API key here")) #set target language + API key
 
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
 
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
```
