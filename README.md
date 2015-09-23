# markov-music-gen

Generating music using music21 and Markov Chains!

## Using this program!

### What you'll need:

* Python 2.7. The port to Python 3 is very possible, and I'll probably do it at some point. To procrastinate.
* Some kind of MusicXML reader. I'd recommend MuseScore because it has a portable version, and it's free and totally cool.
* The music21 library for Python.

### Set up on Windows

I don't normally use Windows, I just need it to work on Windows as that's probably what the examiners will use and that's what my school computer runs. So I now know this quite well! For this method you'll need to have installed pip. If you're at my school and you want to install this for some reason, you'll want to follow these instructions!

If you haven't already got Python installed, go to Python's website and run the applicable installer. Then go to Python27/Scripts. This will probably be in C://, although I only base that off my preinstalled version. Then run 
```
pip install music21
```
to install music21. Then grab your favourite MusicXML editor (*cough*MuseScore*cough*), and assign it to MusicXML files by right-clicking a .xml file (which can be found in /data), selecting Open With..., choosing your editor and ticking the "Always use..." box. That should do it!

### Set up on Linux

You know how to do this, I'm sure. But just in case, I'll mention the packages you'll need. See https://musescore.org/apt first for instructions about adding the MuseScore PPA, or you could just install it yourself.
```
sudo apt-get install python musescore
pip install music21
```