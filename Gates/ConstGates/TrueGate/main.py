# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Import default
from ...Gate.Gate import Gate

# Gate class
class TrueGate(Gate):
	def __init__(self, *args):
		super().__init__(*args)
		self.out = {
			"right": [True],
			"down": [],
			"left": [],
			"up": []
		}