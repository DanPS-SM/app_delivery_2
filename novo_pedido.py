import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QTableView, QComboBox, QSpinBox, QHBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic

class NovoPedido(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("novo_pedido.ui", self)

        # Conectar ao banco de dados MySQL
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crud"
        )
        self.cursor = self.conexao.cursor()

        self.pushButton.clicked.connect(self.salvar_pedido)

        # Carregar os dados nos ComboBoxes
        self.carregar_clientes()
        self.carregar_entregadores()
        self.carregar_formas_pagamento()

        # Carregar data e hora atual
        self.setupUi()

        # Carregar produtos no TableView
        self.carregar_produtos()

    def salvar_pedido(self):
        """Salva o pedido no banco de dados"""
        try:
            # Criar cursor para interação com o banco de dados
            cursor = self.conexao.cursor()

            # Pegar os valores selecionados dos campos
            id_cliente = self.comboBox.currentData()
            id_entregador = self.comboBox_2.currentData()
            id_pagamento = self.comboBox_3.currentData()
            data_pedido = self.dateEdit.date().toString("yyyy-MM-dd")
            hora_pedido = self.timeEdit.time().toString("HH:mm:ss")
            endereco_entrega = self.lineEdit_2.text()
            total = float(self.label_8.text().replace("Total: R$", "").strip())

            if not id_cliente or not id_pagamento:
                QMessageBox.warning(self, "Erro", "Cliente e forma de pagamento são obrigatórios!")
                print("Erro: Cliente e forma de pagamento são obrigatórios!")
                return

            # Inserir na tabela 'pedidos'
            query_pedido = """
            INSERT INTO pedidos (cliente_id, entregador_id, data, hora, forma_pagamento, endereco_entrega, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores_pedido = (id_cliente, id_entregador, data_pedido, hora_pedido, id_pagamento, endereco_entrega, total)

            cursor.execute(query_pedido, valores_pedido)
            self.conexao.commit()

            # Pegar o ID do pedido recém-criado
            id_pedido = cursor.lastrowid

            # Inserir os produtos na tabela 'itens_pedido'
            modelo = self.tableView.model()
            for row in range(modelo.rowCount()):
                index_spin = self.tableView.indexWidget(modelo.index(row, 3))
                if isinstance(index_spin, QWidget):
                    spin_box = index_spin.layout().itemAt(0).widget()
                    quantidade = spin_box.value()
                    if quantidade > 0:
                        nome_produto = modelo.item(row, 0).text()
                        cursor.execute("SELECT id_produto FROM produtos WHERE nome = %s", (nome_produto,))
                        id_produto = cursor.fetchone()

                        if id_produto:
                            id_produto = id_produto[0]

                            query_item = """
                            INSERT INTO pedido_produto (pedido_id, produto_id, quantidade)
                            VALUES (%s, %s, %s)
                            """
                            valores_item = (id_pedido, id_produto, quantidade)

                            cursor.execute(query_item, valores_item)

            # Confirmar as inserções
            self.conexao.commit()
            QMessageBox.information(self, "Sucesso", "Pedido atualizado com sucesso!")
            print("Pedido salvo com sucesso!")
            cursor.close()
            # Fechar a janela após salvar
            self.close()


        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar o pedido: {e}")
            print(f"Erro ao salvar o pedido: {e}")
            self.conexao.rollback()

        finally:
            if self.conexao.is_connected():
                self.conexao.close()
                print("Conexão com o banco de dados fechada.")

    def resetar_formulario(self):
        """Reseta os campos do formulário após salvar um pedido."""
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit.clear()
        self.label_8.setText("Total: R$ 0.00")

        # Reseta a quantidade dos produtos na tabela
        for row in range(self.tableView.model().rowCount()):
            index_widget = self.tableView.indexWidget(self.tableView.model().index(row, 0))
            if index_widget:
                spin_box = index_widget.layout().itemAt(0).widget()
                spin_box.setValue(0)
            self.tableView.model().setItem(row, 4, QStandardItem("0.00"))

    def setupUi(self):
        """Carrega os data e hora atual nos campos"""
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())

    def carregar_clientes(self):
        """Carrega os clientes no combobox"""
        self.cursor.execute("SELECT id_cliente, nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.comboBox.clear()
        self.comboBox.addItem("Selecione...", "")
        for cliente in clientes:
            self.comboBox.addItem(cliente[1], cliente[0])  # Nome exibido, ID armazenado

    def carregar_entregadores(self):
        """Carrega os entregadores no combobox"""
        self.cursor.execute("SELECT id_entregador, nome FROM entregadores")
        entregadores = self.cursor.fetchall()
        self.comboBox_2.clear()
        self.comboBox_2.addItem("Selecione...", "")
        for entregador in entregadores:
            self.comboBox_2.addItem(entregador[1], entregador[0])  # Nome exibido, ID armazenado

    def carregar_formas_pagamento(self):
        """Carrega os formas_pagamento no combobox"""
        self.comboBox_3.clear()
        self.comboBox_3.addItem("Selecione...", "")
        self.comboBox_3.addItem("Dinheiro", "1")
        self.comboBox_3.addItem("Pix", "2")
        self.comboBox_3.addItem("Debito", "3")
        self.comboBox_3.addItem("Credito", "4")

    def carregar_produtos(self):
        """Carrega os produtos no TableView e calcula sub-total e total geral."""
        cursor = self.conexao.cursor()
        self.cursor.execute("SELECT id_produto, nome, descricao, preco_unitario FROM produtos")
        produtos = self.cursor.fetchall()

        # Criando o modelo de tabela com 5 colunas
        modelo = QStandardItemModel(len(produtos), 5)
        modelo.setHorizontalHeaderLabels(["Produto", "Descrição", "Preço", "Qtd", "Sub-Total"])

        self.tableView.setModel(modelo)

        # Lista para armazenar os spin boxes e os preços
        spin_boxes = []

        def atualizar_subtotal(row):
            """Atualiza o subtotal da linha e recalcula o total geral."""
            spin_box = spin_boxes[row]
            quantidade = spin_box.value()
            preco = float(modelo.item(row, 2).text())  # Obtém o preço da tabela
            subtotal = quantidade * preco

            # Atualiza a célula de Sub-Total
            modelo.setItem(row, 4, QStandardItem(f"{subtotal:.2f}"))

            # Atualiza o total geral
            atualizar_total()

        def atualizar_total():
            """Soma todos os subtotais e exibe no label_8."""
            total = sum(float(modelo.item(row, 4).text()) for row in range(modelo.rowCount()))
            self.label_8.setText(f"Total: R$ {total:.2f}")  # Atualiza o QLabel com o valor total

        # Inserindo os dados no modelo
        for row, produto in enumerate(produtos):
            id_produto, nome, descricao, preco = produto

            # Criando SpinBox para selecionar quantidade
            spin_box = QSpinBox()
            spin_box.setMinimum(0)
            spin_box.setMaximum(100)
            spin_boxes.append(spin_box)  # Adiciona à lista para referência posterior

            # Criando Widget para inserir no TableView
            widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(spin_box)
            layout.setContentsMargins(0, 0, 0, 0)  # Remove margem para encaixe correto
            widget.setLayout(layout)

            # Adicionando o SpinBox na coluna "Quantidade"
            index = modelo.index(row, 3)
            self.tableView.setIndexWidget(index, widget)

            # Atualiza subtotal e total quando a quantidade mudar
            spin_box.valueChanged.connect(lambda _, r=row: atualizar_subtotal(r))

            # Adicionando os dados dos produtos nas colunas (Nome, Descrição, Preço)
            modelo.setItem(row, 0, QStandardItem(nome))  # Nome
            modelo.setItem(row, 1, QStandardItem(descricao))  # Descrição
            modelo.setItem(row, 2, QStandardItem(f"{preco:.2f}"))  # Preço
            modelo.setItem(row, 4, QStandardItem("0.00"))  # Sub-total inicial

        # Ajuste do tamanho das colunas proporcional ao conteúdo
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)  # Permite ajuste manual pelo usuário
        self.tableView.setColumnWidth(0, 250)    # Produto (médio)
        self.tableView.setColumnWidth(1, 370)   # Descrição (maior)
        self.tableView.setColumnWidth(2, 100)   # Preço (pequeno)
        self.tableView.setColumnWidth(3, 100)    # Quantidade (pequeno)
        self.tableView.setColumnWidth(4, 100)   # Sub-total (pequeno)

        # Inicializa o total geral
        atualizar_total()

        cursor.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NovoPedido()
    window.show()
    sys.exit(app.exec_())
