# Discount Card Search Application

## Overview
The **Discount Card Search Application** is a desktop application built with Python, PyQt5, and SQLite. It enables users to search and filter medical service providers stored in a local SQLite database (`discount_card.db`). The application features a user-friendly interface with cascading dropdown menus, a resizable window, and the ability to export filtered results to Excel. Designed for Windows, it provides an intuitive way to browse providers by governorate, area, provider type, main specialty, and sub-specialty.

This repository contains the source code, SQLite database, and instructions to build a standalone executable using PyInstaller, making it easy to distribute without requiring Python or additional dependencies.

## Features
- **SQLite Database**: Uses a pre-populated `discount_card.db` for efficient data storage and querying.
- **Cascading Dropdowns**:
  - Filter areas by selected governorate.
  - Filter provider types by selected area and governorate.
  - Filter main specialties by selected provider type, area, and governorate.
  - Filter sub-specialties by selected main specialty, provider type, area, and governorate.
- **Search Functionality**: Filter providers by:
  - Governorate (المحافظة)
  - Area (المنطقة)
  - Provider Type (نوع مقدم الخدمة)
  - Main Specialty (التخصص الرئيسي)
  - Sub Specialty (التخصص الفرعي)
- **Data Display**: Shows filtered results in a table with columns for Provider Name, Address, Phone, Hotline, and Agreed Prices.
- **Export to Excel**: Export table data to Excel files with unique filenames.
- **Resizable Interface**: Adjustable window size with dynamic layout for dropdowns and table.
- **Exit Button**: Dedicated button to close the application.
- **Error Handling**: Robust error messages for database issues, missing data, or export failures.
- **Standalone Executable**: Build a single `.exe` file with PyInstaller, including the SQLite database.

## Requirements
- **Python**: Version 3.8 to 3.10 (for development and testing).
- **Dependencies**:
  - `PyQt5`: For the graphical user interface.
  - `pandas`: For Excel export functionality.
  - `openpyxl`: For writing Excel files.
- **Operating System**: Windows (tested on Windows; other platforms may work but are untested).
- **SQLite Database**: `discount_card.db` (included in the repository).
- **PyInstaller**: For building the standalone executable (optional, for distribution).

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/discount-card-search-app.git
   cd discount-card-search-app
   ```
2. **Install Python**: Ensure Python 3.8-3.10 is installed. Download from [python.org](https://www.python.org/downloads/).
3. **Install Dependencies**:
   ```bash
   pip install PyQt5 pandas openpyxl
   ```
4. **Verify Files**: Ensure `discount_card_app.py` and `discount_card.db` are in the project directory.

## Usage
1. **Run the Application**:
   ```bash
   python discount_card_app.py
   ```
   The application will open, load data from `discount_card.db`, and display all providers in a table.
2. **Search Data**:
   - Select a governorate to filter available areas.
   - Select an area to filter provider types.
   - Select a provider type to filter main specialties.
   - Select a main specialty to filter sub-specialties.
   - Use "All" in any dropdown to broaden the search.
   - Click **Search** to update the table with filtered results.
3. **Export Data**:
   - Click **Export to Excel** to save the table data to an Excel file (e.g., `filtered_discount_card_xxxxxxxx.xlsx`).
   - A success message confirms the export location.
4. **Exit**:
   - Click **Exit** to close the application.
5. **Resize Window**:
   - Drag window edges or maximize to adjust size; dropdowns and table adapt dynamically.

## Building the Executable
To create a standalone executable for Windows, use PyInstaller to package the application with the SQLite database.

### Prerequisites
- Install PyInstaller:
  ```bash
  pip install PyInstaller
  ```

### Steps
1. **Navigate to Project Directory**:
   ```bash
   cd path/to/discount-card-search-app
   ```
2. **Run PyInstaller**:
   ```bash
   pyinstaller --onefile --add-data "discount_card.db;." --name DiscountCardApp discount_card_app.py
   ```
   - `--onefile`: Creates a single `.exe` file.
   - `--add-data "discount_card.db;."`: Includes the SQLite database.
   - `--name DiscountCardApp`: Names the executable `DiscountCardApp.exe`.
3. **Locate the Executable**:
   - Find `DiscountCardApp.exe` in the `dist` folder.
4. **Test the Executable**:
   - Copy `DiscountCardApp.exe` to a Windows machine without Python.
   - Double-click to run and verify functionality (dropdowns, search, export, exit).
5. **Optional: Add an Icon**:
   - Place an `.ico` file (e.g., `app.ico`) in the project directory.
   - Run:
     ```bash
     pyinstaller --onefile --add-data "discount_card.db;." --name DiscountCardApp --icon=app.ico discount_card_app.py
     ```

### Notes
- The executable includes `discount_card.db`, so no external database is needed.
- Exported Excel files are saved in the same directory as the executable.
- The executable size may be large (200-300 MB) due to PyQt5 and pandas.
- Ensure write permissions in the executable’s directory for Excel exports.

## Project Structure
```
discount-card-search-app/
├── discount_card_app.py  # Main Python script
├── discount_card.db      # SQLite database
├── README.md             # Project documentation
```

## Database
- **File**: `discount_card.db`
- **Table**: `providers`
- **Columns**:
  - `id` (Primary Key)
  - `governorate` (المحافظة)
  - `area` (المنطقة)
  - `provider_type` (نوع مقدم الخدمة)
  - `main_specialty` (التخصص الرئيسي)
  - `sub_specialty` (التخصص الفرعي)
  - `provider_name` (إسم مقدم الخدمة)
  - `address` (العنوان)
  - `phone` (التليفون)
  - `hotline` (الخط الساخن)
  - `agreed_prices` (الاسعار المتفق عليها)
- The database is pre-populated and included in the repository.

## Troubleshooting
- **Application Fails to Start**: Ensure `discount_card.db` is in the project directory and readable.
- **Dropdowns Empty**: Verify `discount_card.db` contains data in the `providers` table.
- **Export Fails**: Check write permissions in the project directory and ensure `openpyxl` is installed.
- **Executable Issues**:
  - Confirm `--add-data "discount_card.db;."` is used in PyInstaller command.
  - Test on a clean Windows machine to rule out missing dependencies.
  - If antivirus flags the executable, add an exception.
- **Dependency Errors**: Reinstall dependencies:
  ```bash
  pip install PyQt5 pandas openpyxl
  ```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please include tests and update documentation as needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For issues, feature requests, or questions, please:
- Open an issue on GitHub.
- Contact the maintainer at `<your-email@example.com>`.

*Last Updated: May 26, 2025*