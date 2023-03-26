# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ..Gate.Gate import Gate
import arcade

# Gate class
class IndicatorGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.indicator = False
		self.indicatorRadius = 10

	def draw(self):
		if self.indicator:
			arcade.draw_circle_filled(self.screenX, self.screenY - self.indicatorRadius * 2, self.indicatorRadius, (0, 255, 0))
		else:
			arcade.draw_circle_filled(self.screenX, self.screenY - self.indicatorRadius * 2, self.indicatorRadius, (255, 0, 0))

