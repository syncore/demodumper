# DemoDumper

Dumps Quake Live demo files to JSON format.
Originally written by [Shawn Nock](https://github.com/nocko/qldemo-python) with original Huffman Python wrapper by [Petr Skramovsky](https://code.google.com/p/pyq3a/) Quake 3 demo specification is available at www.elho.net/games/q3/q3dspecs.htm

I have added some modifications (such as directory dumping & file output) to support an application I am currently building.

Note: you will need a C compiler to build the pyhuffman C extension.

    python setup.py build

### Run:

To dump a directory of demo files to JSON:

    python demodumper.py -d "path-to-demo-files"

To dump a single demo file to JSON:

    python demodumper.py -f "demo-file.dm_73"

To dump a text file containing paths to demos (one full path per line):

    python demodumper.py -l "path-to-text-file" -o "name-of-output-json-file.json"

# Testers

If you would like to help us fix bugs but you don't have any .dm_73 demo test data (demo files), [an archive of roughly 100 demos can be found here.](http://goo.gl/gnsTcx) If you need even more, there are plenty of demo files available at [the trance.gg website](http://trance.gg/Quake-demos/)

Even more archive files containing tons of demos from trance.gg:
* [All QuakeCon 2011 demos, 1.8 GB](http://trance.gg/Quake-demos/QuakeCon%202011/ALLDEMOSqcon2011.rar)
* [All QuakeCon 2012 CTF demos, 833 MB](http://trance.gg/Quake-demos/QuakeCon%202012/Quake%20Live%20CTF/qcon2012_ctf_open_results.zip)
* [All QuakeCon 2012 Duel Masters demos, 247.2 MB](http://trance.gg/Quake-demos/QuakeCon%202012/Quake%20Live%20Duel/qcon2012_duel_masters_results.zip)
