#!/bin/env python

## ql-demo-parse.py
## Shawn Nock, 2014

# Standard Lib
import copy
import json
import os
import re
import struct
import sys

# C-Extension wrapping Q3A Huffman Routines
import huffman
import struct

# Constants and enum maps
from qldemo.constants import *
from qldemo.data import (GameState, EntityState, PlayerState,
                         EntityStateNETF, PlayerStateNETF,
                         ServerCommand, Snapshot)

# Configuration

# Utility Functions

# Classes


class QLDemo:

    def __init__(self, demofilename):
        huffman.init()
        huffman.open(demofilename)
        self.demoname = demofilename
        self.gamestate = GameState()
        self.gamestate.players = {}
        self.gamestate.spectators = {}
        self.chatseqs = set()
        self.packets = []
        self.snapshots = []
        self.scores = []
        self.chats = []
        self.error = False

    def get_demoname(self):
        return self.demoname

    def __iter__(self):
        while True:
            seq=huffman.readrawlong()
            length=huffman.readrawlong()
            r = None

            if seq == -1 or length == -1:
                break
            huffman.fill(length)
            ack = huffman.readlong()
            cmd = huffman.readbyte()

            if cmd == SVC_GAMESTATE:
                r = self.parse_gamestate()
            elif cmd == SVC_SERVERCOMMAND:
                r = self.parse_servercommand()
            elif cmd == SVC_SNAPSHOT:
                # not necessary for summary
                continue
                r = self.parse_snapshot()
            if r is None:
                self.error = True
                break
            yield r

    def closefile(self):
        huffman.close(self.demoname)
        return

    def parse_gamestate(self):
        ack=huffman.readlong()
        while True:
            cmd = huffman.readbyte()
            if cmd == SVC_EOF:
                break
            elif cmd == SVC_CONFIGSTRING:
                self.parse_configstring()
            elif cmd == SVC_BASELINE:
                self.parse_baseline()
        self.gamestate.clientNum = huffman.readlong()
        self.gamestate.checksumFeed = huffman.readlong()
        return self.gamestate

    def parse_configstring(self, data=(None, None)):

        i, string = data
        if not i:
            i = huffman.readshort()
            string = huffman.readbigstring()
        dest=self.gamestate.configstrings
        fieldname=str(i)
        output=string
        if CS_STRING_MAP.get(i, None):
            dest=self.gamestate.config
            fieldname=CS_STRING_MAP.get(i)
        if string.startswith("\\"):
            output={}
            subfields = string.split('\\')
            if not fieldname in dest:
                dest[fieldname]={}
            for x in range(1, len(subfields)-1, 2):
                output[subfields[x]]=subfields[x+1]
        if i >= CS_PLAYERS and i < CS_PLAYERS+MAX_CLIENTS:
            clientNum = i-CS_PLAYERS
            fieldname=int(clientNum)
            subfields = string.split('\\')
            output = {}
            for x in range(0, len(subfields), 2):
                output[subfields[x]]=subfields[x+1]
                #print output[subfields[x]]
            if output['t'] == TEAM_SPECTATOR:
                dest=self.gamestate.spectators
            else:
                dest=self.gamestate.players
        #if i >= CS_SOUNDS and i < CS_SOUNDS+MAX_SOUNDS:
            #dest=self.gamestate.config
            #fieldname='sound'+str(i-CS_SOUNDS)
        #if i >= CS_LOCATIONS and i < CS_LOCATIONS+MAX_LOCATIONS:
            #dest=self.gamestate.config
            #fieldname='location{:02d}'.format(i-CS_LOCATIONS)
        dest[fieldname]=output

    def parse_baseline(self):
        newnum = huffman.readbits(GENTITYNUM_BITS)
        null_state=EntityState()
        baseline = self.read_delta_entity(null_state, newnum)
        ## Broken for now, disabling for speed
        #self.gamestate.baselines[newnum]=baseline

    def read_delta_entity(self, frm, num):
        ## Check for server order to remove a baseline
        if huffman.readbits(1) == 1:
            # Don't know how we should handle this, it does mean no
            # new data; skipping for now
            return
        ## Check for 'no delta' flag
        if huffman.readbits(1) == 0:
            ## No changes, we should make 'from' a copy of
            ## 'to'... skipping for now
            return

        last_field = huffman.readbyte()
        entity = EntityState()
        netf = EntityStateNETF(entity)

        for i in range(0, last_field):
            if huffman.readbits(1) :
                if not netf.bits[i] :
                    if huffman.readbits(1) != 0:
                        if huffman.readbits(1) == 0:
                            netf.fields[i] = huffman.readbits(FLOAT_INT_BITS)
                        else :
                            netf.fields[i] = huffman.readfloat()
                else:
                    if huffman.readbits(1) != 0:
                        netf.fields[i] = huffman.readbits(netf.bits[i])

        netf.update()
        return entity

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()

        sc=ServerCommand(seq, string)
        if sc.cmd == "scores_duel":
            sc = self.parse_duel_scores(sc)
            self.scores.append(sc.scores)
        elif sc.cmd == "scores_ctf":
            sc = self.parse_ctf_scores(sc)
            self.scores.append(sc.scores)
        elif sc.cmd == "scores":
            sc = self.parse_old_scores(sc)
            self.scores.append(sc.scores)
        elif sc.cmd == 'cs' or sc.cmd == 'bcs':
            self.update_configstring(sc)
        elif sc.cmd == "chat":
            sc = self.parse_chat_event(sc)
            if sc.chats is not None:
                self.chats.append(sc.chats)
            self.chatseqs.add(seq)
        return sc

    def update_configstring(self, command):
        ls = command.string.split(' ')
        cs_num = int(ls[0])
        cs = ' '.join(ls[1:]).strip('"')
        self.parse_configstring((cs_num, cs))


    def parse_chat_event(self, command):
        ls=command.string.split()
        command.chats = None
        offset = 1

        # offset+0 = clan tag + player name
        # offset+1 = playername only
        #num_chat = ls[offset+1]

        # message = clan tag + playername + message
        message = ' '.join(ls[1:]).strip('"')
        player = message.split(':', 1)[0].replace(u'\x19', '')

        if command.seq not in self.chatseqs:
            if command.chats is None:
                command.chats = {}
            command.chats['player'] = player
            command.chats['msg'] = message

        return command

    def parse_duel_scores(self, command):
        offset = 1
        ls = command.string.split()
        num_scores = int(ls[0])
        command.scores={}
        for client in range(num_scores):
            client_num = ls[offset+0]
            command.scores[client_num]={}
            command.scores[client_num]['score'] = ls[offset+1]
            command.scores[client_num]['ping'] = ls[offset+2]
            command.scores[client_num]['time'] = ls[offset+3]
            command.scores[client_num]['kills'] = ls[offset+4]
            command.scores[client_num]['deaths'] = ls[offset+5]
            command.scores[client_num]['accuracy'] = ls[offset+6]
            command.scores[client_num]['best_weapon'] = ls[offset+7]
            command.scores[client_num]['damage_dealt'] = ls[offset+8]
            command.scores[client_num]['impressive'] = ls[offset+9]
            command.scores[client_num]['excellent'] = ls[offset+10]
            command.scores[client_num]['gauntlet'] = ls[offset+11]
            command.scores[client_num]['perfect'] = ls[offset+12]
            command.scores[client_num]['red_armor_pickups'] = ls[offset+13]
            command.scores[client_num]['red_armor_pickup_time'] = ls[offset+14]
            command.scores[client_num]['yellow_armor_pickups'] = ls[offset+15]
            command.scores[client_num]['yellow_armor_pickup_time'] = ls[offset+16]
            command.scores[client_num]['green_armor_pickups'] = ls[offset+17]
            command.scores[client_num]['green_armor_pickup_time'] = ls[offset+18]
            command.scores[client_num]['mega_health_pickups'] = ls[offset+19]
            command.scores[client_num]['mega_healh_pickup_time'] = ls[offset+20]
            offset+=21
            command.scores[client_num]['weapon_stats'] = []
            for i in range(WP_GAUNTLET, WP_NUM_WEAPONS-1):
                weapon = {}
                weapon['hit'] = ls[offset+0]
                weapon['fired'] = ls[offset+1]
                weapon['accuracy'] = ls[offset+2]
                weapon['damage_dealt'] = ls[offset+3]
                weapon['kills'] = ls[offset+4]
                command.scores[client_num]['weapon_stats'].append(weapon)
                offset += 5
        return command

    def parse_ctf_scores(self, command):
        ls=command.string.split()
        command.scores={}
        command.scores['TEAM_RED'] = {}
        command.scores['TEAM_RED']['red_armor']    = ls[0]
        command.scores['TEAM_RED']['yellow_armor'] = ls[1]
        command.scores['TEAM_RED']['green_armor']  = ls[2]
        command.scores['TEAM_RED']['mega_health']  = ls[3]
        command.scores['TEAM_RED']['quad_damage']  = ls[4]
        command.scores['TEAM_RED']['battle_suit']  = ls[5]
        command.scores['TEAM_RED']['regeneration'] = ls[6]
        command.scores['TEAM_RED']['haste']        = ls[7]
        command.scores['TEAM_RED']['invisibility'] = ls[8]
        command.scores['TEAM_RED']['flag']         = ls[9]
        command.scores['TEAM_RED']['medkit']       = ls[10]
        command.scores['TEAM_RED']['quad_damage_time']  = ls[11]
        command.scores['TEAM_RED']['battle_suit_time']  = ls[12]
        command.scores['TEAM_RED']['regeneration_time']  = ls[13]
        command.scores['TEAM_RED']['haste_time']  = ls[14]
        command.scores['TEAM_RED']['invisibility_time']  = ls[15]
        command.scores['TEAM_RED']['flag_time']  = ls[16]
        command.scores['TEAM_BLUE'] = {}
        command.scores['TEAM_BLUE']['red_armor']    = ls[17]
        command.scores['TEAM_BLUE']['yellow_armor'] = ls[18]
        command.scores['TEAM_BLUE']['green_armor']  = ls[19]
        command.scores['TEAM_BLUE']['mega_health']  = ls[20]
        command.scores['TEAM_BLUE']['quad_damage']  = ls[21]
        command.scores['TEAM_BLUE']['battle_suit']  = ls[22]
        command.scores['TEAM_BLUE']['regeneration'] = ls[23]
        command.scores['TEAM_BLUE']['haste']        = ls[24]
        command.scores['TEAM_BLUE']['invisibility'] = ls[25]
        command.scores['TEAM_BLUE']['flag']         = ls[26]
        command.scores['TEAM_BLUE']['medkit']       = ls[27]
        command.scores['TEAM_BLUE']['quad_damage_time']  = ls[28]
        command.scores['TEAM_BLUE']['battle_suit_time']  = ls[29]
        command.scores['TEAM_BLUE']['regeneration_time']  = ls[30]
        command.scores['TEAM_BLUE']['haste_time']  = ls[31]
        command.scores['TEAM_BLUE']['invisibility_time']  = ls[32]
        command.scores['TEAM_BLUE']['flag_time']  = ls[33]

        num_scores = ls[34]
        command.scores['TEAM_RED']['score'] = ls[35]
        command.scores['TEAM_BLUE']['score'] = ls[36]
        offset = 0
        for client in range(int(num_scores)):
            client_num = ls[offset+37]
            command.scores[client_num]={}
            command.scores[client_num]['team'] = ls[offset+38]
            command.scores[client_num]['premium'] = ls[offset+39]
            command.scores[client_num]['score'] = ls[offset+40]
            command.scores[client_num]['ping'] = ls[offset+41]
            command.scores[client_num]['time'] = ls[offset+42]
            command.scores[client_num]['kills'] = ls[offset+43]
            command.scores[client_num]['deaths'] = ls[offset+44]
            command.scores[client_num]['powerups'] = ls[offset+45]
            command.scores[client_num]['accuracy'] = ls[offset+46]
            command.scores[client_num]['best_weapon'] = ls[offset+47]
            command.scores[client_num]['impressive'] = ls[offset+48]
            command.scores[client_num]['excellent'] = ls[offset+49]
            command.scores[client_num]['gauntlet'] = ls[offset+50]
            command.scores[client_num]['defend'] = ls[offset+51]
            command.scores[client_num]['assist'] = ls[offset+52]
            command.scores[client_num]['captures'] = ls[offset+53]
            command.scores[client_num]['perfect'] = ls[offset+54]
            command.scores[client_num]['alive'] = ls[offset+55]
            offset += 19
        return command

    def parse_old_scores(self, command):
        ls = command.string.split()
        command.scores = {}
        num_scores = int(ls[0])
        command.scores['TEAM_RED'] = ls[1]
        command.scores['TEAM_BLUE'] = ls[2]
        offset = 3
        for client in range(num_scores):
            client_num = ls[offset+0]
            command.scores[client_num]={}
            command.scores[client_num]['score'] = ls[offset+1]
            command.scores[client_num]['ping'] = ls[offset+2]
            command.scores[client_num]['time'] = ls[offset+3]
            command.scores[client_num]['powerups'] = ls[offset+4]
            command.scores[client_num]['accuracy'] = ls[offset+5]
            command.scores[client_num]['impressive'] = ls[offset+6]
            command.scores[client_num]['excellent'] = ls[offset+7]
            command.scores[client_num]['gauntlet'] = ls[offset+8]
            command.scores[client_num]['defend'] = ls[offset+9]
            command.scores[client_num]['assist'] = ls[offset+10]
            command.scores[client_num]['perfect'] = ls[offset+11]
            command.scores[client_num]['captures'] = ls[offset+12]
            command.scores[client_num]['alive'] = ls[offset+13]
            command.scores[client_num]['kills'] = ls[offset+10]
            command.scores[client_num]['deaths'] = ls[offset+11]
            command.scores[client_num]['best_weapon'] = ls[offset+12]
            offset+=18
        return command

    def parse_snapshot(self):
        new_snap = Snapshot()
        new_snap.serverTime=huffman.readlong()
        delta_num = huffman.readbyte()
        new_snap.snapFlags = huffman.readbyte()
        new_snap.areamaskLen = huffman.readbyte()
        #for i in range(new_snap.areamaskLen+1):
        #    new_snap.areamask.append(huffman.readbyte())
        #ps = self.parse_playerstate()
        #new_snap.playerstate=ps
        return new_snap

    def parse_playerstate(self):
        last_field=huffman.readbyte()
        player=PlayerState()
        netf=PlayerStateNETF(player)

        playerStateFieldsNum  = len( netf.bits )

        if last_field > playerStateFieldsNum :
            return None

        for i in range( 0, last_field) :
            if huffman.readbits( 1 ) :
                if netf.bits[ i ] == 0 :
                    if huffman.readbits( 1 ) == 0 :
                        netf.fields[ i ] = huffman.readbits( FLOAT_INT_BITS ) - FLOAT_INT_BIAS
                    else :
                        netf.fields[ i ] = huffman.readfloat()
                else :
                    bits = netf.bits[ i ]
                    netf.fields[ i ] = huffman.readbits( bits )
        netf.update()

        if huffman.readbits( 1 ) :
            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_STATS ) :
                    if c & ( 1 << i ) :
                        player.stats[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_PERSISTANT ) :
                    if c & ( 1 << i ) :
                        player.persistant[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_WEAPONS ) :
                    if c & ( 1 << i ) :
                        player.ammo[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_POWERUPS ) :
                    if c & ( 1 << i ) :
                        player.powerups[ i ] = huffman.readlong()

        return player


