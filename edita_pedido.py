import sys
import mysql.connector
import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QTableView, QComboBox, QSpinBox, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QDate, QTime

class EditarPedido(QDialog):
    def __init__(self, id_pedido):
        super().__init__()
        loadUi("edita_pedido.ui", self)  # Presume-se que você tenha um arquivo .ui para edição
        self.id_pedido = id_pedido

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

        # Carregar os dados do pedido e produtos
        self.carregar_dados_pedido()
        self.carregar_produtos()

    def salvar_pedido(self):
        """Atualiza o pedido no banco de dados"""
        try:
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
                return

            # Atualizar a tabela 'pedidos'
            query_pedido = '''
                UPDATE pedidos
                SET cliente_id = %s, entregador_id = %s, data = %s, hora = %s, 
                    forma_pagamento = %s, endereco_entrega = %s, total = %s
                WHERE id_pedido = %s
            '''
            valores_pedido = (id_cliente, id_entregador, data_pedido, hora_pedido, id_pagamento, endereco_entrega, total, self.id_pedido)
            cursor.execute(query_pedido, valores_pedido)

            # Deletar os itens existentes para atualizar com os novos
            cursor.execute("DELETE FROM pedido_produto WHERE pedido_id = %s", (self.id_pedido,))

            # Inserir os produtos atualizados na tabela 'pedido_produto'
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
                            valores_item = (self.id_pedido, id_produto, quantidade)
                            cursor.execute(query_item, valores_item)

            # Confirmar as alterações
            self.conexao.commit()
            QMessageBox.information(self, "Sucesso", "Pedido atualizado com sucesso!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar o pedido: {e}")
            self.conexao.rollback()

        finally:
            if cursor:
                cursor.close()
            if self.conexao.is_connected():
                self.conexao.close()

    def carregar_dados_pedido(self):
        """Carrega os dados do pedido existente nos campos"""
        query_pedido = '''
            SELECT data, hora, forma_pagamento, total, endereco_entrega, cliente_id, entregador_id
            FROM pedidos
            WHERE pedidos.id_pedido = %s
        '''
        self.cursor.execute(query_pedido, (self.id_pedido,))
        resultado = self.cursor.fetchone()

        if resultado:
            data, hora, forma_pagamento, total, endereco, cliente_id, entregador_id = resultado

            # Converter datetime.date para string no formato "yyyy-MM-dd"
            if isinstance(data, datetime.date):
                data_str = data.strftime("%Y-%m-%d")
            else:
                data_str = str(data)

            # Converter datetime.timedelta para QTime
            if isinstance(hora, datetime.timedelta):
                total_seconds = int(hora.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                hora_qtime = QTime(hours, minutes, seconds)
            else:
                hora_qtime = QTime.fromString(str(hora), "HH:mm:ss")

            # Preencher os campos com os dados
            self.dateEdit.setDate(QDate.fromString(data_str, "yyyy-MM-dd"))
            self.timeEdit.setTime(hora_qtime)
            self.lineEdit_2.setText(endereco)
            self.label_8.setText(f"Total: R$ {total:.2f}")

            # Selecionar os valores nos ComboBoxes
            self.comboBox.setCurrentIndex(self.comboBox.findData(cliente_id))
            self.comboBox_2.setCurrentIndex(self.comboBox_2.findData(entregador_id))
            self.comboBox_3.setCurrentIndex(self.comboBox_3.findData(forma_pagamento))

    def carregar_clientes(self):
        """Carrega os clientes no combobox"""
        self.cursor.execute("SELECT id_cliente, nome FROM clientes")
        clientes = self.cursor.fetchall()
        self.comboBox.clear()
        self.comboBox.addItem("Selecione...", "")
        for cliente in clientes:
            self.comboBox.addItem(cliente[1], cliente[0])

    def carregar_entregadores(self):
        """Carrega os entregadores no combobox"""
        self.cursor.execute("SELECT id_entregador, nome FROM entregadores")
        entregadores = self.cursor.fetchall()
        self.comboBox_2.clear()
        self.comboBox_2.addItem("Selecione...", "")
        for entregador in entregadores:
            self.comboBox_2.addItem(entregador[1], entregador[0])

    def carregar_formas_pagamento(self):
        """Carrega as formas de pagamento no combobox"""
        self.comboBox_3.clear()
        self.comboBox_3.addItem("Selecione...", "")
        self.comboBox_3.addItem("Dinheiro", "1")
        self.comboBox_3.addItem("Pix", "2")
        self.comboBox_3.addItem("Debito", "3")
        self.comboBox_3.addItem("Credito", "4")

    def carregar_produtos(self):
        """Carrega os produtos no TableView e preenche as quantidades do pedido"""
        query_produtos = '''
            SELECT produtos.nome, produtos.descricao, produtos.preco_unitario, pp.quantidade
            FROM pedido_produto pp
            JOIN pedidos ON pp.pedido_id = pedidos.id_pedido
            JOIN produtos ON pp.produto_id = produtos.id_produto
            WHERE pp.pedido_id = %s
        '''
        self.cursor.execute("SELECT id_produto, nome, descricao, preco_unitario FROM produtos")
        produtos = self.cursor.fetchall()

        # Criar o modelo da tabela
        modelo = QStandardItemModel(len(produtos), 5)
        modelo.setHorizontalHeaderLabels(["Produto", "Descrição", "Preço", "Qtd", "Sub-Total"])
        self.tableView.setModel(modelo)

        # Carregar produtos do pedido
        self.cursor.execute(query_produtos, (self.id_pedido,))
        produtos_pedido = {row[0]: row[3] for row in self.cursor.fetchall()}  # Dicionário nome:quantidade

        spin_boxes = []

        def atualizar_subtotal(row):
            spin_box = spin_boxes[row]
            quantidade = spin_box.value()
            preco = float(modelo.item(row, 2).text())
            subtotal = quantidade * preco
            modelo.setItem(row, 4, QStandardItem(f"{subtotal:.2f}"))
            atualizar_total()

        def atualizar_total():
            total = sum(float(modelo.item(row, 4).text()) for row in range(modelo.rowCount()))
            self.label_8.setText(f"Total: R$ {total:.2f}")

        # Preencher o modelo com os produtos
        for row, produto in enumerate(produtos):
            id_produto, nome, descricao, preco = produto

            spin_box = QSpinBox()
            spin_box.setMinimum(0)
            spin_box.setMaximum(100)
            quantidade = produtos_pedido.get(nome, 0)  # Quantidade do pedido ou 0
            spin_box.setValue(quantidade)
            spin_boxes.append(spin_box)

            widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(spin_box)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)

            index = modelo.index(row, 3)
            self.tableView.setIndexWidget(index, widget)

            spin_box.valueChanged.connect(lambda _, r=row: atualizar_subtotal(r))

            modelo.setItem(row, 0, QStandardItem(nome))
            modelo.setItem(row, 1, QStandardItem(descricao))
            modelo.setItem(row, 2, QStandardItem(f"{preco:.2f}"))
            modelo.setItem(row, 4, QStandardItem(f"{quantidade * preco:.2f}"))

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        self.tableView.setColumnWidth(0, 250)
        self.tableView.setColumnWidth(1, 370)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.setColumnWidth(3, 100)
        self.tableView.setColumnWidth(4, 100)

        atualizar_total()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditarPedido(1)  # Exemplo: editar pedido com id_pedido = 1
    window.show()
    sys.exit(app.exec_())