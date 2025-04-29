import sqlite3
from PIL import Image, ImageEnhance
import pytesseract
import re
import os
from collections import Counter
from googlesearch import search
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

pytesseract.pytesseract.tesseract_cmd = r"C:/Users/LAKSHMAN J/tesseract.exe"

def enhance_image(image_path):
    image = Image.open(image_path)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    directory, filename = os.path.split(image_path)
    file_name, file_ext = os.path.splitext(filename)

    enhanced_filename = f"enhanced_{file_name}{file_ext}"
    save_enhanced_image_path = os.path.join(directory, enhanced_filename)

    image.save(save_enhanced_image_path)
    print(f"Enhanced image saved as: {save_enhanced_image_path}")

    return image, save_enhanced_image_path

def preprocess_text(text_list):
    stop_words = {"and", "or", "with", "without", "from", "by", "of", "for", "to", "in", "on", "at", "as", "is", "are",
                  "was", "were", "be", "been", "a", "an", "the"}

    cleaned_text = []
    for word in text_list:
        word = word.lower()

        if word in {"ingredients", "ingredient","Minimum","minimum","Contains","contain"}:
            continue

        word = re.sub(r"[^\w\s\(\)]", "", word)

        if word.startswith(")") and not word.endswith(")"):
            word = word[1:]
        elif word.endswith(")") and not word.startswith("("):
            word = word[:-1]

        if re.match(r"^[\d%]+$", word):
            continue

        if word in stop_words:
            continue

        if word:
            cleaned_text.append(word)

    return cleaned_text

def extract_text_from_image(image_path):

    image, save_enhanced_image_path = enhance_image(image_path)
    text = pytesseract.image_to_string(image)

    print("Extracted Text:")
    for line in text.strip().splitlines():
        print(line)

    stop_words = set(stopwords.words('english'))
    processed_text = []
    for word in text.strip().split():
        # Remove symbols from words
        word = re.sub(r'[{}(),.]', '', word)
        # Skip empty strings after symbol removal
        if not word:
            continue
        # Remove numbers and percentages
        if re.match(r'^\d+%?$', word):
            continue
        # Remove stopwords
        if word.lower() in stop_words:
            continue
        processed_text.append(word)

    return processed_text

def clean_patient_text(text):
    text = re.sub(r'\bIndividuals with\b', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'\bIndividuals\b', '', text, flags=re.IGNORECASE).strip()
    return text

def fuzzy_match_text(text_list, sqlite_db_path, column_name, allergens_column, patients_column):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Retrieve all entries from the database for fuzzy matching
    cursor.execute(f"SELECT {column_name}, {allergens_column}, {patients_column} FROM my_table")
    db_entries = cursor.fetchall()
    matched_allergens = []
    matched_patients = []
    unmatched_texts = set()

    for text in text_list:
        best_match = None
        best_score = 0

        for entry in db_entries:
            db_text, allergens, patients = entry
            score = fuzz.ratio(text.lower(), db_text.lower())

            if score > best_score:
                best_match = (db_text, allergens, patients)
                best_score = score

        if best_score >= 80:  # Threshold for a good match
            allergens, patients = best_match[1], best_match[2]

            if allergens:
                matched_allergens.append(allergens)
            if patients:
                matched_patients.append(clean_patient_text(patients))
        else:
            unmatched_texts.add(text)

    conn.close()

    if matched_allergens:
        print("\nAllergens associated with the matched Ingredients:")
        for i, allergen in enumerate(set(matched_allergens), 1):
            print(f"{i}. {allergen}")

    if matched_patients:
        print("\nPatients who should avoid:")
        for i, patient in enumerate(set(matched_patients), 1):
            print(f"{i}. {patient}")

    if unmatched_texts:
        print("\nUnmatched Texts (not found in the database):")
        for i, unmatched in enumerate(unmatched_texts, 1):
            print(f"{i}. {unmatched}")

    return matched_allergens, matched_patients, unmatched_texts

def google_search(query, num_results=5):
    #Perform a Google search for the given query and return results.
    try:
        search_results = search(query, num_results=num_results, lang="en")
        return list(search_results)
    except Exception as e:
        print(f"Error performing Google search for query '{query}': {e}")
        return []

def search_most_repeated(allergens, patients, top_n=3):
    #Perform Google searches for the most common allergens and patients.
    allergen_counts = Counter(allergens)
    patient_counts = Counter(patients)
    most_common_allergens = allergen_counts.most_common(top_n)
    most_common_patients = patient_counts.most_common(top_n)

    if most_common_allergens:
        print("\nGoogle Search Results for Most Common Allergens:\n")
        for allergen, _ in most_common_allergens:
            if allergen and allergen.lower() != 'none identified':
                search_query = f"Why should people with {allergen} allergy avoid this?"
                results = google_search(search_query)
                print(f"\nTop 5 Google results for '{search_query}':")
                for i, link in enumerate(results, 1):
                    print(f"{i}. {link}")
    else:
        print("\nNo allergens identified, skipping Google search for allergens.")

    if most_common_patients:
        print("\nGoogle Search Results for Most Common Patients:")
        for patient, _ in most_common_patients:
            if patient and patient.lower() != 'none identified':
                search_query = f"Why should patients with {patient} avoid certain Ingredients?"
                results = google_search(search_query)
                print(f"\nTop 5 Google results for '{search_query}':")
                for i, link in enumerate(results, 1):
                    print(f"{i}. {link}")
    else:
        print("\nNo patients identified, skipping Google search for patients.")
    return most_common_allergens, most_common_patients

def clean_unmatched_text(text):
    #Clean unmatched text by removing unwanted characters.
    if re.match(r'^[\d\s%]*$', text):
        return None

    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text.strip() if cleaned_text else None

def log_unmatched_data(unmatched_texts, log_file):
    #Log unmatched data to a text file.
    with open(log_file, 'a') as file:
        for text in unmatched_texts:
            cleaned_text = clean_unmatched_text(text)
            if cleaned_text:
                file.write(cleaned_text + '\n')

# Main script
if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    sqlite_db_path = "C:/Users/LAKSHMAN J/Downloads/example - Copy.db"
    column_name = "Chemical_Name"
    allergens_column = "Allergens"
    patients_column = "Patients_who_should_avoid"
    log_file_path = "C:/Users/LAKSHMAN J/Downloads/unmatched_data.txt"
    # Extract text from the image and match with SQLite data
    extracted_texts = extract_text_from_image(image_path)
    matched_allergens, matched_patients, unmatched_texts = fuzzy_match_text(
        extracted_texts, sqlite_db_path, column_name, allergens_column, patients_column
    )
    # Log unmatched data to a text file
    log_unmatched_data(unmatched_texts, log_file_path)
    if matched_allergens or matched_patients:
        search_most_repeated(matched_allergens, matched_patients, top_n=3)


# C:/Users/LAKSHMAN J/Desktop/Project/input_images/i2.png
# C:/Users/LAKSHMAN J/Desktop/Project/input_images/i6.png
