import wave # package is installed by default
import SpeechDetector
import pyaudio
import matplotlib
matplotlib.use('TkAgg')
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction as aF
from pyAudioAnalysis import audioTrainTest as aT
from wavio import _wav2array
import numpy
import GenreRecognizer
import OSC


classes = ['speech', 'music']
wf = wave.open('./data/01_Radioaufnahmen_Musik_Jingle_Sprache_mono2.wav', 'rb')

print('sample rate: '+ str(wf.getframerate()/1000.0) + 'kHz')
print('channels: '+ str(wf.getnchannels()) )

print('initialize pocketsphinx...' )
sd = SpeechDetector.SpeechDetector()
print('... done.' )

print('initialize speech/music classifier...')
[Classifier, MEAN, STD, classNames, mtWin, mtStep, stWin, stStep, computeBEAT] = aT.load_model("./data/speech_music_classifier/svmSM")
modelType = "svm"
print('... done.' )

print('initialize genre classifier...')
genre_recognizer = GenreRecognizer.GenreRecognizer('./data/genre_classifier/model.yaml', './data/genre_classifier/weights.h5')
print('... done.' )


p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
import time

#set chunk size in seconds to work with
chunk_size = 3
start_time = time.time()
Fs = wf.getframerate()
CHUNK = Fs * chunk_size

#read next chunk from audio file
data = wf.readframes(CHUNK)

#iterate over track
while data != '':
    #stream.write(data)
    array = _wav2array(wf.getnchannels(), wf.getsampwidth(), data)
    array = audioBasicIO.stereo2mono(array)
    #extract features
    MidTermFeatures = aF.mtFeatureExtraction(array, Fs, mtWin * Fs, mtStep * Fs, round(Fs * stWin), round(Fs * stStep))
    MidTermFeatures = MidTermFeatures[0]

    #classify chunks to speech/music
    flags = []
    Ps = []
    flagsInd = []
    for i in range(MidTermFeatures[0].shape[0]):  # for each feature vector (i.e. for each fix-sized segment):
        curFV = (MidTermFeatures[:, i] - MEAN) / STD  # normalize current feature vector
        [Result, P] = aT.classifierWrapper(Classifier, modelType, curFV)  # classify vector
        flagsInd.append(Result)
        flags.append(classNames[int(Result)])  # update class label matrix
        Ps.append(numpy.max(P))  # update probability matrix
    # 1-window smoothing
    #for i in range(1, len(flagsInd) - 1):
    #    if flagsInd[i - 1] == flagsInd[i + 1]:
    #        flagsInd[i] = flagsInd[i + 1]
    #(segs, classes) = flags2segs(flags, mtStep)  # convert fix-sized flags to segments and classes
    #segs[-1] = len(data) / float(Fs)

    flagsInd = numpy.array(flagsInd)

    #check what the majority is
    if (len(set(flagsInd)) == 1 and flagsInd[0] == 1):
        print("music")

        #create temp file
        tmp_file = wave.open('tmp_file.wav', 'w')
        tmp_file.setnchannels(1)
        tmp_file.setframerate(16000)
        tmp_file.setsampwidth(2)
        tmp_file.writeframesraw(data)
        tmp_file.close

        (predictions, duration) = genre_recognizer.recognize("tmp_file.wav")

        genre_distributions = GenreRecognizer.get_genre_distribution_over_time(
            predictions, duration)

        arr = []
        for i in range(0, len(genre_distributions)):
            stats = genre_distributions[i][1]
            arr.append(max(stats, key=stats.get))

        print(max(set(arr), key=arr.count))

    else:
        print("speech:")
        text = ' '.join([str(x) for x in sd.decode_phrase(array)]).decode('utf-8')
        print(text)

        #example to send action to OPC receiver
        if 'bundesregierung' in text :
            c = OSC.OSCClient()
            c.connect(('127.0.0.1', 57120))  # localhost, port 57120
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress("/getMessage")
            oscmsg.append('bundesregierung [POLITIK]')
            c.send(oscmsg)

    data = wf.readframes(CHUNK)

print("--- %s seconds ---" % (time.time() - start_time))
stream.stop_stream()
stream.close()
p.terminate()

