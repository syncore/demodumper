GENTITYNUM_BITS = 10
MAX_GENTITIES = 1 << GENTITYNUM_BITS
FLOAT_INT_BITS = 13
FLOAT_INT_BIAS = (1<<(FLOAT_INT_BITS-1))

## Message Types
SVC_BAD=0
SVC_NOP=1
SVC_GAMESTATE=2
SVC_CONFIGSTRING=3
SVC_BASELINE=4
SVC_SERVERCOMMAND=5
SVC_DOWNLOAD=6
SVC_SNAPSHOT=7
SVC_EOF=8

## Trajectory Types
TR_STATIONARY=0
TR_INTERPOLATE=1
TR_LINEAR=2
TR_LINEAR_STOP=3
TR_SINE=4,
TR_GRAVITY=5

## Entity Types
ET_GENERAL=0
ET_PLAYER=1
ET_ITEM=2
ET_MISSILE=3
ET_MOVER=4
ET_BEAM=5
ET_PORTAL=6
ET_SPEAKER=7
ET_PUSH_TRIGGER=8
ET_TELEPORT_TRIGGER=9
ET_INVISIBLE=10
ET_GRAPPLE=11             # grapple hooked on wall
ET_TEAM=12
ET_EVENTS=13

## Means of Death
MOD_UNKNOWN=0
MOD_SHOTGUN=1
MOD_GAUNTLET=2
MOD_MACHINEGUN=3
MOD_GRENADE=4
MOD_GRENADE_SPLASH=5
MOD_ROCKET=6
MOD_ROCKET_SPLASH=7
MOD_PLASMA=8
MOD_PLASMA_SPLASH=9
MOD_RAILGUN=10
MOD_LIGHTNING=11
MOD_BFG=12
MOD_BFG_SPLASH=13
MOD_WATER=14
MOD_SLIME=15
MOD_LAVA=16
MOD_CRUSH=17
MOD_TELEFRAG=18
MOD_FALLING=19
MOD_SUICIDE=20
MOD_TARGET_LASER=21
MOD_TRIGGER_HURT=22
MOD_GRAPPLE=23

## Team Task
TEAMTASK_NONE=0
TEAMTASK_OFFENSE=1
TEAMTASK_DEFENSE=2
TEAMTASK_PATROL=3
TEAMTASK_FOLLOW=4
TEAMTASK_RETRIEVE=5
TEAMTASK_ESCORT=6
TEAMTASK_CAMP=7

## Team
TEAM_FREE='0'
TEAM_RED='1'
TEAM_BLUE='2'
TEAM_SPECTATOR='3'
TEAM_NUM_TEAMS='4'

TEAM_STRING_MAP={
    TEAM_FREE: 'NONE',
    TEAM_RED: 'TEAM_RED',
    TEAM_BLUE: 'TEAM_BLUE',
    TEAM_SPECTATOR: 'SPECTATOR'
}

## Gametypes
GT_FFA=0                         # free for all
GT_DUEL=1          # one on one tournament
GT_RACE=2       # single player ffa
GT_TEAM=3               # team deathmatch
GT_CA=4
GT_CTF=5                 # capture the flag
GT_1FCTF=6
GT_OBELISK=7
GT_HARVESTER=8
GT_FREEZETAG=9
GT_DOMINATION=10
GT_ATTACK_AND_DEFEND=11
GT_REDROVER=12
GT_MAX_GAME_TYPE=13

GT_STRING_MAP={GT_FFA: 'FFA',
               GT_DUEL: 'DUEL',
               GT_RACE: 'RACE',
               GT_TEAM: 'TDM',
               GT_CA: 'CA',
               GT_CTF: 'CTF',
               GT_1FCTF: '1FCTF',
               GT_OBELISK: 'OBELISK',
               GT_HARVESTER: 'HARVESTER',
               GT_FREEZETAG: 'FREEZETAG',
               GT_DOMINATION: 'DOMINATION',
               GT_ATTACK_AND_DEFEND: 'AD',
               GT_REDROVER: 'REDROVER',
}

def gametype_to_string(i):
    i=int(i)
    return GT_STRING_MAP.get(i, None)

MAX_MODELS = 256 # Not the same as Q3A
MAX_SOUNDS = 256 # Not the same as Q3A
MAX_CLIENTS = 64 
MAX_LOCATIONS = 64
MAX_PS_EVENTS = 2
MAX_STATS = 16
MAX_PERSISTANT = 16
MAX_POWERUPS = 16
MAX_WEAPONS = 16
MAX_MAP_AREA_BYTES = 32

# Configstring Definitions from Q3A source headers with mods for QL
CS_SERVERINFO = 0
CS_SYSTEMINFO = 1
CS_MUSIC = 2
CS_MESSAGE = 3               # from the map worldspawn's message field
CS_MOTD = 4              # g_motd string for server message of the day
CS_WARMUP = 5               # server time when the match will be restarted
CS_SCORES1 = 6
CS_SCORES2 = 7
CS_VOTE_TIME = 8
CS_VOTE_STRING = 9
CS_VOTE_YES = 10
CS_VOTE_NO = 11
CS_GAME_VERSION = 12
CS_LEVEL_START_TIME = 13
CS_INTERMISSION = 14
CS_ITEMS = 15
CS_BOTINFO = 16
CS_MODELS = 17

CS_SOUNDS = (CS_MODELS+MAX_MODELS)
CS_PLAYERS = (CS_SOUNDS+MAX_SOUNDS)
CS_LOCATIONS = (CS_PLAYERS+MAX_CLIENTS)
CS_LAST_GENERIC = (CS_LOCATIONS + MAX_LOCATIONS) # Should be 656

CS_FLAGSTATUS = 658
CS_SCORES1PLAYER = 659
CS_SCORES2PLAYER = 660
CS_ROUND_WARMUP = 661
CS_ROUND_START_TIME = 662 
CS_TEAMCOUNT_RED = 663
CS_TEAMCOUNT_BLUE = 664
CS_SHADERSTATE = 665
CS_NEXTMAP = 666
CS_PRACTICE = 667
CS_FREECAM = 668

CS_PAUSE_START_TIME = 669   # if this is non-zero, the game is paused
CS_PAUSE_END_TIME = 670     # 0 = pause, !0 = timeout

CS_TIMEOUTS_RED = 671        # TOs REMAINING
CS_TIMEOUTS_BLUE = 672

CS_MODEL_OVERRIDE = 673
    
CS_PLAYER_CYLINDERS = 674
CS_DEBUGFLAGS = 675
CS_ENABLEBREATH = 676
CS_TEAMLOCATORS = 677
CS_DMGTHROUGHDEPTH = 678
CS_AUTHOR = 679             # from the map worldspawn's author field
CS_AUTHOR2 = 680 
CS_ADVERT_DELAY = 681
CS_PMOVEINFO = 682
CS_ARMORINFO = 683
CS_WEAPONINFO = 684
CS_PLAYERINFO = 685
CS_1STPLAYER = 686
CS_2NDPLAYER = 687
CS_SCORE1STPLAYER = 688
CS_SCORE2NDPLAYER = 689
CS_ATMOSEFFECT =  690 # unused =  was per-map rain/snow effects
CS_MOST_DAMAGEDEALT_PLYR = 691 
CS_MOST_ACCURATE_PLYR = 692
CS_REDTEAMNAME = 693
CS_BLUETEAMNAME = 694
CS_REDTEAMCLANTAG = 695
CS_BLUETEAMCLANTAG = 696
CS_BEST_ITEMCONTROL_PLYR = 697 
CS_SERVER_OWNER = 698
CS_MOST_VALUABLE_OFFENSIVE_PLYR = 699
CS_MOST_VALUABLE_DEFENSIVE_PLYR = 700
CS_MOST_VALUABLE_PLYR = 701
CS_GENERIC_COUNT_RED = 702
CS_GENERIC_COUNT_BLUE = 703
CS_AD_SCORES = 704
CS_ROUND_WINNER = 705
CS_CUSTOM_SETTINGS = 706
CS_ROTATIONMAPS = 707
CS_ROTATIONVOTES = 708
CS_DISABLE_VOTE_UI = 709
CS_ALLREADY_TIME = 710
CS_ENEMYLOCATORS = 711
CS_INFECTED_SURVIVOR_MINSPEED = 712
CS_RACE_POINTS = 713
CS_MAX = 714

CS_STRING_MAP = {
    CS_SERVERINFO: "serverinfo",
    CS_SYSTEMINFO: "systeminfo",
    CS_MUSIC: "music",
    CS_MESSAGE: "message",
    CS_MOTD: "motd",
    CS_WARMUP: "warmup",               # server time when the match will be restarted
    CS_SCORES1: "scores1",
    CS_SCORES2: "scores2",
    CS_VOTE_TIME: "vote_time",
    CS_VOTE_STRING: "vote_string",
    CS_VOTE_YES: "vote_yes",
    CS_VOTE_NO: "vote_no",
    CS_GAME_VERSION: "game_version",
    CS_LEVEL_START_TIME: "level_start_time",
    CS_INTERMISSION: "intermission",
    CS_ITEMS: "items",
    CS_BOTINFO: "botinfo",
    CS_FLAGSTATUS: "flagstatus",
    CS_SCORES1PLAYER: "scores1player",
    CS_SCORES2PLAYER: "scores2player",
    CS_ROUND_WARMUP: "round_warmup",
    CS_ROUND_START_TIME: "round_start_time",
    CS_TEAMCOUNT_RED: "teamcount_red",
    CS_TEAMCOUNT_BLUE: "teamcount_blue",
    CS_SHADERSTATE: "shaderstate",
    CS_NEXTMAP: "nextmap",
    CS_PRACTICE: "practice",
    CS_FREECAM: "freecam",
    CS_PAUSE_START_TIME: "pause_start_time",
    CS_PAUSE_END_TIME: "pause_end_time",
    CS_TIMEOUTS_RED: "timeouts_red",
    CS_TIMEOUTS_BLUE: "timeouts_blue",
    CS_MODEL_OVERRIDE: "cs_model_override",
    CS_PLAYER_CYLINDERS: "player_cylinders",
    CS_DEBUGFLAGS: "debugflags",
    CS_ENABLEBREATH: "enablebreath",
    CS_TEAMLOCATORS: "teamlocators",
    CS_DMGTHROUGHDEPTH: "dmgthroughdepth",
    CS_AUTHOR: "author",
    CS_AUTHOR2: "author2",
    CS_ADVERT_DELAY: "advert_delauy",
    CS_PMOVEINFO: "pmoveinfo",
    CS_ARMORINFO: "armorinfo",
    CS_WEAPONINFO: "weaponinfo",
    CS_PLAYERINFO: "playerinfo",
    CS_1STPLAYER: "1stplayer",
    CS_2NDPLAYER: "2ndplayer",
    CS_SCORE1STPLAYER: "score1stplayer",
    CS_SCORE2NDPLAYER: "score2ndplayer",
    CS_ATMOSEFFECT: "atmoseffect",
    CS_MOST_DAMAGEDEALT_PLYR: "most_damagedealt_plyr",
    CS_MOST_ACCURATE_PLYR: "most_accurate_plyr",
    CS_REDTEAMNAME: "redteamname",
    CS_BLUETEAMNAME: "blueteamname",
    CS_REDTEAMCLANTAG: "redteamclantag",
    CS_BLUETEAMCLANTAG: "blueteamclantag",
    CS_BEST_ITEMCONTROL_PLYR: "best_itemcontrol_plyr",
    CS_SERVER_OWNER: "server_owner",
    CS_MOST_VALUABLE_OFFENSIVE_PLYR: "most_valuable_offensive_plyr",
    CS_MOST_VALUABLE_DEFENSIVE_PLYR: "most_valuable_deffensive_plyr",
    CS_MOST_VALUABLE_PLYR: "most_valuable_plyr",
    CS_GENERIC_COUNT_RED: "generic_count_red",
    CS_GENERIC_COUNT_BLUE: "generic_count_blue",
    CS_AD_SCORES: "cs_ad_scores",
    CS_ROUND_WINNER: "round_winner",
    CS_CUSTOM_SETTINGS: "cs_custom_settings",
    CS_ROTATIONMAPS: "rotationmaps",
    CS_ROTATIONVOTES: "rotationvotes",
    CS_DISABLE_VOTE_UI: "disable_vote_ui",
    CS_ALLREADY_TIME: "allready_time",
    CS_ENEMYLOCATORS: "enemylocators",
    CS_INFECTED_SURVIVOR_MINSPEED: "infected_survivor_minspeed",
    CS_RACE_POINTS: "race_points",
}

# WEAPONS
WP_NONE=0
WP_GAUNTLET=1
WP_MACHINEGUN=2
WP_SHOTGUN=3
WP_GRENADE_LAUNCHER=4
WP_ROCKET_LAUNCHER=5
WP_LIGHTNING=6
WP_RAILGUN=7
WP_PLASMAGUN=8
WP_BFG=9
WP_GRAPPLING_HOOK=10
WP_NAILGUN=11
WP_PROX_LAUNCHER=12
WP_CHAINGUN=13
WP_HANDS=14
WP_NUM_WEAPONS=15

WP_STRING_MAP = {
    WP_NONE: "none",
    WP_GAUNTLET: "gauntlet",
    WP_MACHINEGUN: "machinegun",
    WP_SHOTGUN: "shotgun",
    WP_GRENADE_LAUNCHER: "grenade_launcher",
    WP_ROCKET_LAUNCHER: "rocket_launcher",
    WP_LIGHTNING: "lightning",
    WP_RAILGUN: "railgun",
    WP_PLASMAGUN: "plasmagun",
    WP_BFG: "bfg",
    WP_GRAPPLING_HOOK: "grappling_hook",
    WP_HANDS: "hands",
}

userinfo_map={'c1': 'color1',
              'c2': 'color2',
              'tt': 'team_target',
              'hc': 'handicap',
              'c': 'country',
              'cn': 'clan',
              't': 'team',
              'xcn': 'extended_clan',
              'tl': 'team_leader'}

