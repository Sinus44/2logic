# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class LUWireGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [],
			"down": [],
			"left": [],
			"up": [False]
		}

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateLeft:
			gateLeft[1].tick(parent, dt)
			self.out["up"][0] = gateLeft[1].out["right"][0]
		else:
			self.out["up"][0] = False