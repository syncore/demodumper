from qldemo.constants import *

class FlattenableObject:
    def flatten(self):
        out = {}
        for key, value in self.__dict__.items():
            if key.startswith('__'):
                continue
            elif hasattr(value, 'flatten'):
                out[key]=value.flatten()
                continue
            if value.__class__ is list:
                out[key]=[member.flatten() for member in value if hasattr(member, 'flatten')]
                continue
            if value.__class__ is dict:
                out2={}
                for k, v in value.items():
                    if hasattr(v, 'flatten'):
                        out2[k]=v.flatten()
                    else:
                        out2[k]=v
                out[key]=out2
                continue
            out[key]=value
        return out

#class Scores(FlattenableObject):
#    def __init__(self, score_string):
#

class GameState(FlattenableObject):
    def __init__(self):
        self.configstrings = {}
        self.config = {}
        self.players = {}
        self.spectators = {}
        self.baselines = {}
        self.scores = {}
        self.error = False

class Trajectory(FlattenableObject):
  def __init__(self):
    self.trType = 0
    self.trTime = 0
    self.rDuration = 0
    self.trBase = [ 0 ] * 3
    self.trDelta = [ 0 ] * 3
    self.gravity = 0

class ServerCommand(FlattenableObject):
    seq = None
    cmd = None
    string = None
    error = False

    def __init__(self, seq, string):
        self.seq = seq
        self.cmd = string.split()[0]
        self.string = ' '.join(string.split()[1:])

class PlayerState(FlattenableObject):
  def __init__(self):
    self.commandTime = 0
    self.pm_type = 0
    self.bobCycle = 0
    self.pm_flags = 0
    self.pm_time = 0
    self.origin = [ 0 ] * 3
    self.velocity = [ 0 ] * 3
    self.weaponTime = 0
    self.gravity = 0
    self.speed = 0
    self.delta_angles = [ 0 ] * 3
    self.groundEntityNum = 0
    self.legsTimer = 0
    self.legsAnim = 0
    self.torsoTimer = 0
    self.torsoAnim = 0
    self.movementDir = 0
    self.grapplePoint = [ 0 ] * 3
    self.eFlags = 0
    self.eventSequence = 0
    self.events = [ 0 ] * MAX_PS_EVENTS
    self.eventParms = [ 0 ] * MAX_PS_EVENTS
    self.externalEvent = 0
    self.externalEventParm = 0
    self.externalEventTime = 0
    self.clientNum = 0
    self.weapon = 0
    self.weaponstate = 0
    self.viewangles = [ 0 ] * 3
    self.viewheight = 0
    self.damageEvent = 0
    self.damageYaw = 0
    self.damagePitch = 0
    self.damageCount = 0
    self.stats = [ 0 ] * MAX_STATS
    self.persistant = [ 0 ] * MAX_PERSISTANT
    self.powerups = [ 0 ] * MAX_POWERUPS
    self.ammo = [ 0 ] * MAX_WEAPONS
    self.generic1 = 0
    self.loopSound = 0
    self.jumppad_ent = 0
    self.ping = 0
    self.pmove_framecount = 0
    self.jumppad_frame = 0
    self.entityEventSequence = 0

class PlayerStateNETF:
  def __init__( self, player ):
    self.player = player
    self.fields = [ 0 ] * 48
    self.bits = []
    self.bits.append( 32 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 8 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( -16 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 8 )
    self.bits.append( -16 )
    self.bits.append( 16 )
    self.bits.append( 8 )
    self.bits.append( 4 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 16 )
    self.bits.append( GENTITYNUM_BITS )
    self.bits.append( 4 )
    self.bits.append( 16 )
    self.bits.append( 10 )
    self.bits.append( 16 )
    self.bits.append( 16 )
    self.bits.append( 16 )
    self.bits.append( 8 )
    self.bits.append( -8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 16 )
    self.bits.append( 16 )
    self.bits.append( 12 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 5 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 10 )
    self.bits.append( 16 )


    assert len( self.bits ) == len( self.fields )

  def __setitem__(self,index,value):
    self.fields[ index ] = value

  def __getitem__(self,index):
    return self.fields[ index ]

  def update(self):
    self.player.commandTime = self.fields[ 0 ]
    self.player.origin[ 0 ] = self.fields[ 1 ]
    self.player.origin[ 1 ] = self.fields[ 2 ]
    self.player.bobCycle = self.fields[ 3 ]
    self.player.velocity[ 0 ] = self.fields[ 4 ]
    self.player.velocity[ 1 ] = self.fields[ 5 ]
    self.player.viewangles[ 1 ] = self.fields[ 6 ]
    self.player.viewangles[ 0 ] = self.fields[ 7 ]
    self.player.weaponTime = self.fields[ 8 ]
    self.player.origin[ 2 ] = self.fields[ 9 ]
    self.player.velocity[ 2 ] = self.fields[ 10 ]
    self.player.legsTimer = self.fields[ 11 ]
    self.player.pm_time = self.fields[ 12 ]
    self.player.eventSequence = self.fields[ 13 ]
    self.player.torsoAnim = self.fields[ 14 ]
    self.player.movementDir = self.fields[ 15 ]
    self.player.events[ 0 ] = self.fields[ 16 ]
    self.player.legsAnim = self.fields[ 17 ]
    self.player.events[ 1 ] = self.fields[ 18 ]
    self.player.pm_flags = self.fields[ 19 ]
    self.player.groundEntityNum = self.fields[ 20 ]
    self.player.weaponstate = self.fields[ 21 ]
    self.player.eFlags = self.fields[ 22 ]
    self.player.externalEvent = self.fields[ 23 ]
    self.player.gravity = self.fields[ 24 ]
    self.player.speed = self.fields[ 25 ]
    self.player.delta_angles[ 1 ] = self.fields[ 26 ]
    self.player.externalEventParm = self.fields[ 27 ]
    self.player.viewheight = self.fields[ 28 ]
    self.player.damageEvent = self.fields[ 29 ]
    self.player.damageYaw = self.fields[ 30 ]
    self.player.damagePitch = self.fields[ 31 ]
    self.player.damageCount = self.fields[ 32 ]
    self.player.generic1 = self.fields[ 33 ]
    self.player.pm_type = self.fields[ 34 ]
    self.player.delta_angles[ 0 ] = self.fields[ 35 ]
    self.player.delta_angles[ 2 ] = self.fields[ 36 ]
    self.player.torsoTimer = self.fields[ 37 ]
    self.player.eventParms[ 0 ] = self.fields[ 38 ]
    self.player.eventParms[ 1 ] = self.fields[ 39 ]
    self.player.clientNum = self.fields[ 40 ]
    self.player.weapon = self.fields[ 41 ]
    self.player.viewangles[ 2 ] = self.fields[ 42 ]
    self.player.grapplePoint[ 0 ] = self.fields[ 43 ]
    self.player.grapplePoint[ 1 ] = self.fields[ 44 ]
    self.player.grapplePoint[ 2 ] = self.fields[ 45 ]
    self.player.jumppad_ent = self.fields[ 46 ]
    self.player.loopSound = self.fields[ 47 ]


class Snapshot(FlattenableObject):
  def __init__(self):
    self.valid = False
    self.snapFlags = 0
    self.serverTime = 0
    self.messageNum = 0
    self.deltaNum = 0
    self.ping = 0
    self.areamask = [ 0 ] * MAX_MAP_AREA_BYTES
    self.cmdNum = 0
    self.ps = None
    self.numEntities = 0
    self.parseEntitiesNum = 0
    self.serverCommandNum = 0
    #self.Error = False


class EntityState(FlattenableObject):
    def __init__(self):
        self.number = 0
        self.eType = 0
        self.eFlags = 0
        self.pos = Trajectory()
        self.apos = Trajectory()
        self.time = 0
        self.time2 = 0
        self.origin = [ 0 ] * 3
        self.origin2 = [ 0 ] * 3
        self.angles = [ 0 ] * 3
        self.angles2 = [ 0 ] * 3
        self.otherEntityNum = 0
        self.otherEntityNum2 = 0
        self.groundEntityNum = 0
        self.constantLight = 0
        self.loopSound = 0
        self.modelindex = 0
        self.modelindex2 = 0
        self.clientNum = 0
        self.frame = 0
        self.solid = 0
        self.event = 0
        self.eventParm = 0
        self.powerups = 0
        self.weapon = 0
        self.legsAnim = 0
        self.torsoAnim = 0
        self.generic1 = 0



class EntityStateNETF:
  def __init__(self,entity):
    self.entity = entity
    self.fields = [ 0 ] * 53
    self.bits = []
    self.bits.append( 32 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 32 )
    self.bits.append( 10 )
    self.bits.append( 0 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( GENTITYNUM_BITS )
    self.bits.append( 8 )
    self.bits.append( 19 )
    self.bits.append( GENTITYNUM_BITS )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 0 )
    self.bits.append( 32 )
    self.bits.append( 8 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 24 )
    self.bits.append( 16 )
    self.bits.append( 8 )
    self.bits.append( GENTITYNUM_BITS )
    self.bits.append( 8 )
    self.bits.append( 8 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 8 )
    self.bits.append( 0 )
    self.bits.append( 32 )
    self.bits.append( 32 )
    self.bits.append( 32 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 32 )
    self.bits.append( 32 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 0 )
    self.bits.append( 32 )
    self.bits.append( 16 )

    assert len( self.bits ) == len( self.fields )

  def __setitem__(self,index,value):
    self.fields[ index ] = value

  def update(self):
    self.entity.pos.trTime = self.fields[ 0 ]
    self.entity.pos.trBase[ 0 ] = self.fields[ 1 ]
    self.entity.pos.trBase[ 1 ] = self.fields[ 2 ]
    self.entity.pos.trDelta[ 0 ] = self.fields[ 3 ]
    self.entity.pos.trDelta[ 1 ] = self.fields[ 4 ]
    self.entity.pos.trBase[ 2 ] = self.fields[ 5 ]
    self.entity.apos.trBase[ 1 ] = self.fields[ 6 ]
    self.entity.pos.trDelta[ 2 ] = self.fields[ 7 ]
    self.entity.apos.trBase[ 0 ] = self.fields[ 8 ]
    self.entity.apos.gravity = self.fields[ 9 ]
    self.entity.event = self.fields[ 10 ]
    self.entity.angles2[ 1 ] = self.fields[ 11 ]
    self.entity.eType = self.fields[ 12 ]
    self.entity.torsoAnim = self.fields[ 13 ]
    self.entity.eventParm = self.fields[ 14 ]
    self.entity.legsAnim = self.fields[ 15 ]
    self.entity.groundEntityNum = self.fields[ 16 ]
    self.entity.pos.trType = self.fields[ 17 ]
    self.entity.eFlags = self.fields[ 18 ]
    self.entity.otherEntityNum = self.fields[ 19 ]
    self.entity.weapon = self.fields[ 20 ]
    self.entity.clientNum = self.fields[ 21 ]
    self.entity.angles[ 1 ] = self.fields[ 22 ]
    self.entity.pos.trDuration = self.fields[ 23 ]
    self.entity.apos.trType = self.fields[ 24 ]
    self.entity.origin[ 0 ] = self.fields[ 25 ]
    self.entity.origin[ 1 ] = self.fields[ 26 ]
    self.entity.origin[ 2 ] = self.fields[ 27 ]
    self.entity.solid = self.fields[ 28 ]
    self.entity.powerups = self.fields[ 29 ]
    self.entity.modelindex = self.fields[ 30 ]
    self.entity.otherEntityNum2 = self.fields[ 31 ]
    self.entity.loopSound = self.fields[ 32 ]
    self.entity.generic1 = self.fields[ 33 ]
    self.entity.origin2[ 2 ] = self.fields[ 34 ]
    self.entity.origin2[ 0 ] = self.fields[ 35 ]
    self.entity.origin2[ 1 ] = self.fields[ 36 ]
    self.entity.modelindex2 = self.fields[ 37 ]
    self.entity.angles[ 0 ] = self.fields[ 38 ]
    self.entity.time = self.fields[ 39 ]
    self.entity.apos.trTime = self.fields[ 40 ]
    self.entity.apos.trDuration = self.fields[ 41 ]
    self.entity.apos.trBase[ 2 ] = self.fields[ 42 ]
    self.entity.apos.trDelta[ 0 ] = self.fields[ 43 ]
    self.entity.apos.trDelta[ 1 ] = self.fields[ 44 ]
    self.entity.apos.trDelta[ 2 ] = self.fields[ 45 ]
    self.entity.apos.gravity = self.fields[ 46 ]
    self.entity.time2 = self.fields[ 47 ]
    self.entity.angles[ 2 ] = self.fields[ 48 ]
    self.entity.angles2[ 0 ] = self.fields[ 49 ]
    self.entity.angles2[ 2 ] = self.fields[ 50 ]
    self.entity.constantLight = self.fields[ 51 ]
    self.entity.frame = self.fields[ 52 ]
