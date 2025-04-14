import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView, QPushButton, QDialog, QMessageBox

class ListaClientes(QtWidgets.QMainWindow):
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
            cursor.execute("SELECT id_cliente, nome, endereco, telefone FROM clientes")
            dados = cursor.fetchall()
            
            ui = uic.loadUi("lista_clientes.ui", self)
            ui.pushButton.clicked.connect(lambda: self.abrir_novo_cliente())
            ui.tableWidget.setRowCount(len(dados))
            ui.tableWidget.setColumnCount(4)
            ui.tableWidget.setHorizontalHeaderLabels(["Nome", "Endereço", "Telefone", "Ações"])
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
                ui.tableWidget.setCellWidget(i, 3, widget)
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")

    def criar_callback_edicao(self, id_cliente):
        def callback():
            self.abrir_edicao(id_cliente)
        return callback

    def criar_callback_apagar(self, id_cliente):
        def callback():
            self.apagar_cliente(id_cliente)
        return callback

    def abrir_edicao(self, id_cliente):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Cliente")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_cliente.ui", dialog)
        
        if id_cliente:
            ui.label.setText("Editar Cliente")
            self.carregar_dados(id_cliente, ui)
        
        ui.pushButton.clicked.connect(lambda: self.salvar_cliente(id_cliente, ui, dialog))
        
        dialog.exec_()

    def abrir_novo_cliente(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Novo Cliente")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_cliente.ui", dialog)
        ui.label.setText("Novo Cliente")
        
        ui.pushButton.clicked.connect(lambda: self.salvar_cliente(None, ui, dialog))
        
        dialog.exec_()

    def apagar_cliente(self, id_cliente):
        resposta = QMessageBox.question(
            None, "Confirmação", f"Deseja realmente excluir o cliente com ID {id_cliente}?",
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
                cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
                conexao.commit()
                cursor.close()
                conexao.close()
                self.buscar_dados()  
            except mysql.connector.Error as err:
                print(f"Erro ao excluir o cliente: {err}")
                
    def carregar_dados(self, id_cliente, ui):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id_cliente, nome, endereco, telefone FROM clientes WHERE id_cliente = %s", (id_cliente,))
            dados = cursor.fetchone()            
            if dados:
                ui.lineEdit.setText(dados[1])  
                ui.lineEdit_2.setText(dados[2])  
                ui.lineEdit_3.setText(dados[3])  
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao carregar os dados: {err}")
    
    def salvar_cliente(self, id_cliente, ui, dialog):
        nome = ui.lineEdit.text()
        endereco = ui.lineEdit_2.text()
        telefone = ui.lineEdit_3.text()

        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            
            if id_cliente:  
                cursor.execute("UPDATE clientes SET nome = %s, endereco = %s, telefone = %s WHERE id_cliente = %s", 
                               (nome, endereco, telefone, id_cliente))
            else:  
                cursor.execute("INSERT INTO clientes (nome, endereco, telefone) VALUES (%s, %s, %s)", 
                               (nome, endereco, telefone))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            self.buscar_dados()
            
            QMessageBox.information(dialog, "Sucesso", "Dados atualizados com sucesso!")
            dialog.accept()
        except mysql.connector.Error as err:
            print(f"Erro ao salvar os dados: {err}")
            QMessageBox.critical(dialog, "Erro", "Falha ao atualizar os dados!")