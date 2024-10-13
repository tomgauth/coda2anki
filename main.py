import streamlit as st
import pandas as pd
from services.anki import generate_anki_flashcards
from codaio import Coda, Document
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Coda API credentials
CODA_API_KEY = os.getenv("CODA_API_KEY")
DOC_ID = 'jPJTMi7bJR'
TABLE_ID = 'grid-2sttiFy7gJ'

# Initialize Coda client
coda = Coda(CODA_API_KEY)

# Initialize Coda client and document
doc = Document(DOC_ID, coda=coda)

# Get the table using the table ID
table = doc.get_table(TABLE_ID)

# Convert the table to a pandas DataFrame
df = pd.DataFrame(table.to_dict())

# Function to filter and fetch flashcards from Coda table based on 'lesson' and 'username'
def get_flashcards_by_username(username):
    matching_rows = df[df['user_username'] == username]  # Correct way to filter rows
    
    if not matching_rows.empty:
        flashcards = []
        for _, row in matching_rows.iterrows():
            flashcard = {
                'lesson': row['lesson'],
                'lang_a_text': row['lang_a_text'],
                'lang_b_text': row['lang_b_text'],
                'audio_a_url': row['audio_a_url']
            }
            flashcards.append(flashcard)
        return flashcards
    else:
        return None

# Streamlit UI
st.title("Anki Flashcard Generator from Coda")

username = st.text_input("Enter your username:", value="alicetest")

if st.button("Fetch Flashcards"):
    flashcards = get_flashcards_by_username(username)

    if flashcards:
        # Preview flashcards
        st.write("Preview of Flashcards:")
        flashcards_df = pd.DataFrame(flashcards)
        st.dataframe(flashcards_df)
        anki_flashcards = generate_anki_flashcards(flashcards)
        st.text_area("Anki Flashcards Format", anki_flashcards)
        # Option to export flashcards to Anki format
        if st.button("Export to Anki Format"):
            st.write("ok let's go")
    else:
        st.error("No matching flashcards found.")
