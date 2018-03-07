# coding: UTF-8
import wx
import gamelist
import os
import utils
import libs.mymc.ps2mc as ps2mc

class App(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(700, 480), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		# Window Parent
		panel = wx.Panel(self, wx.ID_ANY)
		self.panel = panel
		self.CreateStatusBar() # Cria barra de status

		# **** START MENUBAR ****
		file_menu = wx.Menu()

		openfolder = file_menu.Append(wx.ID_ANY, "Abrir Pasta", "Escolhe uma pasta para ser aberta")
		file_menu.AppendSeparator()
		closeapp = file_menu.Append(wx.ID_ANY, "Fechar", "Fecha aplicativo")


		menubar = wx.MenuBar()
		menubar.Append(file_menu, "Arquivo")
		self.SetMenuBar(menubar)
		# **** END MENUBAR ****
		
		# COLUMS
		self.opcoes = wx.ListCtrl(panel, size=(350, 400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
		self.opcoes.InsertColumn(0, "NOME", width=200)
		self.opcoes.InsertColumn(1, "CÓDIGO", width=80)

		# **** GAME DATA WIDGETS ****

		# NAME'S BOX
		nome_box = wx.BoxSizer(wx.HORIZONTAL)
		txt_nome = wx.StaticText(panel, label="Nome:               ")
		self.rel_nome = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(200, 20))
		nome_box.Add(txt_nome)
		nome_box.Add(self.rel_nome)

		# GAME ID'S BOX
		id_box = wx.BoxSizer(wx.HORIZONTAL)
		txt_id = wx.StaticText(panel, label="Código:             ")
		self.codigo = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(200, 20))
		id_box.Add(txt_id)
		id_box.Add(self.codigo)

		# CFG'S BOX
		cfg_box = wx.BoxSizer(wx.HORIZONTAL)
		txt_cfg = wx.StaticText(panel, label="Arquivo CFG:    ")
		self.cfg = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(200, 20))
		cfg_box.Add(txt_cfg)
		cfg_box.Add(self.cfg)

		# VMC BOX
		vmc_box = wx.BoxSizer(wx.HORIZONTAL)
		txt_vmc = wx.StaticText(panel, label="Arquivo VMC:   ")
		self.vmc = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(200, 20))
		vmc_changing = wx.Button(panel, label="Mudar", size=(100, 23))
		vmc_box.Add(txt_vmc)
		vmc_box.Add(self.vmc)
		vmc_box.Add(vmc_changing)

		# VMC CONTENT BOX
		vmc_content_box  = wx.BoxSizer(wx.VERTICAL)
		
		self.vmc_content_list = wx.ListCtrl(panel, size=(325, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
		self.vmc_content_list.InsertColumn(0, "Nome", width=200)
		self.vmc_content_list.InsertColumn(1, "Tamanho", width=200)

		self.vmc_content_btn  = wx.Button(panel, label="Carregar VMC", size=(130, 25))
		self.vmc_content_btn.Disable()
		vmc_content_box.Add(self.vmc_content_list)
		vmc_content_box.AddSpacer(3)
		vmc_content_box.Add(self.vmc_content_btn, 0, wx.ALIGN_CENTER)

		# MAIN BOX
		data_box = wx.BoxSizer(wx.VERTICAL)
		
		data_box.Add(nome_box, 0, wx.EXPAND)
		data_box.AddSpacer(10) # Add space
		data_box.Add(id_box, 0)
		data_box.AddSpacer(10) # Add space
		data_box.Add(cfg_box, 0)
		data_box.AddSpacer(10) # Add space
		data_box.Add(vmc_box, 0)
		data_box.AddSpacer(10) # Add space
		data_box.Add(vmc_content_box, 0)

		# **** GAME DATA WIDGETS ****

		janela = wx.BoxSizer(wx.HORIZONTAL)
		janela.Add(self.opcoes)
		janela.Add(wx.StaticText(panel, label="   "))
		janela.Add(data_box)
		
		# Binds
		self.Bind(wx.EVT_MENU, self.open_folder, openfolder) # "Open Folder" on menu bar
		self.Bind(wx.EVT_MENU, self.__CloseApp, closeapp) # "Open Folder" on menu bar
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.__show_data, self.opcoes) # Focused item in the list
		self.Bind(wx.EVT_BUTTON, self.__change_vmc, vmc_changing) # VMC Changing button
		self.Bind(wx.EVT_BUTTON, self._fill_vmc_content, self.vmc_content_btn)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click, self.vmc_content_list)

		self.SetSizer(janela)
		self.Show()

	def open_folder(self, event=None):
		f_diag = wx.DirDialog(self)
		f_diag.SetMessage("""Escolha a pasta do que contenha as "CD", "DVD", etc.""")
		f_diag.ShowModal()

		self.def_path = f_diag.GetPath()

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

		self.opcoes.DeleteAllItems() # Empty the ListCtrl object ger around another folder opening appending

		has_dvd = True if 'DVD' in arqs else False    # Check if it has "DVD" folder inside given path
		has_ul  = True if 'ul.cfg' in arqs else False # Check if it has "ul.cfg" file inside given path
		has_cd  = True if 'CD' in arqs else False     # Check if it has "CD" folder inside given path

		self.folder = folder
		games = gamelist.GameList(folder)
		games, err_games = games.get_games(has_dvd, has_ul, has_cd)

		if (len(err_games) > 0):
			self.__show_message("%d jogos foram ilegiveis, veja nomes do arquivo de log:\nsaveit-log.txt" % len(err_games))

		with open("saveit-log.txt", "w") as log:
			log.write('\n'.join(err_games))

		if (len(games) == 0):
			self.__show_message("Nenhum jogo foi encontrado.")
	
		games.sort(key=lambda k: k['nome'], reverse=True)

		self.games =  games

		for game in games:
			nome   = game['nome']
			codigo = game['codigo']
			self.__add_line(self.opcoes, [nome, codigo])

	def __add_line(self, obj, items):
		obj.InsertItem(0, items[0])
		obj.SetItem(0, 1, items[1])

	def __show_message(self, texto):
		dlg = wx.MessageDialog(self, texto, "Aviso")
		dlg.ShowModal()
		dlg.Destroy()

	def __show_data(self, event=''):
		self.vmc_content_list.DeleteAllItems()
		jogos = list(reversed(self.games))
		self.rel_nome.SetValue(jogos[event.GetIndex()]["nome"])
		self.codigo.SetValue(jogos[event.GetIndex()]["codigo"])

		self.game_data = event

		vmc_name = utils.CFG(self.folder, jogos[event.GetIndex()]["codigo"])
		vmc_file = vmc_name.get_vmc_file()

		if not vmc_file:
			self.vmc_content_btn.Disable()
			self.vmc.SetValue("**Nenhum arquivo**")
		else:
			self.vmc_content_btn.Enable()
			self.vmc.SetValue(str(vmc_name.get_vmc_file()) + ".bin")
			self.global_vmc_name = self.folder.strip("\\") + "\\VMC\\" + vmc_file + ".bin"


		cfg_file = jogos[event.GetIndex()]["codigo"] + ".cfg"
		self.cfg.SetValue(cfg_file)

	def __change_vmc(self, event):
		jogos = list(reversed(self.games))
		focused_game = self.opcoes.GetFocusedItem()
		game_cfg = utils.CFG(self.folder, jogos[focused_game]["codigo"])

		vmc_open = wx.FileDialog(self, wildcard="VMC File (*.bin)|*.bin")
		vmc_open.SetMessage("Abra um arquivo *.bin")
		vmc_open.SetDirectory(self.def_path + "\\VMC")
		vmc_open.ShowModal()


		if vmc_open.GetFilename() == '':
			leave_blank = wx.MessageDialog(self, "Nenhum arquivo aberto, quer deixar em branco?\nAperte 'OK' caso sim.",
				"Aviso!", wx.YES_NO | wx.ICON_QUESTION)

			leave_blank.ShowModal()
			
			yes_or_no = leave_blank.GetYesLabel()
			if yes_or_no == 'Yes':
				game_cfg.set_vmc_file('')
			else:
				vmc_open = wx.FileDialog(self, wildcard="VMC File (*.bin)|*.bin")
				vmc_open.SetMessage("Abra um arquivo *.bin")
				vmc_open.ShowModal()
			
		self.vmc_name = vmc_open.GetFilename()
		vmc_open.Destroy()
		game_cfg.set_vmc_file(self.vmc_name)

		self.vmc.SetValue(os.path.basename(vmc_name))

	def _fill_vmc_content(self, event):
		self.vmc_content_list.DeleteAllItems()

		arq_vmc = open(self.global_vmc_name, 'r+b')

		mc = ps2mc.ps2mc(arq_vmc)
		
		try:
			for save in mc.dir_open("/"):
				if save[8] not in [".", ".."]:
					nome = save[8]
					nome2 = "/" + nome
					tamanho = mc.dir_size(nome2)
					self.__add_vmc_line(self.vmc_content_list, [nome, tamanho])
		finally:
			arq_vmc.close()

	def __add_vmc_line(self, obj, items):
		obj.InsertItem(0, items[0])
		obj.SetItem(0, 1, str(items[1]/1024) + "KB")

	def __import(self, savefile):
		ps2save_ins = ps2save.ps2_save_file()
		file = file(savefile, "rb")
		try:
			ft = ps2save.detect_file_type(file)
			file.seek(0)
			if ft == "max":
				ps2save_ins.load_max_drive(file)
			elif ft == "psu":
				ps2save_ins.load_ems(file)
			elif ft == "cbs":
				ps2save_ins.load_codebreaker(file)
			elif ft == "sps":
				ps2save_ins.load_sharkport(file)
			elif ft == "npo":
				self.error_box(savefile + ": nPort saves"
					       " are not supported.")
				return
			else:
				self.error_box(savefile + ": Save file format not"
					       " recognized.")
				return
		finally:
			f.close()

		if not self.mc.import_save_file(ps2save_ins, True):
			self.error_box(fn + ": Save file already present.")
		
	def on_right_click(self, event):
		
		buttons = {
			wx.NewId(): "Importar",
			wx.NewId(): "Exportar",
			wx.NewId(): "Deletar"
		}

		self.buttons = buttons

		rc_menu = wx.Menu()
		for (id, button) in buttons.items():
			rc_menu.Append(id, button)

			wx.EVT_MENU(rc_menu, id, self.on_sel_right_click)

		rc_menu.InsertSeparator(2)
		# For a reason I couldn't realize, the "GetPoint" was returning a position related to the whole panel
		pos = event.GetPoint()[0] + 361, event.GetPoint()[1] + 125
		self.panel.PopupMenu(rc_menu, pos)

	def on_sel_right_click(self, event):
		clicked_opt = self.buttons[ event.GetId() ]

		print clicked_opt

if __name__ == '__main__':
	app = wx.App(False)
	jnl = App(None, "SaveIt! Manager - PS2 Saves")
	app.MainLoop()

