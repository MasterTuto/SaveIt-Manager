# coding: UTF-8
import wx
import gamelist
import os

class App(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(600, 480), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		# Window Parent
		panel = wx.Panel(self, wx.ID_ANY)
		self.CreateStatusBar() # Cria barra de status

		# Complete MenuBar config
		file_menu = wx.Menu()

		openfolder = file_menu.Append(wx.ID_ANY, "Abrir Pasta", "Escolhe uma pasta para ser aberta")
		file_menu.AppendSeparator()
		closeapp = file_menu.Append(wx.ID_ANY, "Fechar", "Fecha aplicativo")


		menubar = wx.MenuBar()
		menubar.Append(file_menu, "File")
		self.SetMenuBar(menubar)
		
		# List and columns
		self.opcoes = wx.ListCtrl(panel, size=(350, 400),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         )
		self.opcoes.InsertColumn(0, "NOME", width=200)
		self.opcoes.InsertColumn(1, "CÓDIGO", width=80)
		
		# Inner BoxSizer
		topbox = wx.BoxSizer(wx.VERTICAL)
		topbox.Add(self.opcoes, 0, wx.ALL|wx.EXPAND, 5)

		# Outer BoxSizer
		rightbox = wx.BoxSizer(wx.HORIZONTAL)
		rightbox.Add(topbox, 0, wx.EXPAND, 5)
		panel.SetSizer(rightbox)

		# Binds
		self.Bind(wx.EVT_MENU, self.open_folder, openfolder) # "Open Folder" on menu bar
		self.Bind(wx.EVT_MENU, self.__CloseApp, closeapp) # "Open Folder" on menu bar

		self.Show()

	def open_folder(self, event=None):
		f_diag = wx.DirDialog(self)
		f_diag.SetMessage("""Escolha a pasta do que contenha as "CD", "DVD", etc.""")
		f_diag.ShowModal()

		self.__fill_listctrl(folder=f_diag.GetPath())


	def __CloseApp(self, event=None):
		self.Close()


	def __fill_listctrl(self, event=None, folder=''):
		if folder == '':
			self.__show_message("Nenhuma pasta selecionada!")
			return None

		arqs = os.listdir(folder)
		if not any([c in arqs for c in ["CD", "DVD", "ul.cfg"]]):
			return self.open_folder()

		has_dvd = True if 'DVD' in arqs else False
		has_ul  = True if 'ul.cfg' in arqs else False
		has_cd  = True if 'CD' in arqs else False

		games = gamelist.GameList(folder)
		games, err_games = games.get_games(has_dvd, has_ul, has_cd)

		if (len(err_games) > 0):
			self.__show_message("%d jogos foram ilegiveis" % len(err_games))

		if (len(games) == 0):
			self.__show_message("Nenhum jogo foi entregado.")

		games.sort(key=lambda k: k['nome'], reverse=True)

		for game in games:
			self.nome   = game['nome']
			self.codigo = game["codigo"]
			self.__add_line()


	def __add_line(self, event=None):
		self.opcoes.InsertItem(0, self.nome)
		self.opcoes.SetItem(0, 1, self.codigo)


	def __show_message(self, texto):
		dlg = wx.MessageDialog(self, texto, "Aviso")
		dlg.ShowModal()
		dlg.Destroy()

if __name__ == '__main__':
	app = wx.App(False)
	jnl = App(None, "SaveIt! Manager - PS2 Saves")
	app.MainLoop()

