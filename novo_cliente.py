import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView, QPushButton, QDialog, QMessageBox

class Cliente(QDialog):
    ''' Classe que representa a janela para adicionar ou editar um cliente '''
    def __init__(self, nome, id_cliente=None, atualizar_lista=None):
        super().__init__()

        if id_cliente:
            self.setWindowTitle("Editar Cliente: {nome}")
        else:
            self.setWindowTitle("Novo Cliente")

        self.setGeometry(100, 100, 600, 581)

        self.ui = uic.loadUi("novo_cliente.ui", self)

        self.id_cliente = id_cliente
        self.atualizar_lista = atualizar_lista

        if id_cliente:
            self.carregar_dados(id_cliente)

        self.ui.label.setText("Novo Cliente" if not id_cliente else "Editar Cliente")
        
        self.ui.pushButton.clicked.connect(self.salvar_cliente)

    def carregar_dados(self, id_cliente):
        ''' Carrega os dados de um cliente específico do banco de dados '''
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
                self.ui.lineEdit.setText(dados[1])
                self.ui.lineEdit_2.setText(dados[2])
                self.ui.lineEdit_3.setText(dados[3])

            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            print("Erro ao carregar os dados: (err)")

    def salvar_cliente(self):
        ''' Salva ou atualiza um cliente no banco de dados '''
        nome = self.ui.lineEdit.text()
        endereco = self.ui.lineEdit_2.text()
        telefone = self.ui.lineEdit_3.text()

        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )

            cursor = conexao.cursor()

            if self.id_cliente:
                cursor.execute("UPDATE clientes SET nome = %s, endereco = %s, telefone = %s WHERE id_cliente = %s",
                               (nome, endereco, telefone, self.id_cliente))
            else:
                cursor.execute("INSERT INTO clientes (nome, endereco, telefone) VALUES (%s, %s, %s)",
                               (nome, endereco, telefone))

            conexao.commit()
            cursor.close()
            conexao.close()

            if self.atualizar_lista:
                self.atualizar_lista()

            QMessageBox.information(self, "Sucesso", "Dados atualizados com sucesso!")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erro", "Falha ao atualizar os dados!")

# Funções auxiliares
def abrir_edicao(id_cliente, atualizar_lista):
    ''' Abre a janela de edição de um cliente específico '''
    janela = Cliente(nome, id_cliente, atualizar_lista)
    janela.exec_()

def abrir_novo_cliente(atualizar_lista):
    ''' Abre a janela para cadastrar um novo cliente '''
    janela = Cliente(nome, None, atualizar_lista)
    janela.exec_()

def excluir_cliente(id_cliente):
    ''' Exclui um cliente do banco de dados '''
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
        except mysql.connector.Error as err:
            print("Erro ao excluir o cliente: (err)")

def buscar_dados():
    ''' Carrega os dados e lista os clientes na interface gráfica '''
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

        ui.tableWidget.setRowCount(len(dados))
        ui.tableWidget.setColumnCount(4)
        ui.tableWidget.setHorizontalHeaderLabels(["Nome", "Endereço", "Telefone", "Ações"])
        ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, linha in enumerate(dados):
            for j, valor in enumerate(linha[1:]):
                ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))

            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(criar_callback_edicao(linha[0]))

            btn_apagar = QPushButton("Apagar")
            btn_apagar.clicked.connect(criar_callback_apagar(linha[0]))

            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(btn_editar)
            layout.addWidget(btn_apagar)

            widget = QtWidgets.QWidget()
            widget.setLayout(layout)

            ui.tableWidget.setCellWidget(i, 3, widget)

        cursor.close()
        conexao.close()
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados: (err)")

def criar_callback_edicao(id_cliente):
    ''' Retorna uma função que abre a edição de um cliente '''
    def callback():
        abrir_edicao(id_cliente, buscar_dados)
    return callback

def criar_callback_apagar(id_cliente):
    ''' Retorna uma função que exclui um cliente '''
    def callback():
        excluir_cliente(id_cliente)
    return callback

# Inicialização do aplicativo
app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = uic.loadUi("lista_clientes.ui", MainWindow)

ui.pushButton.clicked.connect(lambda: abrir_novo_cliente(buscar_dados))

buscar_dados()

MainWindow.show()
sys.exit(app.exec_())
