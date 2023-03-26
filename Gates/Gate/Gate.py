# Check main
if __name__ == "__main__":
	print("Модификации не должны запускаться отдельно.")
	quit()

# Gate class
class Gate:
	texture = None

	def __init__(self, screenX, screenY, cellX, cellY):
		self.screenX = screenX
		self.screenY = screenY
		self.cellX = cellX
		self.cellY = cellY
		self.root = False

		self.out = {
			"right":[],
			"down": [],
			"left": [],
			"up": []
		}

	def draw(self):
		...

	def tick(self, parent, dt):
		...

	def mousePress(self, x, y, modificators):
		...

	def getNeighbour(self, parent):
		return (parent.findGateByCellPos(self.cellX + 1, self.cellY), parent.findGateByCellPos(self.cellX, self.cellY - 1), parent.findGateByCellPos(self.cellX - 1, self.cellY), parent.findGateByCellPos(self.cellX, self.cellY + 1))
