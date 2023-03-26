# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class XorGate(Gate):	
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

		if gateLeft:
			gateLeft[1].tick(parent, dt)
			if len(gateLeft[1].out["right"]) > 1:
				self.out["right"][0] = gateLeft[1].out["right"][0] != gateLeft[1].out["right"][1]

		else:
			self.out["right"][0] = False