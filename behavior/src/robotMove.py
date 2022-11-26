import robotop as op
from gtts import gTTS 
from pydub import AudioSegment
import time
import random as rnd

def axes(IP, PORT):
    axes = op.read_axes(IP, PORT)
    print(axes)
    time.sleep(2)

def timeSleep(d):
    if d < 2:
        time.sleep(2)
    else:
        time.sleep(d)

def leftRaise(IP:str, PORT:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=100, L_EYE_B=100, 
            R_EYE_R=255, R_EYE_G=100, R_EYE_B=100)
    servo_map = dict(L_SHOU=-70)
    pose = dict(Msec=500, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)

def rightRaise(IP:str, PORT:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=100, L_EYE_B=100, 
            R_EYE_R=255, R_EYE_G=100, R_EYE_B=100)
    servo_map = dict(R_SHOU=-70)
    pose = dict(Msec=500, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)

def bothRaise(IP:str, PORT:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=100, L_EYE_B=100, 
            R_EYE_R=255, R_EYE_G=100, R_EYE_B=100)
    servo_map = dict(R_SHOU=-70, L_SHOU=70, R_ELBO=0, L_ELBO=0, HEAD_P=-10, HEAD_Y=0, BODY_Y=0)
    pose = dict(Msec=500, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)

def pointing(IP:str, PORT:int):
    led_map = dict(L_EYE_R=100, L_EYE_G=0, L_EYE_B=100, 
            R_EYE_R=100, R_EYE_G=0, R_EYE_B=100)
    servo_map = dict(R_ELBO=0, R_SHOU = 0, L_SHOU = -90)
    pose = dict(Msec=250, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)

def hi(IP:str, PORT:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=100, L_EYE_B=100, 
            R_EYE_R=255, R_EYE_G=100, R_EYE_B=100)
    motion = [
        dict(Msec=500, ServoMap=dict(R_SHOU=-90, L_SHOU =-90, R_ELBO=0, L_ELBO=0, HEAD_P=0, HEAD_Y=0, BODY_Y=0, HEAD_R=5), LedMap=led_map),
        dict(Msec=250, ServoMap=dict(R_ELBO=40)),
        dict(Msec=250, ServoMap=dict(R_ELBO=-60)),
        dict(Msec=250, ServoMap=dict(R_ELBO=40)),
        dict(Msec=250, ServoMap=dict(R_ELBO=-60))
    ]
    op.play_motion(IP, PORT, motion)

def nod(IP:str, PORT:int):
    led_map = dict(L_EYE_R=100, L_EYE_G=100, L_EYE_B=255, 
            R_EYE_R=100, R_EYE_G=100, R_EYE_B=255)
    motion = [
    dict(Msec=250, ServoMap=dict(R_SHOU=105,HEAD_P=-15,R_ELBO=0, L_ELBO=-3, L_SHOU=-102, HEAD_Y=0, BODY_Y=0, HEAD_R=0), LedMap=led_map),
    dict(Msec=250, ServoMap=dict(R_SHOU=77, HEAD_P=20, R_ELBO=17,L_ELBO=-17,L_SHOU=-79 )),
    dict(Msec=250, ServoMap=dict(R_SHOU=92, HEAD_P=0, R_ELBO=5, L_ELBO=-7, L_SHOU=-88 ))
    ]
    op.play_motion(IP, PORT, motion)

def shakeHead(IP, PORT):
    led_map = dict(L_EYE_R=255, L_EYE_G=0, L_EYE_B=0, 
            R_EYE_R=255, R_EYE_G=0, R_EYE_B=0)
    motion = [
    dict(Msec=250, ServoMap=dict(R_SHOU=105,HEAD_P=-5, HEAD_Y=20, R_ELBO=0, L_ELBO=-3, L_SHOU=-102, HEAD_R = 0), LedMap=led_map),
    dict(Msec=250, ServoMap=dict(HEAD_Y=-20)),
    dict(Msec=250, ServoMap=dict(HEAD_Y=20)),
    dict(Msec=250, ServoMap=dict(HEAD_Y=-20))
    ]
    op.play_motion(IP, PORT, motion)

def tiltHead(IP:str, PORT:int):
    led_map = dict(L_EYE_R=100, L_EYE_G=0, L_EYE_B=100, 
            R_EYE_R=100, R_EYE_G=0, R_EYE_B=100)
    pose = dict(Msec=250, ServoMap=dict(HEAD_R=10, HEAD_P=-5, HEAD_Y=0, BODY_Y=0,
                L_SHOU=-90, L_ELBO=0, R_SHOU=-20, R_ELBO=90), LedMap=led_map)
    op.play_pose(IP, PORT, pose)

def Isee(IP:str, PORT:int):
    led_map = dict(L_EYE_R=100, L_EYE_G=100, L_EYE_B=255, 
            R_EYE_R=100, R_EYE_G=100, R_EYE_B=255)
    motion = [
    dict(Msec=250, ServoMap=dict(R_SHOU=-10,R_ELBO=90, L_ELBO=-90, L_SHOU=-35, HEAD_R=0, HEAD_P=-5, HEAD_Y=0, BODY_Y=0), LedMap=led_map),
    dict(Msec=250, ServoMap=dict(R_SHOU=20)),
    dict(Msec=250, ServoMap=dict(R_SHOU=-10))
    ]
    op.play_motion(IP, PORT, motion)


def sad(IP:str, PORT:int):
    led_map = dict(L_EYE_R=0, L_EYE_G=0, L_EYE_B=255, 
            R_EYE_R=0, R_EYE_G=0, R_EYE_B=255)
    servo_map = dict(HEAD_R=0, HEAD_P=15, HEAD_Y=0, BODY_Y=0, 
                L_SHOU=-95, L_ELBO=0, R_SHOU=95, R_ELBO=0)
    pose = dict(Msec=1000, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)
    time.sleep(1)

def fight(ip:str, port:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=0, L_EYE_B=0, 
            R_EYE_R=255, R_EYE_G=0, R_EYE_B=0)
    motion = [
    dict(Msec=700, ServoMap=dict(R_SHOU=-80,R_ELBO=0, L_ELBO=-80, L_SHOU=-10, HEAD_R=0, HEAD_P=-5, HEAD_Y=0, BODY_Y=0), LedMap=led_map),
    dict(Msec=700, ServoMap=dict(R_SHOU=-10, R_ELBO=80, L_ELBO=0, L_SHOU=80)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-80, R_ELBO=0, L_ELBO=-80, L_SHOU=-10)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-10, R_ELBO=80, L_ELBO=0, L_SHOU=80)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-80, R_ELBO=0, L_ELBO=-80, L_SHOU=-10)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-10, R_ELBO=80, L_ELBO=0, L_SHOU=80)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-80, R_ELBO=0, L_ELBO=-80, L_SHOU=-10)),
    dict(Msec=700, ServoMap=dict(R_SHOU=-10, R_ELBO=80, L_ELBO=0, L_SHOU=80))
    ]
    op.play_motion(ip, port, motion)

def reset(IP:str, PORT:int):
    led_map = dict(L_EYE_R=255, L_EYE_G=255, L_EYE_B=255, 
            R_EYE_R=255, R_EYE_G=255, R_EYE_B=255)
    servo_map = dict(HEAD_R=0, HEAD_P=-5, HEAD_Y=0, BODY_Y=0, 
                L_SHOU=-90, L_ELBO=0, R_SHOU=90, R_ELBO=0)
    pose = dict(Msec=250, ServoMap=servo_map, LedMap=led_map)
    op.play_pose(IP, PORT, pose)
    time.sleep(0.25)

def randomMove(ip:str, port:int):
    movings = [
        "leftRaise(ip, port)", 
        "rightRaise(ip, port)", 
        "bothRaise(ip, port)", 
        "pointing(ip, port)", 
        "nod(ip, port)", 
        "Isee(ip, port)"
        ]
    n = rnd.randint(0, len(movings) - 1)
    eval(movings[n])
    
