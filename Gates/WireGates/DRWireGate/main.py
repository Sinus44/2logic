# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class DRWireGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [False],
			"down": [],
			"left": [],
			"up": []
		}

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateDown:
			gateDown[1].tick(parent, dt)
			self.out["right"][0] = gateDown[1].out["up"][0]
		else:
			self.out["right"][0] = False