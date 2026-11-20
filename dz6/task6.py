import os
import sqlite3
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
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)


DB_PATH = os.path.join(os.path.dirname(__file__), "shop.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quan INTEGER NOT NULL CHECK(quan > 0),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );
        """
    )
    conn.commit()
    conn.close()


class ShopDBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет клиентов и заказов (SQLite + PyQt6)")
        self.resize(750, 580)
        init_db()
        self.init_ui()
        self.load_customers()
        self.load_orders()

    def init_ui(self):
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("Добавить клиента:"))
        cust_form = QHBoxLayout()
        self.cust_name_input = QLineEdit()
        self.cust_name_input.setPlaceholderText("ФИО клиента")
        self.cust_email_input = QLineEdit()
        self.cust_email_input.setPlaceholderText("Email клиента")
        self.add_cust_btn = QPushButton("Добавить клиента")
        self.add_cust_btn.clicked.connect(self.add_customer)
        cust_form.addWidget(self.cust_name_input)
        cust_form.addWidget(self.cust_email_input)
        cust_form.addWidget(self.add_cust_btn)
        main_layout.addLayout(cust_form)

        main_layout.addWidget(QLabel("Таблица клиентов (customers):"))
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(3)
        self.customers_table.setHorizontalHeaderLabels(["ID", "ФИО", "Email"])
        main_layout.addWidget(self.customers_table)

        main_layout.addWidget(QLabel("Добавить заказ:"))
        order_form = QHBoxLayout()
        self.order_cust_id_input = QLineEdit()
        self.order_cust_id_input.setPlaceholderText("ID клиента")
        self.order_product_input = QLineEdit()
        self.order_product_input.setPlaceholderText("Товар")
        self.order_quan_input = QLineEdit()
        self.order_quan_input.setPlaceholderText("Количество (> 0)")
        self.add_order_btn = QPushButton("Добавить заказ")
        self.add_order_btn.clicked.connect(self.add_order)
        order_form.addWidget(self.order_cust_id_input)
        order_form.addWidget(self.order_product_input)
        order_form.addWidget(self.order_quan_input)
        order_form.addWidget(self.add_order_btn)
        main_layout.addLayout(order_form)

        filter_layout = QHBoxLayout()
        self.filter_checkbox = QCheckBox("Фильтровать заказы по ID клиента:")
        self.filter_checkbox.stateChanged.connect(self.load_orders)
        self.filter_id_input = QLineEdit()
        self.filter_id_input.setPlaceholderText("Введите ID клиента")
        self.filter_btn = QPushButton("Применить")
        self.filter_btn.clicked.connect(self.load_orders)
        filter_layout.addWidget(self.filter_checkbox)
        filter_layout.addWidget(self.filter_id_input)
        filter_layout.addWidget(self.filter_btn)
        main_layout.addLayout(filter_layout)

        main_layout.addWidget(QLabel("Таблица заказов (orders):"))
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "ID клиента", "Товар", "Количество"])
        main_layout.addWidget(self.orders_table)

        self.setLayout(main_layout)

    def add_customer(self):
        name = self.cust_name_input.text().strip()
        email = self.cust_email_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Ошибка", "Заполните ФИО и Email клиента!")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO customers (name, email) VALUES (?, ?);", (name, email))
            conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Клиент с таким Email уже существует!")
            conn.close()
            return
        conn.close()

        self.cust_name_input.clear()
        self.cust_email_input.clear()
        self.load_customers()
        QMessageBox.information(self, "Успех", "Клиент добавлен в базу данных!")

    def add_order(self):
        cust_id_text = self.order_cust_id_input.text().strip()
        product = self.order_product_input.text().strip()
        quan_text = self.order_quan_input.text().strip()

        if not cust_id_text or not product or not quan_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля заказа!")
            return

        if not cust_id_text.isdigit() or not quan_text.isdigit() or int(quan_text) <= 0:
            QMessageBox.warning(self, "Ошибка", "ID клиента и количество должны быть числами > 0!")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        try:
            cur.execute(
                "INSERT INTO orders (customer_id, product, quan) VALUES (?, ?, ?);",
                (int(cust_id_text), product, int(quan_text)),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Клиент с таким ID не найден!")
            conn.close()
            return
        conn.close()

        self.order_cust_id_input.clear()
        self.order_product_input.clear()
        self.order_quan_input.clear()
        self.load_orders()
        QMessageBox.information(self, "Успех", "Заказ добавлен в базу данных!")

    def load_customers(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM customers;")
        rows = cur.fetchall()
        conn.close()

        self.customers_table.setRowCount(len(rows))
        for r_idx, row in enumerate(rows):
            for c_idx, value in enumerate(row):
                self.customers_table.setItem(r_idx, c_idx, QTableWidgetItem(str(value)))

    def load_orders(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        filter_id = self.filter_id_input.text().strip()
        if self.filter_checkbox.isChecked() and filter_id.isdigit():
            cur.execute(
                "SELECT id, customer_id, product, quan FROM orders WHERE customer_id = ?;",
                (int(filter_id),),
            )
        else:
            cur.execute("SELECT id, customer_id, product, quan FROM orders;")
        rows = cur.fetchall()
        conn.close()

        self.orders_table.setRowCount(len(rows))
        for r_idx, row in enumerate(rows):
            for c_idx, value in enumerate(row):
                self.orders_table.setItem(r_idx, c_idx, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShopDBApp()
    window.show()
    sys.exit(app.exec())
