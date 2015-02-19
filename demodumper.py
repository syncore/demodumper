#!/bin/env python

# # quake live demo -> json
# # Original author: Shawn Nock, 2014 (https://github.com/nocko/qldemo-python)
# Changes by syncore@syncore.org

import argparse
import json
import os
import sys
import time

from qldemo import QLDemo, gametype_to_string
from qldemo.data import GameState
#from qldemo.constants import userinfo_map, GT_TEAM, GT_RACE, TEAM_STRING_MAP

# # Configuration ##

# playerinfo stuff is from https://github.com/id-Software/Quake-III-Arena/blob/master/code/cgame/cg_players.c, but
# some is specific to quakelive (ws, su, so, rp, p)
playerinfo_override = {'n': 'name',  # The userInfo_t summary in
                       'c1': 'color1',
                       'c2': 'color2',
                       'cn': 'clan',  # CS_PLAYER[MAX_PLAYERS] has short
                       'xcn': 'xclan',  # hard to decipher names. Any map
                       'w': 'wins',  # here will override the name
                       'c': 'country',  # most of these are from
                       'l': 'losses',
                       't': 'team',
                       'tl': 'teamleader',
                       'tt': 'teamtask',
                       'ws': 'secondayweap',
                       'su': 'subscription',
                       'so': 'spec_only',
                       'rp': 'readytoplay'}

### END Configuration


def main():
    """ Set up some command-line arguments and handle them. """
    parser = argparse.ArgumentParser(
        description='Dump QuakeLive demo file info to json format')
    parser.add_argument('--silent', "-s", help='silent mode: display nothing on stdout', action='store_false')
    parser.add_argument('--output', "-o", help='name of the output JSON file when dumping from a text file', type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dir", "-d", help='directory containing .dm_73 & .dm_90 files to dump', type=is_valid_dir)
    group.add_argument('--file', "-f", help='individual .dm_73 or .dm_90 file to dump', type=is_valid_file)
    group.add_argument('--list', "-l", help='text file containing .dm_73 or .dm_90 files to dump', type=is_valid_file)
    args = parser.parse_args()

    if args.dir:
        # Use sequenced file names for directory dump.
        dumpdirectory(args.dir, args.silent)
    else:
        # Use filename as output file for single demo dump.
        if args.file:
            dumpsinglefile(args.file, args.silent)
            return
        if args.list:
            # Explicitly require output file for list of demos dump.
            if args.output:
                dumpdemolist(args.list, args.output, args.silent)
            else:
                if args.silent is not False:
                    print "No output file specified. Exiting."
                return
        else:
            if args.silent is not False:
                print "Invalid arguments specified. Exiting."
            return
    return 0


def dumpdirectory(directory, silent):
    """ Dump all .dm_73 and .dm_90 files in directory and associated sub-directories to json format"""
    demofilelist = []
    filenumber = 0
    # Scan demo directory and all sub-directories
    for root, dirs, files in os.walk(directory):
        for demofile in files:
            if demofile.endswith((".dm_73", ".dm_90")):
                fullpath = os.path.join(root, demofile)
                filenumber += 1
                if silent is not False:
                    print "[INFO] Found QL demo file: {0} - #{1}".format(fullpath, filenumber)
                demofilelist.append(fullpath)
    # x demos at a time (x=128)
    parsednum = 0
    failednum = 0
    demofilelist_chunk = [demofilelist[x:x+128] for x in range(0, len(demofilelist), 128)]
    for i, chunk in enumerate(demofilelist_chunk):
        results = []
        for result in resultgenerator(chunk):
            if 'failed' not in result:
            #if len(result) is not 0:
                results.append(result)
                parsednum += 1
                if silent is not False:
                    print "[INFO] Parsed demo file {0} (#{1} of {2})".\
                        format(result['filename'], parsednum+failednum, (len(demofilelist)))
            else:
                failednum += 1
                print "[ERROR] Corrupt demo: Unable to open demo file {0} (#{1} of {2})".\
                    format(result['failed'], parsednum+failednum, (len(demofilelist)))
        # No point writing JSON if nothing has been successfully parsed...
        if len(results) is not 0:
            filename = "demodir-{0}.uql".format(i)
            with open(filename, 'w') as resultfile:
                for r in json.JSONEncoder().iterencode(results):
                    resultfile.write(r)
            filesize = os.stat(filename).st_size * .000001
            if silent is not False:
                print "=========> [INFO] Successfully wrote {0:.2f} MB file ({1}) to disk. <========".\
                    format(filesize, filename)
    return


def dumpdemolist(listfile, outputfile, silent):
    """ Dump a list of .dm_73 & .dm_90 in a text file to json format on disk. """
    # Note: for file list dump, another application handles splitting of the list that is fed to this function.
    toparse = []
    results = []
    parsednum = 0
    toparsenum = 0
    failednum = 0
    with open(listfile) as lf:
        for demo in lf:
            demo = demo.strip('\n')
            if os.path.isfile(demo):
                if demo.endswith((".dm_73", ".dm_90")):
                    toparse.append(demo)
                    toparsenum += 1
                else:
                    print "[ERROR] {0} exists on disk, but is not a valid Quake Live demo file.".format(demo)
            else:
                print "[ERROR] {0} does not exist on the disk."\
                    .format(demo)
    for result in resultgenerator(toparse):
        if 'failed' not in result:
            results.append(result)
            parsednum += 1
            if silent is not False:
                print "[INFO] Parsed demo file {0} (#{1} of {2})".\
                    format(result['filename'], parsednum+failednum, (len(toparse)))
        else:
            failednum += 1
            print "[ERROR] Corrupt demo: Unable to open demo file {0} (#{1} of {2})".\
                format(result['failed'], parsednum+failednum, len(toparse))
    # No point writing JSON if nothing has been successfully parsed...
    if len(results) is not 0:
        with open(outputfile, 'w') as output:
            for r in json.JSONEncoder().iterencode(results):
                output.write(r)
        filesize = os.stat(outputfile).st_size * .000001
        if silent is not False:
                print "=========> [INFO] Successfully wrote {0:.2f} MB output file ({1}) to disk. <========="\
                    .format(filesize, outputfile)


def dumpsinglefile(file, silent):
    """ Dump a single .dm_73 or .dm_90 file to the disk in json format. """
    toparse = []
    results = []
    filenumber = 0
    toparse.append(file)
    for result in resultgenerator(toparse):
        if len(result) is not 0:
            results.append(result)
            filenumber += 1
            if silent is not False:
                print "[INFO] Parsed demo file {0} (#{1} of {2})"\
                    .format(result['filename'], filenumber, (len(toparse)))
            filename = result['filename'].strip('.dm_73').strip('.dm_90')+".uql"
            with open(filename, 'w') as output:
                for r in json.JSONEncoder().iterencode(results):
                    output.write(r)
            filesize = os.stat(filename).st_size * .000001
            if silent is not False:
                print "=========> [INFO] Successfully wrote {0:.2f} MB output file: {1} to disk. <========"\
                    .format(filesize, filename)
        else:
            if silent is not False:
                print "[ERROR] Unable to parse {0} ...skipping.".format(file)
    return


def resultgenerator(filelist):
    """ Generator for actually parsing the demo files. """
    for demo in filelist:
        q = QLDemo(demo)
        qld = None
        # call QLDemo's __iter()__
        for a in q:
            # GameState contains bulk of the required info.
            # Would be nice to parse all the ServerCommands
            # to accumulate total scores and chat messages
            # but that's not happening w/ buggy huffman code/Python on Windows,
            # on Linux it's fine, but since target platform is Windows....
            if a.__class__ is GameState:
                qld = a
                break
        if qld is not None:
            if not qld.error:
                recordedby = None
                # Override playerinfo for players & see if demo pov is from player
                for clientNum, player in qld.players.items():
                    if clientNum == qld.clientNum:
                        recordedby = player['n']
                    for key, value in player.items():
                        new_name = playerinfo_override.get(key, None)
                        if new_name:
                            player[new_name] = player[key]
                            del (player[key])
                # Override playerinfo for spectators & see if demo pov is from spectator
                for clientNum, spectator in qld.spectators.items():
                    if clientNum == qld.clientNum:
                        recordedby = spectator['n']
                    for key, value in spectator.items():
                        new_name = playerinfo_override.get(key, None)
                        if new_name:
                            spectator[new_name] = spectator[key]
                            del (spectator[key])
                # if serverinfo isn't present, then there's no point
                if not 'serverinfo' in qld.config:
                    yield {}
                # g_levelStartTime should be there, but sometimes reported as not
                if not 'g_levelStartTime' in qld.config['serverinfo']:
                    timeval = 0
                else:
                    timeval = qld.config['serverinfo']['g_levelStartTime']
                output = {'filename': demo.split(os.sep)[-1],
                          'recorded_by': recordedby,
                          'timestamp': time.ctime(float(timeval)),
                          'gametype': int(qld.config['serverinfo']['g_gametype']),
                          'gametype_title': gametype_to_string(qld.config['serverinfo']['g_gametype']),
                          'map_name': qld.config['serverinfo']['mapname'],
                          'players': qld.players.values(),
                          'protocol': qld.config['serverinfo']['protocol'],
                          'size': os.stat(demo).st_size * .000001,
                          'srvinfo': qld.config['serverinfo'],
                          'spectators': qld.spectators.values()}
                yield output
            else:
                yield {'failed': demo.split(os.sep)[-1]}
        # Unable to open demo for whatever reason (corrupt, etc.)
        else:
            q.closefile()
            del qld
            yield {'failed': demo.split(os.sep)[-1]}
        q.closefile()


def is_valid_dir(dirname):
    """ Check to see if it is a valid directory. """
    if not os.path.isdir(dirname):
        msg = "{0} is not a valid directory... Exiting.".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def is_valid_file(filename):
    """ Check to see if it is a valid file. """
    if not os.path.isfile(filename):
        msg = "{0} is not a valid file... Exiting.".format(filename)
        raise argparse.ArgumentTypeError(msg)
    else:
        return filename

if __name__ == '__main__':
        main()