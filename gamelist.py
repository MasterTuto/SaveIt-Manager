import re
from libs import iso9660
import os


class GameList(list):
	"""docstring for GameList"""
	def __init__(self, path):
		self.path = path
		
		os.chdir(path)


	def get_games(self, has_dvd, has_ul, has_cd):
		games = []

		if has_ul:
			ulgames = self.__get_ul_games()
			games.extend(ulgames)
		
		if has_cd:
			cdgames, err_games = self.__get_cd_games()
			games.extend(cdgames)
		
		if has_dvd:
			dvdgames, err_games = self.__get_dvd_games()
			games.extend(dvdgames)

		return games, err_games

	def __get_dvd_games(self):
		os.chdir(self.path)

		dvd_folder = os.listdir("DVD")

		games, err_games = [], []

		pattern = r"^(\w{4,4}_[0-9]{3,3}\.[0-9]{2,2})\.(.+)\.iso$"
		for game in dvd_folder:
			new_format = re.match(pattern, game, re.IGNORECASE) # Check if matches the new format game -> "SLUS_222.33.GAME NAME.iso"
			
			if new_format:
				game2add = {
					"nome":   new_format.group(2),
					"codigo": new_format.group(1)
				}
				games.append(game2add)
			else:
				if game.lower().endswith("iso"):
					try:
						arq_game = iso9660.ISO9660("DVD\\"+game) # Opens the game that hasn't the right format
						systemcnf = arq_game.get_file("SYSTEM.CNF")

						pattern2 = r"\\(.+);"
						codigo = re.search(pattern2, systemcnf).group(1) # Looks for ELF file inside SYSTEM.CNF
						nome   = join(game.split(".")[:-1]) # Take the game name

						game2add = {
							"nome": nome,
							"codigo": codigo
						}

					except Exception as e:
						err_games.append(game)

		return games, err_games


	def __get_cd_games(self):
		os.chdir(self.path)

		dvd_folder = os.listdir("CD")

		games, err_games = [], []

		pattern = r"^(\w{4,4}_[0-9]{3,3}\.[0-9]{2,2})\.(.+)\.iso$"
		for game in dvd_folder:
			new_format = re.match(pattern, game, re.IGNORECASE) # Check if matches the new format game -> "SLUS_222.33.GAME NAME.iso"
			
			if new_format:
				game2add = {
					"nome":   new_format.group(2),
					"codigo": new_format.group(1)
				}
				games.append(game2add)
			else:
				if game.lower().endswith("iso"):
					try:
						arq_game = iso9660.ISO9660("CD\\"+game) # Opens the game that hasn't the right format
						systemcnf = arq_game.get_file("SYSTEM.CNF")

						pattern2 = r"\\(.+);"
						codigo = re.search(pattern2, systemcnf).group(1) # Looks for ELF file inside SYSTEM.CNF
						nome   = join(game.split(".")[:-1]) # Take the game name

						game2add = {
							"nome": nome,
							"codigo": codigo
						}

					except Exception as e:
						err_games.append(game)

		return games, err_games


	def __get_ul_games(self):
		ulcfg_file = open("ul.cfg", "rb")

		ulgames = []

		try:
			split_str = "\x00\x05\x14\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
			games = ulcfg_file.read().split(split_str)

			for game in games[:-1]:
				game = game.replace("\x00", '') # remove \x00 from each game
				g_data = game.split("ul.") # split it by "ul." since it is useless to us

				game = {
					"nome":   g_data[0],
					"codigo": g_data[1]
				}

				ulgames.append(game)

			ulcfg_file.close()
		
		except Exception as e:
			ulcfg_file.close()
			raise e

		return ulgames


		
if __name__ == '__main__':
	games = GameList("I:/PS2USB")
	games, err_games = games.get_games()

	games.sort(key=lambda k: k['nome'])
