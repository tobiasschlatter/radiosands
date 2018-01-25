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