import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView, QPushButton, QDialog, QMessageBox

class ListaProdutos(QtWidgets.QMainWindow):
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
            cursor.execute("SELECT id_produto, nome, descricao, fornecedor, estoque, preco_unitario FROM produtos")
            dados = cursor.fetchall()
            
            
            ui = uic.loadUi("lista_produtos.ui", self)
            ui.pushButton.clicked.connect(lambda: self.abrir_novo_produto())
            ui.tableWidget.setRowCount(len(dados))
            ui.tableWidget.setColumnCount(6)
            ui.tableWidget.setHorizontalHeaderLabels(["Nome", "Endereço", "Fornecedor", "Estoque", "Preco Unitário", "Ações"])
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
                ui.tableWidget.setCellWidget(i, 5, widget)
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")

    def criar_callback_edicao(self, id_produto):
        def callback():
            self.abrir_edicao(id_produto)
        return callback

    def criar_callback_apagar(self, id_produto):
        def callback():
            self.apagar_produto(id_produto)
        return callback

    def abrir_edicao(self, id_produto):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar produto")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_produto.ui", dialog)
        
        if id_produto:
            ui.label.setText("Editar produto")
            self.carregar_dados(id_produto, ui)
        
        ui.pushButton.clicked.connect(lambda: self.salvar_produto(id_produto, ui, dialog))
        
        dialog.exec_()

    def abrir_novo_produto(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Novo produto")
        dialog.setGeometry(100, 100, 640, 581)
        
        ui = uic.loadUi("novo_produto.ui", dialog)
        ui.label.setText("Novo produto")
        
        ui.pushButton.clicked.connect(lambda: self.salvar_produto(None, ui, dialog))
        
        dialog.exec_()

    def apagar_produto(self, id_produto):
        resposta = QMessageBox.question(
            None, "Confirmação", f"Deseja realmente excluir o produto com ID {id_produto}?",
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
                cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
                conexao.commit()
                cursor.close()
                conexao.close()
                self.buscar_dados()  
            except mysql.connector.Error as err:
                print(f"Erro ao excluir o produto: {err}")
                
    def carregar_dados(self, id_produto, ui):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id_produto, nome, descricao, fornecedor, estoque, preco_unitario FROM produtos WHERE id_produto = %s", (id_produto,))
            dados = cursor.fetchone()            
            if dados:
                ui.lineEdit.setText(dados[1])  
                ui.lineEdit_2.setText(dados[2])  
                ui.lineEdit_3.setText(dados[3])
                ui.lineEdit_4.setText(str(dados[4])) 
                ui.lineEdit_5.setText(str(dados[5]))   
            
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print(f"Erro ao carregar os dados: {err}")
    
    def salvar_produto(self, id_produto, ui, dialog):
        nome = ui.lineEdit.text()
        descricao = ui.lineEdit_2.text()
        fornecedor = ui.lineEdit_3.text()
        estoque = ui.lineEdit_4.text()
        preco_unitario = ui.lineEdit_5.text()

        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            cursor = conexao.cursor()
            
            if id_produto:  
                cursor.execute("UPDATE produtos SET nome = %s, descricao = %s, fornecedor = %s, estoque = %s, preco_unitario = %s WHERE id_produto = %s", 
                               (nome, descricao, fornecedor, estoque, preco_unitario, id_produto))
            else:  
                cursor.execute("INSERT INTO produtos (nome, descricao, fornecedor, estoque, preco_unitario) VALUES (%s, %s, %s, %s, %s)", 
                               (nome, descricao, fornecedor, estoque, preco_unitario))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            self.buscar_dados()
            
            QMessageBox.information(dialog, "Sucesso", "Dados atualizados com sucesso!")
            dialog.accept()
        except mysql.connector.Error as err:
            print(f"Erro ao salvar os dados: {err}")
            QMessageBox.critical(dialog, "Erro", "Falha ao atualizar os dados!")