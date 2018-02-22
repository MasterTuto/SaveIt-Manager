# coding: utf-8
import re
import os

class CFG(object):
	has_cfg = True
	def __init__(self, path='', game_id=''):
		if path == '':
			return None
		path = path.strip("\\")
		game_cfg = path + "\\CFG\\" + game_id + ".cfg"

		self.absolute_cfg_path = game_cfg

		# Verify if "CFG" folder exists inside the given path
		if "CFG" not in os.listdir(path):
			os.mkdir("CFG")


		# Verify if the cfg of the game is inside path
		if game_id + ".cfg" not in os.listdir(path+"\\CFG"):
			self.has_cfg = False
			with open(game_cfg, "wb") as game:
				game.write("CfgVersion=3")
		else:
			self.has_cfg = True

		with open(game_cfg, "rb") as game:
			self.cfg_file = game.read()

	def get_vmc_file(self):
		pattern = r"\$VMC_0=(.+)"
		
		try:
			vmc_file = re.search(pattern, self.cfg_file).group(1)
		except:
			return False
		
		return str(vmc_file)

	def set_vmc_file(self, new_vmc_file):
		new_vmc_file = new_vmc_file.split("\\")

		if not isinstance(new_vmc_file, list):
			new_vmc_file = new_vmc_file.split("/")

		new_vmc_file = new_vmc_file[-1][:-4]

		# In case user cancels open vmc operation, new_vmc_file is equal to ''

		# If there's a set VMC_0 file, it will delete it
		if new_vmc_file == '' and "$VMC_0=" in self.cfg_file:
			old_vmc_file = re.search(r"(\$VMC_0=(.+))", self.cfg_file).group(1)
			new_cfg_file = self.cfg_file.decode("utf-8").replace(old_vmc_file, '')

			with open(self.absolute_cfg_path, 'wb') as cfg_file:
				cfg_file.write(new_cfg_file.encode("utf-8"))

			return
		# Otherwise, it will leave it as it is
		elif new_vmc_file == '' and '$VMC_0' not in self.cfg_file:
			return

		


		if "$VMC_0=" not in self.cfg_file:
			new_cfg_file = self.cfg_file.decode("utf-8").strip() + "\r\n$VMC_0=" + new_vmc_file
		else:
			old_vmc_file = re.search(r"\$VMC_0=(.+)", self.cfg_file.decode("utf-8")).group(1)
			new_cfg_file = self.cfg_file.decode("utf-8").replace(old_vmc_file, new_vmc_file)

		with open(self.absolute_cfg_path, 'w') as cfg_file:
			cfg_file.write(new_cfg_file.encode("utf-8"))

if __name__ == '__main__':
	c = CFG("F:\\PS2USB", "SLUS_216.64")

	c.set_vmc_file("Bakugam")