import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
import uuid

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DiscountCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discount Card Search Application by >>REMO_OX<< ")
        self.setGeometry(100, 100, 1200, 600)
        self.setMinimumSize(1500, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        
        self.db_path = resource_path("discount_card.db")
        self.load_data()
        self.init_ui()

    def load_data(self):
        """Load unique values for governorates dropdown"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            self.governorates = ['All'] + sorted([row[0] for row in cursor.execute(
                "SELECT DISTINCT governorate FROM providers WHERE governorate IS NOT NULL AND governorate != ''").fetchall()])
            self.areas = ['All']
            self.provider_types = ['All']
            self.main_specialties = ['All']
            self.sub_specialties = ['All']
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            sys.exit(1)

    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        search_panel = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        search_panel.setLayout(search_layout)
        self.governorate_combo = QComboBox()
        self.governorate_combo.setMinimumWidth(150)
        self.area_combo = QComboBox()
        self.area_combo.setMinimumWidth(150)
        self.provider_type_combo = QComboBox()
        self.provider_type_combo.setMinimumWidth(150)
        self.main_specialty_combo = QComboBox()
        self.main_specialty_combo.setMinimumWidth(150)
        self.sub_specialty_combo = QComboBox()
        self.sub_specialty_combo.setMinimumWidth(150)
        self.governorate_combo.addItems(self.governorates)
        self.area_combo.addItems(self.areas)
        self.provider_type_combo.addItems(self.provider_types)
        self.main_specialty_combo.addItems(self.main_specialties)
        self.sub_specialty_combo.addItems(self.sub_specialties)
        self.governorate_combo.currentTextChanged.connect(self.update_areas)
        self.area_combo.currentTextChanged.connect(self.update_provider_types)
        self.provider_type_combo.currentTextChanged.connect(self.update_main_specialties)
        self.main_specialty_combo.currentTextChanged.connect(self.update_sub_specialties)
        search_button = QPushButton("Search")
        search_button.setMinimumWidth(100)
        search_button.clicked.connect(self.search_data)
        export_button = QPushButton("Export to Excel")
        export_button.setMinimumWidth(100)
        export_button.clicked.connect(self.export_to_excel)
        exit_button = QPushButton("Exit")
        exit_button.setMinimumWidth(100)
        exit_button.clicked.connect(self.close)
        search_layout.addWidget(QLabel("Governorate:"))
        search_layout.addWidget(self.governorate_combo)
        search_layout.addWidget(QLabel("Area:"))
        search_layout.addWidget(self.area_combo)
        search_layout.addWidget(QLabel("Provider Type:"))
        search_layout.addWidget(self.provider_type_combo)
        search_layout.addWidget(QLabel("Main Specialty:"))
        search_layout.addWidget(self.main_specialty_combo)
        search_layout.addWidget(QLabel("Sub Specialty:"))
        search_layout.addWidget(self.sub_specialty_combo)
        search_layout.addWidget(search_button)
        search_layout.addWidget(export_button)
        search_layout.addWidget(exit_button)
        search_layout.addStretch()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Provider Name", "Address", "Phone", "Hotline", "Agreed Prices"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setMinimumHeight(300)
        main_layout.addWidget(search_panel)
        main_layout.addWidget(self.table, stretch=1)
        main_layout.setStretch(1, 1)
        self.search_data()

    def update_areas(self):
        """Update area dropdown based on selected governorate"""
        selected_governorate = self.governorate_combo.currentText()
        self.area_combo.clear()
        self.area_combo.addItem("All")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if selected_governorate != "All":
                cursor.execute(
                    "SELECT DISTINCT area FROM providers WHERE governorate = ? AND area IS NOT NULL AND area != ''",
                    (selected_governorate,)
                )
            else:
                cursor.execute("SELECT DISTINCT area FROM providers WHERE area IS NOT NULL AND area != ''")
            areas = sorted([row[0] for row in cursor.fetchall()])
            self.area_combo.addItems(areas)
            conn.close()
            self.update_provider_types()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update areas: {str(e)}")

    def update_provider_types(self):
        """Update provider type dropdown based on selected area"""
        selected_governorate = self.governorate_combo.currentText()
        selected_area = self.area_combo.currentText()
        self.provider_type_combo.clear()
        self.provider_type_combo.addItem("All")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT DISTINCT provider_type FROM providers WHERE provider_type IS NOT NULL AND provider_type != ''"
            params = []
            if selected_area != "All":
                query += " AND area = ?"
                params.append(selected_area)
            if selected_governorate != "All":
                query += " AND governorate = ?"
                params.append(selected_governorate)
            cursor.execute(query, params)
            provider_types = sorted([row[0] for row in cursor.fetchall()])
            self.provider_type_combo.addItems(provider_types)
            conn.close()
            self.update_main_specialties()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update provider types: {str(e)}")

    def update_main_specialties(self):
        """Update main specialty dropdown based on selected provider type"""
        selected_governorate = self.governorate_combo.currentText()
        selected_area = self.area_combo.currentText()
        selected_provider_type = self.provider_type_combo.currentText()
        self.main_specialty_combo.clear()
        self.main_specialty_combo.addItem("All")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT DISTINCT main_specialty FROM providers WHERE main_specialty IS NOT NULL AND main_specialty != ''"
            params = []
            if selected_provider_type != "All":
                query += " AND provider_type = ?"
                params.append(selected_provider_type)
            if selected_area != "All":
                query += " AND area = ?"
                params.append(selected_area)
            if selected_governorate != "All":
                query += " AND governorate = ?"
                params.append(selected_governorate)
            cursor.execute(query, params)
            main_specialties = sorted([row[0] for row in cursor.fetchall()])
            self.main_specialty_combo.addItems(main_specialties)
            conn.close()
            self.update_sub_specialties()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update main specialties: {str(e)}")

    def update_sub_specialties(self):
        """Update sub-specialty dropdown based on selected main specialty"""
        selected_governorate = self.governorate_combo.currentText()
        selected_area = self.area_combo.currentText()
        selected_provider_type = self.provider_type_combo.currentText()
        selected_main_specialty = self.main_specialty_combo.currentText()
        self.sub_specialty_combo.clear()
        self.sub_specialty_combo.addItem("All")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT DISTINCT sub_specialty FROM providers WHERE sub_specialty IS NOT NULL AND sub_specialty != ''"
            params = []
            if selected_main_specialty != "All":
                query += " AND main_specialty = ?"
                params.append(selected_main_specialty)
            if selected_provider_type != "All":
                query += " AND provider_type = ?"
                params.append(selected_provider_type)
            if selected_area != "All":
                query += " AND area = ?"
                params.append(selected_area)
            if selected_governorate != "All":
                query += " AND governorate = ?"
                params.append(selected_governorate)
            cursor.execute(query, params)
            sub_specialties = sorted([row[0] for row in cursor.fetchall()])
            self.sub_specialty_combo.addItems(sub_specialties)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update sub-specialties: {str(e)}")

    def search_data(self):
        """Search and display data based on selected criteria"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT provider_name, address, phone, hotline, agreed_prices
                FROM providers
                WHERE 1=1
            """
            params = []
            if self.governorate_combo.currentText() != "All":
                query += " AND governorate = ?"
                params.append(self.governorate_combo.currentText())
            if self.area_combo.currentText() != "All":
                query += " AND area = ?"
                params.append(self.area_combo.currentText())
            if self.provider_type_combo.currentText() != "All":
                query += " AND provider_type = ?"
                params.append(self.provider_type_combo.currentText())
            if self.main_specialty_combo.currentText() != "All":
                query += " AND main_specialty = ?"
                params.append(self.main_specialty_combo.currentText())
            if self.sub_specialty_combo.currentText() != "All":
                query += " AND sub_specialty = ?"
                params.append(self.sub_specialty_combo.currentText())
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            self.table.setRowCount(0)
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ''))
            self.table.resizeColumnsToContents()
            if not results:
                QMessageBox.information(self, "Info", "No results found for the selected criteria.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search data: {str(e)}")

    def export_to_excel(self):
        """Export table data to Excel"""
        import pandas as pd
        rows = self.table.rowCount()
        if rows == 0:
            QMessageBox.warning(self, "Warning", "No data to export!")
            return
        data = []
        for row in range(rows):
            row_data = {
                'Provider Name': self.table.item(row, 0).text() if self.table.item(row, 0) else '',
                'Address': self.table.item(row, 1).text() if self.table.item(row, 1) else '',
                'Phone': self.table.item(row, 2).text() if self.table.item(row, 2) else '',
                'Hotline': self.table.item(row, 3).text() if self.table.item(row, 3) else '',
                'Agreed Prices': self.table.item(row, 4).text() if self.table.item(row, 4) else ''
            }
            data.append(row_data)
        export_df = pd.DataFrame(data)
        filename = f"filtered_discount_card_{uuid.uuid4().hex[:8]}.xlsx"
        try:
            export_df.to_excel(filename, index=False, engine='openpyxl')
            QMessageBox.information(self, "Success", f"Data exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export to Excel: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = DiscountCardApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()