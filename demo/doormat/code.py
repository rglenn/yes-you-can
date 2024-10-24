import struct
import board
import canio
import digitalio
import neopixel

# Written for an ESP32-S3 Feather with a CAN Pal connected, CAN TX on MCU TX and CAN RX on MCU RX

doormat = digitalio.DigitalInOut(board.A1)
doormat.pull = digitalio.Pull.UP
doormat.direction = digitalio.Direction.INPUT

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

can = canio.CAN(rx=board.RX, tx=board.TX, baudrate=250_000, auto_restart=True)
listener = can.listen(timeout=.9)

while True:
    message = listener.receive()
    if message is None:
        print("No messsage received within timeout")
        continue

    if type(message) is canio.RemoteTransmissionRequest:
        if message.id == 0x201:
            # request for status of doormat
            transmitState = 0
            if (!doormat.value):
                transmitState = 1
                message = canio.Message(id=0x201, data=struct.pack("<B", transmitState))
                can.send(message)
    elif type(message) is canio.Message:
        if message.id == 0x202:
            # play LED animation
            data = message.data
            if len(data) != 1:
                print(f"Unusual message length {len(data)}")
                continue
            ledMode = struct.unpack("<B", data)
            if ledMode == 1:
                print("Got LED animation 1 command")
                pixel.fill((255, 255, 255))
                time.sleep(0.25)
                pixel.fill((0, 0, 0))