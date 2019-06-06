# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QColorDialog, QErrorMessage,
	QAction, QFileDialog, QTextEdit, QApplication, QLineEdit, QPushButton, QComboBox, QGridLayout, QMenuBar, QStatusBar, QCheckBox, QMessageBox)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import QStandardPaths, QCoreApplication, Qt
from interface import Ui_MainWindow
import sys, os, os.path, re, mysql.connector

cnx = mysql.connector.connect(user="", password="", database="")


class MyFirstGuiProgram(Ui_MainWindow):
	def __init__(self, main_window):
		Ui_MainWindow.__init__(self)
		self.setupUi(main_window)
		self.file_name = ['']
		self.current_amino_acid_position = ''
		self.article_to_parse_list = []
		self.current_article_index = False
		self.left_label_pattern = ''
		self.query_results_list = []
		# residue_label = self.label
		# left_tedit = self.textEdit
		# parsed_combobox = self.comboBox
		# right_tedit = self.textEdit_2
		# include_db_buttom = self.pushButton
		self.textEdit.setReadOnly(True)

		openFile = QAction(QIcon('open.png'), 'Open', main_window)
		openFile.setShortcut('Ctrl+O')
		quitFile = QAction(QIcon('quit.png'), 'Quit', main_window)
		quitFile.setShortcut('Ctrl+Q')
		self.pushButton.clicked.connect(self.includeInDatabase)
		# self.pushButton_5.clicked.connect(self.moveBetweenQResults('leftqtedit', 'left'))
		self.pushButton_5.clicked.connect(lambda: self.moveBetweenQResults('leftqtedit', 'left'))
		self.pushButton_6.clicked.connect(lambda: self.moveBetweenQResults('leftqtedit', 'right'))

		# self.pushButton_2.clicked.connect(self.moveBetweenQResults())
		# self.pushButton_3.clicked.connect(self.moveBetweenQResults())
		# self.pushButton_4.clicked.connect(self.moveBetweenQResults())
		# self.pushButton_7.clicked.connect(self.moveBetweenQResults())

		openFile.triggered.connect(self.showOpenDialog)
		quitFile.triggered.connect(QCoreApplication.instance().quit)

		menubar = self.menubar
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openFile)
		fileMenu.addAction(quitFile)

	def showOpenDialog(self):
		pathname = QFileDialog.getOpenFileName(main_window, 'Open File', '.')
		self.file_name = ['']
		self.file_name[0] = pathname[0]
		print(pathname[0])
		fname_query = re.search('([A-Z]\d+)\.\w+$', pathname[0])
		if (fname_query):
			cursor = cnx.cursor()
			query_for_residue = ("SELECT aminoacid, align_position FROM Residues")
			cursor.execute(query_for_residue)
			residues_in_db_list = [ str(x[0] + str(x[1])) for x in cursor]
			print(residues_in_db_list)
			cursor.close()
			fname = fname_query.group().split('.')[0]
			print(fname)
			if fname in residues_in_db_list:
				errorExistingResidueInDB = QErrorMessage()
				errorExistingResidueInDB.showMessage('Error!\n\nResidue already exists in current DB\n')
				errorExistingResidueInDB.exec_()
			else:
				self.label.setText(fname)
				self.current_amino_acid_position = fname
				fopen = open(pathname[0], 'r+')
				fread = fopen.read()
				flist = fread.split('\n\n')
				for e_text in flist:
					e_text_list = e_text.split('\n')
					header_line = e_text_list[0]
					# print(header_line)
					# title_art = 
					# year_art = 
					# sequences = 
					description_lines = '\n'.join(e_text_list[1:])
				#texto precisa ser tratado por expressoes regulares e nova lista gerada
				self.article_to_parse_list = flist
				self.textEdit.setText(flist[0])
				self.current_article_index = 0
				self.left_label_pattern = ' of ' + str(len(flist))
				self.label_3.setText(str(1) + self.left_label_pattern)
				#texto ja parcialmente parseado e aberto, agora falta rodar os queries na database, informar numero de resultados e colocar o primeiro na setinha
				#	cursor = cnx.cursor()
				#	query_for_residue = ("SELECT description FROM Articles WHERE Title = %s", self.current_article_title)
				#	cursor.execute(query_for_residue)
				#	cursor.close()
		else:
			errorInputType = QErrorMessage()
			errorInputType.showMessage('Error!\n\nPlease verify the input file name.\n Ex: Correct pattern for Alanine at Position 289: A289.txt')
			errorInputType.exec_()
		#read file and write lines to left textEdit

		#query db for similar entries and append their text to list

		#get most similar entry and append its text to right textEdit

		#update label_2 with entry number 1

	def moveBetweenQResults(self, tedit, move):
		if tedit == 'leftqtedit':
			if self.article_to_parse_list:
				current_number = self.current_article_index
				if move == 'right':
					if (current_number >= 0):
						movement_number = abs(current_number + 1) % len(self.article_to_parse_list)
						self.textEdit.setText(self.article_to_parse_list[movement_number])
						self.label_3.setText(str(movement_number + 1) + self.left_label_pattern)
					else:
						movement_number = abs(current_number + 1) % len(self.article_to_parse_list)
						self.textEdit.setText(self.article_to_parse_list[(-1 * movement_number)])
						if movement_number != 0:
							self.label_3.setText(str(len(self.article_to_parse_list) - movement_number + 1) + self.left_label_pattern)
						else:
							self.label_3.setText(str(movement_number + 1) + self.left_label_pattern)
					self.current_article_index += 1
					# print(self.current_article_index)
				else:
					if (current_number <= 0):
						movement_number = abs(current_number - 1) % len(self.article_to_parse_list)
						self.textEdit.setText(self.article_to_parse_list[(-1 * movement_number)])
						if movement_number != 0:
							self.label_3.setText(str(len(self.article_to_parse_list) - movement_number + 1) + self.left_label_pattern)
						else:
							self.label_3.setText(str(movement_number + 1) + self.left_label_pattern)
					else:
						movement_number = abs(current_number - 1) % len(self.article_to_parse_list)
						self.textEdit.setText(self.article_to_parse_list[(movement_number)])
						self.label_3.setText(str(movement_number + 1) + self.left_label_pattern)
					self.current_article_index -= 1
					# print(self.current_article_index)


		# else:
		# 	if self.query_results_list:
		# 		if move == 'new':
		# 		elif move == 'left':
		# 		else:

		#new equals to entry number 0 which should be empty text


	def includeInDatabase(self):
		#parse output format from box
		current_text = self.textEdit.toPlainText()
		#launch database inclusion

		#clear left textEdit
		self.textEdit.clear()
		#clear right textEdit
		self.textEdit_2.clear()
		#clear label
		#self.label.clear()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	main_window = QMainWindow()
 
	prog = MyFirstGuiProgram(main_window)
 
	main_window.show()
	sys.exit(app.exec_())
