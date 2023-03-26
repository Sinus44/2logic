# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class URWireGate(Gate):
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
		if gateUp:
			gateUp[1].tick(parent, dt)
			self.out["right"][0] = gateUp[1].out["down"][0]
		else:
			self.out["right"][0] = False