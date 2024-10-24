import time
import board
import digitalio
import canio
from adafruit_mcp2515 import MCP2515 as CAN

# Written for an RP2040 CAN Feather

cs = digitalio.DigitalInOut(board.CAN_CS)
cs.switch_to_output()
spi = board.SPI()

can_bus = CAN(
    spi, cs, loopback=False
)

buttonState = 0
ledLightningAnimation = 1
soundThunder = 1

while True:
    message = listener.receive()
    if message is None:
        print("No messsage received within timeout")
        continue

    if isinstance(msg, canio.Message):
        data = message.data
        if message.id == 0x200:
            if len(data) != 1:
                print(f"Unusual message length for 0x200 {len(data)}")
                continue
            buttonState = struct.unpack("<B", data)
            if buttonState = 1:
                print("Button pushed")
                request = canio.RemoteTransmissionRequest(id=0x201)
                can.send(request)
         elif message.id == 0x201:
            if len(data) != 1:
                print(f"Unusual message length for 0x201 {len(data)}")
                continue
            doormatState = struct.unpack("<B", data)
            if (doormatState == 1) and (buttonState = 1):
                print("Doorbell is pushed and doormat is squished")
                # button pushed while on pad
                lightningMessage = canio.Message(id=0x202, data=struct.pack("<B", ledLightningAnimation))
                can.send(lightningMessage)
                thunderMessage = canio.Message(id=0x203, data=struct.pack("<B", soundThunder))
                can.send(thunderMessage)