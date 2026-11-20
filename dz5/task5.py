import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QTextEdit,
    QMessageBox,
)


class OrderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет заказов")
        self.resize(450, 400)
        self.orders = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("Добавление нового заказа")
        main_layout.addWidget(title)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Клиент:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя клиента")
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        product_layout = QHBoxLayout()
        product_layout.addWidget(QLabel("Товар:"))
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Введите название товара")
        product_layout.addWidget(self.product_input)
        main_layout.addLayout(product_layout)

        quan_layout = QHBoxLayout()
        quan_layout.addWidget(QLabel("Количество:"))
        self.quan_input = QLineEdit()
        self.quan_input.setPlaceholderText("Введите целое число > 0")
        quan_layout.addWidget(self.quan_input)
        main_layout.addLayout(quan_layout)

        self.urgent_checkbox = QCheckBox("Срочный заказ")
        main_layout.addWidget(self.urgent_checkbox)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить заказ")
        self.add_btn.clicked.connect(self.add_order)
        btn_layout.addWidget(self.add_btn)

        self.clear_btn = QPushButton("Очистить список")
        self.clear_btn.clicked.connect(self.clear_orders)
        btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        main_layout.addWidget(QLabel("Список заказов:"))
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        main_layout.addWidget(self.result_area)

        self.setLayout(main_layout)

    def add_order(self):
        name = self.name_input.text().strip()
        product = self.product_input.text().strip()
        quan_text = self.quan_input.text().strip()

        if not name or not product or not quan_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if not quan_text.isdigit() or int(quan_text) <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество должно быть целым числом больше 0!")
            return

        urgent = " [СРОЧНО]" if self.urgent_checkbox.isChecked() else ""
        order_line = f"{name} — {product} ({quan_text} шт.){urgent}"
        self.orders.append(order_line)
        self.result_area.setText("\n".join(self.orders))

        self.name_input.clear()
        self.product_input.clear()
        self.quan_input.clear()
        self.urgent_checkbox.setChecked(False)
        QMessageBox.information(self, "Успех", "Заказ добавлен!")

    def clear_orders(self):
        self.orders.clear()
        self.result_area.clear()
        QMessageBox.information(self, "Очистка", "Список заказов очищен.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderApp()
    window.show()
    sys.exit(app.exec())
