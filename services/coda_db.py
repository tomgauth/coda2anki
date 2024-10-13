import streamlit as st
import pandas as pd
from codaio import Coda, Table, Document, Cell
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Coda API key
CODA_API_KEY = os.getenv("CODA_API_KEY")

# Coda API credentials
DOC_ID = 'jPJTMi7bJR'
TABLE_ID = 'grid-2sttiFy7gJ'  # New table ID

# Initialize Coda client
coda = Coda(CODA_API_KEY)

# Initialize Coda client and document
doc = Document(DOC_ID, coda=coda)

# Get the table using the new table ID
table = doc.get_table(TABLE_ID)

# Convert the table to a pandas DataFrame
df = pd.DataFrame(table.to_dict())

# Function to filter and fetch lesson information from the Coda table based on 'lesson' and 'username'
def get_flashcards_by_lesson_username(lesson, username):
    matching_rows = df[(df['lesson'] == lesson) & (df['user_username'] == username)]

    if not matching_rows.empty:
        flashcards = []
        for _, row in matching_rows.iterrows():
            flashcard = {
                'lesson': row['lesson'],
                'name': row['Name'],
                'lang_a_text': row['lang_a_text'],
                'lang_b_text': row['lang_b_text'],
                'explanation': row['explanation'],
                'auto_translate': row['auto_translate'],
                'audio_a_url': row['audio_a_url'],
                'lang_a': row['lang_a'],
                'lang_b': row['lang_b'],
                'flashcard_type': row['flashcard_type']
            }
            flashcards.append(flashcard)
        return flashcards
    else:
        return None

# Step to display filtered flashcards in a DataFrame format
def display_flashcards(lesson, username):
    flashcards = get_flashcards_by_lesson_username(lesson, username)
    if flashcards:
        df_flashcards = pd.DataFrame(flashcards)
        st.write(f"Flashcards for Lesson {lesson} and Username {username}:")
        st.dataframe(df_flashcards)
        return df_flashcards
    else:
        st.write("No matching flashcards found.")
        return None

# Function to export filtered flashcards to a format suitable for Anki import
def export_flashcards_to_anki(flashcards):
    if flashcards:
        output = ""
        for flashcard in flashcards:
            front = flashcard['lang_a_text']
            back = flashcard['lang_b_text']
            audio = flashcard['audio_a_url
