# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ..Gate.Gate import Gate

# Gate class
class JoinGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [False, False],
			"down": [],
			"left": [],
			"up": []
		}

	def tick(self, parent, dt):
		gateRight, gateDown, gateLeft, gateUp = self.getNeighbour(parent)
		if gateUp:
			gateUp[1].tick(parent, dt)
			if len(gateUp[1].out["down"]) > 0:
				self.out["right"][0] = gateUp[1].out["down"][0]
		else:
			self.out["right"][0] = False

		if gateDown:
			gateDown[1].tick(parent, dt)
			if len(gateDown[1].out["up"]) > 0:
				self.out["right"][1] = gateDown[1].out["up"][0]
		else:
			self.out["right"][1] = False
