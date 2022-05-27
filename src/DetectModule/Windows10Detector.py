from src.DetectModule.Detector import Detector


class Windows10Detector(Detector):
	def detect(self):
		result = False
		fileName = self.path + '/Windows/System32/config/SYSTEM'
		with open(fileName, mode='rb') as file:
			fileContent = file.read()
			result = fileContent.find(b'FileHistory') != -1

		return "This windows {} FileHistory option".format("has" if result else "hasn't")