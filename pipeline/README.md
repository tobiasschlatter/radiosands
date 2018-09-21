# radiosands
Sound installation


Components:

- Radio interface
- Speech/Music classification
- Genre detection
- Voice recognition
  - Google Cloud Speech API (online)
  - PocketSphinx (offline) ([docs](sphinx/))
- Control protocol

### Setup
It is best to use a virtualenv using python 2.7.
You create it like this:
```sh
virtualenv --python=/usr/bin/python2.7 <path/to/new/virtualenv/>
```
activate it:
```sh
source path/to/new/virtualenv/bin/activate
```
install neccessary packages:
```sh
pip install -r requirements.txt
```
and terminate it
```sh
deactivate
```