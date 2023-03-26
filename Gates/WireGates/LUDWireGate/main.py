# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class LUDWireGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [],
			"down": [False],
			"left": [],
			"up": [False]
		}

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateLeft:
			gateLeft[1].tick(parent, dt)
			self.out["down"][0] = gateLeft[1].out["right"][0]
			self.out["up"][0] = gateLeft[1].out["right"][0]
		else:
			self.out["down"][0] = False
			self.out["up"][0] = False