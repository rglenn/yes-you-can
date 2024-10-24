#include <Adafruit_MCP2515.h>

Adafruit_MCP2515 mcp(A3);

int lastButtonState;
unsigned long lastDebounce;
unsigned long debounceDelay = 50;

#define buttonPin 7

void setup() {
	Serial.begin(115200);

	if (!mcp.begin(250000)) {
		Serial.println("Error initializing MCP2515.");
		while(1) delay(10);
	}
	Serial.println("MCP2515 initialized");
	pinMode(buttonPin, INPUT_PULLUP);
	lastButtonState = digitalRead(buttonPin);
}

void loop() {
	int buttonState = digitalRead(buttonPin);

	if (buttonState != lastButtonState)
	{
		lastDebounce = millis();
	}

	if ((millis() - lastDebounce) > debounceDelay)
	{
		if (lastButtonState != buttonState)
		{
			lastButtonState = buttonState;
			mcp.beginPacket(0x200);
			mcp.write(buttonState ? 0 : 1);
			if (mcp.endPacket()) 
			{
				Serial.printf("Sent successfully, button state %d\n", buttonState);
			}
			else
			{
				Serial.printf("Failed to send, button state %d\n", buttonState);
			}
		}
	}
}
