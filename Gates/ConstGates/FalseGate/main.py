# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class FalseGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [False],
			"down": [],
			"left": [],
			"up": []
		}