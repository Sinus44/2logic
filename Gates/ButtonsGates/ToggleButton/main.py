# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...IndicatorGate.main import IndicatorGate

# Gate class
class ToggleButton(IndicatorGate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [False],
			"down": [],
			"left": [],
			"up": []
		}
		self.root = False

	def mousePress(self, x, y, modificators):
		self.out["right"][0] = not self.out["right"][0]
		self.updateIndicator()

	def updateIndicator(self):
		self.indicator = self.out["right"][0]