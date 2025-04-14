import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView, QPushButton, QDialog, QMessageBox

class ListaEntregadores(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.buscar_dados()

    def buscar_dados(self):
        try:       
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id_entregador, cpf, nome, endereco, telefone FROM entregadores")
            dados = cursor.fetchall()
            
            
            ui = uic.loadUi("lista_entregadores.ui", self)
            ui.pushButton.clicked.connect(lambda: self.abrir_novo_entregador())
            ui.tableWidget.setRowCount(len(dados))
            ui.tableWidget.setColumnCount(5)
            ui.tableWidget.setHorizontalHeaderLabels(["CPF", "Nome", "Endereço", "Telefone", "Ações"])
            ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            for i, linha in enumerate(dados):
                for j, valor in enumerate(linha[1:]):
                    ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))
                        
                btn_editar = QPushButton("Editar")
                btn_editar.clicked.connect(self.criar_callback_edicao(linha[0]))
                            
                btn_apagar = QPushButton("Apagar")
                btn_apagar.clicked.connect(self.criar_callback_apagar(linha[0]))
                        
                layout = QtWidgets.QHBoxLayout()
                widget = QtWidgets.QWidget()
                layout.addWidget(btn_editar)
                layout.addWidget(btn_apagar)
                layout.setContentsMargins(0, 0, 0, 0)
                widget.setLayout(layout)
                ui.tableWidget.setCellWidget(i, 4, widget)
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")

    def criar_callback_edicao(self, id_entregador):
        def callback():
            self.abrir_edicao(id_entregador)
        return callback

    def criar_callback_apagar(self, id_entregador):
        def callback():
            self.apagar_entregador(id_entregador)
        return callback

    def abrir_edicao(self, id_entregador):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Entregador")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_entregador.ui", dialog)
        
        if id_entregador:
            ui.label.setText("Editar Entregador")
            self.carregar_dados(id_entregador, ui)
        
        ui.pushButton.clicked.connect(lambda: self.salvar_entregador(id_entregador, ui, dialog))
        
        dialog.exec_()

    def abrir_novo_entregador(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Novo Entregador")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_entregador.ui", dialog)
        ui.label.setText("Novo Entregador")
        
        ui.pushButton.clicked.connect(lambda: self.salvar_entregador(None, ui, dialog))
        
        dialog.exec_()

    def apagar_entregador(self, id_entregador):
        resposta = QMessageBox.question(
            None, "Confirmação", f"Deseja realmente excluir o entregador com ID {id_entregador}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            try:
                conexao = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="crud"
                )
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM entregadores WHERE id_entregador = %s", (id_entregador,))
                conexao.commit()
                cursor.close()
                conexao.close()
                self.buscar_dados()  
            except mysql.connector.Error as err:
                print(f"Erro ao excluir o entregador: {err}")
                
    def carregar_dados(self, id_entregador, ui):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id_entregador, cpf, nome, endereco, telefone FROM entregadores WHERE id_entregador = %s", (id_entregador,))
            dados = cursor.fetchone()            
            if dados:
                ui.lineEdit.setText(dados[1])  
                ui.lineEdit_2.setText(dados[2])  
                ui.lineEdit_3.setText(dados[3])
                ui.lineEdit_4.setText(dados[4]) 
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao carregar os dados: {err}")
    
    def salvar_entregador(self, id_entregador, ui, dialog):
        cpf = ui.lineEdit.text()
        nome = ui.lineEdit_2.text()
        endereco = ui.lineEdit_3.text()
        telefone = ui.lineEdit_4.text()

        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            
            if id_entregador:  
                cursor.execute("UPDATE entregadores SET cpf = %s, nome = %s, endereco = %s, telefone = %s WHERE id_entregador = %s", 
                               (cpf, nome, endereco, telefone, id_entregador))
            else:  
                cursor.execute("INSERT INTO entregadores (cpf, nome, endereco, telefone) VALUES (%s, %s, %s, %s)", 
                               (cpf, nome, endereco, telefone))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            self.buscar_dados()
            
            QMessageBox.information(dialog, "Sucesso", "Dados atualizados com sucesso!")
            dialog.accept()
        except mysql.connector.Error as err:
            print(f"Erro ao salvar os dados: {err}")
            QMessageBox.critical(dialog, "Erro", "Falha ao atualizar os dados!")