# Voice Recognition with PocketSphinx

PocketSphinx is a good option for offline voice recognition.

## Installing on Raspberry Pi

Follow these [installation instructions](http://www.robotrebels.org/index.php?topic=220.0) to compile sphinxbase and pocketsphinx on the raspberry pi. Summary:

#### Prerequisites

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install bison libasound2-dev swig python-dev mplayer
```

#### SphinxBase

```
cd ~/Downloads
wget http://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz
tar -zxvf ./sphinxbase-5prealpha.tar.gz
cd ./sphinxbase-5prealpha
./configure --enable-fixed
make clean all
sudo make install
cd ..
```

#### PocketSphinx

```
cd ~/Downloads
wget http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz
tar -zxvf pocketsphinx-5prealpha.tar.gz
cd ./pocketsphinx-5prealpha
./configure
make clean all
sudo make install
```

#### Environmental variables

Put this in your `.bashrc`:

```
export LD_LIBRARY_PATH=/usr/local/lib
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
```

## Language Model


# Testing

This command will listen on alsa device 1,0 for input and print anything it recognises. Use `cat /proc/asound/cards` to determine which device is your microphone.

```
pocketsphinx_continuous -hmm ~/sphinx_models/cmusphinx-en-us-ptm-8khz-5.2 \
    -lm ~/sphinx_models/custom/1054.lm -dict ~/sphinx_models/custom/1054.dic \
    -adcdev plughw:1,0 -inmic yes -samprate 8000
```
