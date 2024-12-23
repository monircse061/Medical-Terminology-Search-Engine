**Heart Diseases Medical Terminology Search Engine**

This project is a web application that uses Apache Nutch as a web crawler, Flask as the framework, and NLP techniques for data preprocessing and extraction. It integrates the SNOMED API for retrieving related medical terminologies.

**Why users need Medical Terminology Search Engine?**

• Detailing medical term with related terms and description all
together.

• Providing accurate, reliable information from trusted sources.

• Connecting related information for better understanding

**Features:**

• Web Crawling: Powered by Apache Nutch for data collection from web sources.

• Natural Language Processing: Uses scikit-learn for text preprocessing and similarity analysis.

• API Integration: Retrieves SNOMED CT descriptions via the SNOMED API.

• Flask Framework: Handles the back-end application and API routes.

**Setup and Installation**

**Step 1: Clone or Download the Repository**

Clone the repository or download it as a ZIP file:

**Step 2: Install Necessary Libraries**

Ensure you have Python installed. Then, navigate to the project folder and install the required libraries:

pip install -r requirements.txt  



Libraries Used:

Flask

Pandas

scikit-learn

urllib

You can refer to the app.py file for any additional dependencies.

**Step 3: Run the Project**

Start the application by running the following command in your terminal:

python app.py  

The application will start running on http://localhost:5000.

**Project Structure**
├── app.py                   # Main application file  
├── images/                  # Images used in the project  
├── static/                  # Static assets like CSS and JavaScript  
├── templates/               # HTML templates for the Flask app  
├── extracted_database.json  # Pre-extracted data from web sources  
├── pre_database.json        # Preprocessed database file  
├── preprocess_data.ipynb    # Jupyter Notebook for preprocessing  
├── main_process.ipynb       # Main data processing notebook  
└── requirements.txt         # List of required Python libraries  

**Technology Stack**

Framework: Flask

Back End: Python

Web Crawler: Apache Nutch

NLP: scikit-learn

API: SNOMED

**Contributors**

[MD MONIR AHAMMOD]: Project Lead

[VO NGOC HUY THONG]: Team Member

**License**

This project is licensed under the MIT License.

Feel free to reach out for any questions or contributions! 😊

