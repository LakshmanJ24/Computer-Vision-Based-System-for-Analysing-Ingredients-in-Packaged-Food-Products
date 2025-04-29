# Computer-Vision-Based-System-for-Analysing-Ingredients-in-Packaged-Food-Products

The **Computer-Vision-Based-System-for-Analysing-Ingredients-in-Packaged-Food-Products** is a system designed to extract and analyze ingredient data from food labels using **Optical Character Recognition (OCR)**. This system matches the extracted ingredients with a local SQLite database and identifies allergens and patients who should avoid certain ingredients. If no match is found, the system logs the unmatched data and performs web searches to gather more information on potential allergens and dietary restrictions.

---

## 📌 Key Features

- **OCR with Tesseract**: Extracts text from images of food labels.
- **Text Preprocessing**: Cleans the raw OCR output to remove unnecessary words and symbols.
- **Database Matching**: Matches extracted ingredients with a local SQLite database using fuzzy matching (Jaccard similarity).
- **Allergen Detection**: Identifies allergens associated with ingredients.
- **Patient Recommendations**: Suggests patient groups who should avoid certain ingredients based on database entries.
- **Unmatched Data Logging**: Logs unmatched ingredients for further processing or manual review.
- **Google Search Integration**: Performs web searches for the most common allergens and patient groups, providing additional context.

---

## 🖥️ Technologies Used

- **Python 3.7+**
- **OCR Engine**: Tesseract via `pytesseract`
- **Image Processing**: PIL (Pillow) for image enhancement
- **Text Processing**: Regular Expressions (`re`), NLTK (Natural Language Toolkit)
- **Database**: SQLite3 for storing ingredients, allergens, and patient recommendations
- **Similarity Matching**: Fuzzy matching using `fuzzywuzzy` and Jaccard similarity
- **Web Search**: `googlesearch-python` for performing Google searches
- **Data Logging**: Simple text logging for unmatched ingredient entries

---

## 🚀 How to Run the Project

### ✅ Step 1: Clone the Repository

Clone the repository to your local machine using the following command:

git clone https://github.com/LakshmanJ24/Computer-Vision-Based-System-for-Analysing-Ingredients-in-Packaged-Food-Products.git

cd Computer-Vision-Based-System-for-Analysing-Ingredients-in-Packaged-Food-Products

### ✅ Step 2: Install Python Dependencies
Make sure you have Python 3.7+ installed. Then, install the required dependencies:

pip install -r requirements.txt

### ✅ Step 3: Install Tesseract OCR Engine
To enable OCR functionality, you need to install the Tesseract OCR engine. Follow these steps:

Download: Tesseract OCR

Install: Follow the installation instructions for your operating system.

Set the Tesseract Path: Update the Tesseract path in the main.py file:

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

### ✅ Step 4: Add Input Data
Place your ingredient label images in the assets/sample_images/ folder.

Update or replace the ingredient_database.db with your own SQLite database containing ingredients and their corresponding allergens and patient recommendations.

### ✅ Step 5: Run the Project
To run the project, execute the following command:

python main.py

## 🧑‍💻 Usage
Once you run the project, it will prompt you to enter the path of an ingredient image. The system will:

Extract Text: Use OCR to extract text from the image.

Preprocess Text: Clean and preprocess the OCR output.

Database Matching: Compare the extracted ingredients with the database using fuzzy matching.

Display Results: Show allergens and patients who should avoid the ingredients, if any matches are found.

Log Unmatched Data: Store any unmatched ingredients in a text file for further review.

Google Search: If there are common allergens or patient groups, it will search the web for more context.

## 📊 Sample Database Schema
Your ingredient_database.db should have a table like the following:

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT,
    allergen TEXT,
    patients_to_avoid TEXT
);

## 💾 Sample Output
Example of matched allergens and patient recommendations:

Extracted Ingredient: sodium chloride
Allergens found: Sodium, Chloride
Patients who should avoid: Hypertension patients
Example of unmatched ingredients and web search results:

Unmatched Ingredient: calcium_disodium_edta
Detected Words: calcium, disodium, edta
Related Allergens Found Online: preservatives, synthetic agents
Patient Recommendations: Avoid in children, kidney patients

Top 5 Google results for 'Why should people with calcium_disodium_edta allergy avoid this?':
1. [Link 1]
2. [Link 2]
3. [Link 3]
...

## 🧪 Sample Log Output
Any unmatched ingredient will be logged in unmatched_data.txt:

Unmatched Ingredient: sodium_benzoate
Detected Words: sodium, benzoate
Related Allergens Found Online: Preservatives
Patient Recommendations: Avoid for asthmatic patients

## ❗ Known Limitations
OCR Accuracy: OCR may struggle with poor-quality images or handwriting.

Matching Sensitivity: The matching threshold for fuzzy matching (e.g., Jaccard similarity) may need tuning based on the dataset.

Google Search Limitations: Google searches are limited by the number of queries you can make per day and may not always yield relevant results.

## 🛠️ Future Improvements
Real-time OCR: Implement a real-time camera feed for ingredient extraction.

Improved Matching Algorithm: Explore advanced NLP techniques to improve database matching.

Enhanced User Interface: Create a graphical user interface (GUI) for better user experience.

Cross-platform Support: Make the system compatible with macOS and Linux.

## 🙌 Contributing
Contributions, suggestions, and issues are welcome! Feel free to fork this repository and submit a pull request. When contributing, please ensure your code is well-documented and tested.

## 📧 Contact
Email: lakshmanj@karunya.edu.in
GitHub: @LakshmanJ24
