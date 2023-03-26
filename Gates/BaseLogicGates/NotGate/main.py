# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class NotGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [True],
			"down": [],
			"left": [],
			"up": []
		}

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateLeft:
			gateLeft[1].tick(parent, dt)
			self.out["right"][0] = not gateLeft[1].out["right"][0]
		else:
			self.out["right"][0] = True