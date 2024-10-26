import time
import board
import digitalio
import struct
from adafruit_mcp2515 import canio as canio
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
    with can_bus.listen(timeout=1.0) as listener:
        message = listener.receive()
        if message is None:
            print("No messsage received within timeout")
            continue

        #message can be a Message or a RemoteTransmissionRequest, figure out which
        if isinstance(message, canio.Message):
            data = message.data
            #message with ID 0x200 is a button state, process it
            if message.id == 0x200:
                if len(data) != 1:
                    print(f"Unusual message length for 0x200 {len(data)}")
                    continue
                buttonState = struct.unpack("<B", data)
                if buttonState[0] == 1:
                    print("Button pushed")
                    request = canio.RemoteTransmissionRequest(id=0x201, length=0)
                    can_bus.send(request)
            #message with ID 0x201 is a doormat state, process it
            elif message.id == 0x201:
                if len(data) != 1:
                    print(f"Unusual message length for 0x201 {len(data)}")
                    continue
                doormatState = struct.unpack("<B", data)
                if (doormatState[0] == 1) and (buttonState[0] == 1):
                    print("Doorbell is pushed and doormat is squished")
                    # button pushed while on pad
                    lightningMessage = canio.Message(id=0x202, data=struct.pack("<B", ledLightningAnimation))
                    can_bus.send(lightningMessage)
                    thunderMessage = canio.Message(id=0x203, data=struct.pack("<B", soundThunder))
                    can_bus.send(thunderMessage)