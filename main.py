# Default imports
import arcade
import json
import os
import datetime

# Import Base Gate
from Gates.Gate.Gate import Gate

# Logger
class Logger:
	def clearFile(self):
		date = datetime.datetime.now()
		file = open(f"{date.day}{date.month}{date.year}.log", "w")
		file.write("")
		file.close()

	def log(self, *text):
		self.print("LOG", *text)

	def error(self, *text):
		self.print("ERROR", *text)

	def warn(self, *text):
		self.print("WARN", *text)

	def print(self, type, *text):
		date = datetime.datetime.now()
		file = open(f"{date.day}{date.month}{date.year}.log", "a")

		for i in text:
			i = str(i)
			file.write(f"[{'{:2.0f}'.format(date.hour)}:{'{:2.0f}'.format(date.minute)}:{'{:2.0f}'.format(date.second)} {type}]: {str(i)}\n")

		file.close()

# Mod
class Mod:
	def __init__(self, name, isGate, isPack, gates):
		self.name = name
		self.isGate = isGate
		self.isPack = isPack
		self.gates = gates
		self.selected = 0 if len(gates) else None
		self.selectedGate = self.gates[self.selected] if self.selected != None else None

	def rotate(self):
		if not self.isPack:
			return

		if self.selected < len(self.gates) - 1:
			self.selected += 1
		else:
			self.selected = 0

		self.selectedGate = self.gates[self.selected]

# Main class
class App(arcade.Window):
	def __init__(self, settings):
		# Объект логгер
		self.logger = Logger()
		self.logger.clearFile()
		self.logger.log("Запуск...")

		# Перерасчет размеров что бы сетка была ровной
		settings["width"] = (settings["width"] // settings["gridSize"]) * settings["gridSize"]
		settings["height"] = (settings["height"] // settings["gridSize"]) * settings["gridSize"]
		self.logger.log(f"Ширина: {settings['width']} | Высота: {settings['height']}")

		# Создание окна
		super().__init__(title=settings["title"], width=settings["width"], height=settings["height"])
		self.logger.log("Создание окна")

		# Объект содержащий все настройки
		self.settings = settings

		# Координаты ячейки на которую наведена мышь
		self.selectedCellX = -1
		self.selectedCellY = -1

		# Стандартная текстура которая заменяет все то что не загрузилось
		self.defaultTexturePath = "./Gates/Gate/texture.png"
		self.logger.log(f"Путь стандартной текстуры: {self.defaultTexturePath}")

		# Массив имен папок игноририуемых в ПАКЕ
		self.ignoreFoldersList = ["__pycache__"]
		self.logger.log(f"Игнорируемые папки в моде: {self.ignoreFoldersList}")

		# Массив имен модов игнорируемых при загрузке
		self.ignoreModList = ["Gate"] + self.settings["ignoremods"]
		self.logger.log(f"Игнорируемые моды: {self.ignoreModList}")

		# Папка в которой размещенны гейты
		self.modsFolder = "./Gates"
		self.logger.log(f"Папка с модами: {self.modsFolder}")

		# Массив размещенных гейтов
		self.gates = []

		# Выбранный мод, для перебода через таб
		self.selectedMod = None

		# Массив модов который перебирается при табе (Gate's / GatePack's)
		self.mods = []

		# Объект стандартной текстуры
		try:
			self.defaultTexture = arcade.load_texture(self.defaultTexturePath)
		except:
			self.logger.error("Не удалось загрузить стандартную текстуру. Запуск невозможен.")

		self.logger.log("Загрузка модов...")

		# Подгрузка всех модов
		self.loadMods()
		self.logger.log("Моды загружены")

	def createGate(self, Gate):
		free = True
		x = self.selectedCellX
		y = self.selectedCellY

		# Проверка, занята ли ячейка
		for gate in self.gates:
			if gate.cellX == x and gate.cellY == y:
				free = False
				break

		if free:
			try:
				gate = Gate(self.selectedCellX * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.selectedCellY * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.selectedCellX, self.selectedCellY)
			except:
				self.logger.error("При создании гейта произошла ошибка.")
				return

			self.gates.append(gate)
			#self.gates.sort(key=lambda x: int(x.root), reverse=True)

	def findGateByCellPos(self, x, y):
		for index, gate in enumerate(self.gates):
			if gate.cellX == x and gate.cellY == y:
				return (index, gate)

		return False

	def on_key_press(self, symbols: int, modificators):
		if symbols == 65289: # Tab - select gate
			if len(self.mods) > 0:
				if self.selectedMod == None:
					self.selectedMod = 0
				else:
					if self.selectedMod >= len(self.mods) - 1:
						self.selectedMod = None
					else:
						self.selectedMod += 1

		elif symbols == 119: # W - delete gate
			if gate := self.findGateByCellPos(self.selectedCellX, self.selectedCellY):
				self.gates.pop(gate[0])

		elif symbols == 114: # R - Rotate gate
			if self.selectedMod != None:
				self.mods[self.selectedMod].rotate()

	def on_update(self, dt):
		for gate in self.gates:
			try:
				if gate.root:
					gate.tick(self, dt)
			except:
				self.logger.error(f"Произошла ошибка в методе tick. Один из элементов цепи работает не правильно.")

	def on_mouse_press(self, x, y, button, modificators):
		if button == 1:
			if self.selectedMod != None:
				self.createGate(self.mods[self.selectedMod].selectedGate)

			else:
				if (gate := self.findGateByCellPos(self.selectedCellX, self.selectedCellY)):
					gate[1].mousePress(x, y, modificators)

	def on_mouse_motion(self, x, y, dx, dy):
		self.selectedCellX = x // self.settings["gridSize"]
		self.selectedCellY = y // self.settings["gridSize"]

	def getAllFilesFromFolder(self, path):
		return os.listdir(path)

	def loadMods(self):
		modNames = self.getAllFilesFromFolder(self.modsFolder)

		for modName in modNames:
			#try:
				if modName in self.ignoreModList:
					self.logger.log(f"Мод {modName} игнорируется при загрузке")
					continue

				modFiles = self.getAllFilesFromFolder(f"{self.modsFolder}/{modName}")

				gates = []
				if "main.py" in modFiles:
					isGate = True
					isPack = False

					try:
						module = __import__(f"{self.modsFolder[2:]}.{modName}.main")
					except:
						self.logger.error(f"При импорте мода {modName} произошла ошибка.")
						continue

					# Проверка на существование класса
					if not modName in module.__dict__[modName].main.__dict__:
						self.logger.error(f"Не найден класс {modName} мода {modName}.")
						continue

					modClass = module.__dict__[modName].main.__dict__[modName]

					texturePath = f"{self.modsFolder}/{modName}/texture.png"
					
					try:
						texture = arcade.load_texture(texturePath)
					except:
						if self.settings["usedefaulttexture"]:
							self.logger.warn(f"При загрузке текстуры гейта мода {modName} произошла ошибка. Будет использована стандартная текстура.")
						else:
							self.logger.error(f"При загрузке текстуры гейта мода {modName} произошла ошибка.")
							continue
						texture = self.defaultTexture

					modClass.texture = texture
					gates.append(modClass)

				else:
					isPack = True
					isGate = False
					gatesFolders = []
					for folder in modFiles:
						if folder.find(".") != -1:
							continue

						if folder in self.ignoreFoldersList:
							continue

						gatesFolders.append(folder)

					if len(gatesFolders) < 1:
						self.logger.error(f"При загрузке {modName} произошла ошибка. Папка с модом пуста.")
						continue
					
					for folder in gatesFolders:
						# Проверка есть ли main.py
						try:
							module = __import__(f"{self.modsFolder[2:]}.{modName}.{folder}.main")
						except ModuleNotFoundError:
							self.logger.error(f"В моде {modName} в гейте {folder} не найден main.py.")
							continue

						# Проверка на существование класса
						if not folder in module.__dict__[modName].__dict__[folder].main.__dict__:
							self.logger.error(f"Не найден класс {folder} в гейте {folder} мода {modName}.")
							continue	

						modClass = module.__dict__[modName].__dict__[folder].main.__dict__[folder]
						texturePath = f"{self.modsFolder}/{modName}/{folder}/texture.png"

						# Проверка наследования
						if not issubclass(modClass, Gate):
							if self.settings["checksubclass"]:
								self.logger.error(f"Гейт {folder} в моде {modName} не наследуется от стандартного гейта.")
								continue
							else:
								self.logger.warn(f"Гейт {folder} в моде {modName} не наследуется от стандартного гейта. Мод будет загружен, но стабильность работы не гарантируется.")

						# Подгрузка текстуры гейта
						try:
							texture = arcade.load_texture(texturePath)
						except FileNotFoundError:
							if self.settings["usedefaulttexture"]:
								self.logger.warn(f"Не найдена текстура гейта {folder} из мода {modName}. Будет использована стандартная текстура.")
								texture = self.defaultTexture
							else:
								self.logger.error(f"Не найдена текстура гейта {folder} из мода {modName}.")
								continue
						modClass.texture = texture

						# Добавляем гейт в массив гейтов мода
						gates.append(modClass)

				if len(gates) < 1:
					self.logger.error(f"В модe {modName} отсутсвуют гейты.")
					continue

				self.mods.append(Mod(modName, isGate, isPack, gates))
				self.logger.log(f"Мод {modName} успешно загружен.")

	def on_draw(self):
		# Очистка экрана
		self.clear()

		# Отрисовка сетки
		for y in range(1, self.height // self.settings["gridSize"]):
			arcade.draw_line(0, y * self.settings["gridSize"], self.width, y * self.settings["gridSize"], self.settings["colors"]["grid"])

		for x in range(1, self.width // self.settings["gridSize"]):
			arcade.draw_line(x * self.settings["gridSize"], 0, x * self.settings["gridSize"], self.height, self.settings["colors"]["grid"])

		# Отрисовка гейтов
		for gate in self.gates:
			gate.texture.draw_sized(gate.screenX, gate.screenY, self.settings["gridSize"] - 2, self.settings["gridSize"] - 2)
			gate.draw()

		# Подсветка гейта (ячейки) под мышью
		if self.selectedMod != None:
			if self.findGateByCellPos(self.selectedCellX, self.selectedCellY):
				arcade.draw_rectangle_filled(self.selectedCellX * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.selectedCellY * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.settings["gridSize"], self.settings["gridSize"], self.settings["colors"]["busy"])

			else:
				self.mods[self.selectedMod].selectedGate.texture.draw_sized(self.selectedCellX * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.selectedCellY * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.settings["gridSize"], self.settings["gridSize"])
				arcade.draw_rectangle_filled(self.selectedCellX * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.selectedCellY * self.settings["gridSize"] + self.settings["gridSize"] // 2, self.settings["gridSize"], self.settings["gridSize"], self.settings["colors"]["free"])

		else:
			arcade.draw_rectangle_filled(self.selectedCellX * self.settings["gridSize"]  + self.settings["gridSize"] // 2, self.selectedCellY * self.settings["gridSize"] +  self.settings["gridSize"] // 2, self.settings["gridSize"], self.settings["gridSize"], self.settings["colors"]["hovered"])

settings = {}

with open("settings.json", "r") as file:
	settings = json.loads(file.read())

main = App(settings)
main.run()