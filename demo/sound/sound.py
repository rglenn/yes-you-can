import socket, sys, struct
import pygame

pygame.init()
thunder_sound = pygame.mixer.Sound("thunder.wav")

sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
interface = "can0"
try:
    sock.bind((interface,))
except OSError:
    sys.stderr.write("Could not bind to interface '%s'\n" % interface)
    exit(0)

can_fmt = "<IB3x8s"

while True:
    can_pkt = sock.recv(16)
    can_id, length, data = struct.unpack("<IB3x8s", can_pkt)
    can_id &= socket.CAN_EFF_MASK
    data = data[:length]

    if (can_id == 0x203) and (data[0] == 0x01):
        # play sound effect
        print("Playing sound effect")
        pygame.mixer.Sound.play(thunder_sound)