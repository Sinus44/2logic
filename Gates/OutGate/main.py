# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ..IndicatorGate.main import IndicatorGate
import arcade
import math

# Gate class
class OutGate(IndicatorGate):
	def __init__(self, *args):
		super().__init__(*args)
		self.root = True

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateLeft:
			if len(gateLeft[1].out["right"]):
				gateLeft[1].tick(parent, dt)
				self.indicator = gateLeft[1].out["right"][0]
			else:
				self.indicator = False
		else:
			self.indicator = False