
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from openai import OpenAI
import pandas as pd
import argparse
from src.scraper import run_scraper
import traceback
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logopath = 'assets/Eraneoslogo.png'
        
        # Initialize OpenAI client and other necessary variables
        self.client = OpenAI(api_key="your_api_key_here")  # Replace with your API key
        # self.projects_df = pd.DataFrame()  # Initialize empty DataFrame
        # self.inputinstruction = """
        # You will compare a company profile with the project description and find out if the project is a good match for the profile.
        # """
        # self.outputinstruction = """
        # You are an AI that provides structured output. Return the response as a json object with the following keys:
        # - "fitting": String in the form of "true" or "false".
        # - "explanation": A string that provides an explanation.
        # """
        # self.companyprofile = "Your company profile here"  # Replace with actual company profile
        
        # Create parser for arguments
        self.args = argparse.Namespace()
        self.args.test = True  # Set default value for testing

        # Set up the GUI
        self.setWindowTitle('Image in Lower Right Corner with Button')
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget and set a vertical layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox_layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for the image and button
        hbox_layout = QHBoxLayout()

        # Add a spacer to push the image to the right
        hbox_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Load the image and put it in a QLabel
        image_label = QLabel()
        pixmap = QPixmap(self.logopath)  # Replace with your image file path
        image_label.setPixmap(pixmap)

        # Add the image label to the layout
        hbox_layout.addWidget(image_label)

        # Add the horizontal layout (with the image) to the vertical layout
        vbox_layout.addLayout(hbox_layout)

        # Create a spacer to push the button to the bottom
        vbox_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a button
        search_button = QPushButton('Start Search')
        search_button.setMinimumHeight(50)

        # Connect the button click to the function
        search_button.clicked.connect(self.on_search_button_clicked)

        # Add the button to the bottom of the layout
        vbox_layout.addWidget(search_button, alignment=Qt.AlignCenter)

    # Function to be executed when the button is clicked
    def on_search_button_clicked(self):


        try:
            # Run the LLM analysis
            _, project_fits_df = run_scraper()

            # Check if we got any matching projects
            if not project_fits_df.empty:
                message = "Found matching projects!\n\n"
                for _, row in project_fits_df.iterrows():
                    message += f"Project Number: {row['projectNumber']}\n"
                    message += f"Explanation: {row['explanation']}\n\n"
            else:
                message = "No matching projects found."

            QMessageBox.information(self, "Search Results", message)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            print(f"\tError matching segments: {e}")
            print("Full traceback:")
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
