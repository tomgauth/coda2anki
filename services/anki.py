import genanki
import os
import random
import streamlit as st

def generate_anki_flashcards(flashcards):
    """
    Converts flashcards into Anki-friendly format with audio and text for each flashcard.
    :param flashcards: A list of flashcard dictionaries with 'lang_b_text', 'lang_a_text', and 'audio_a_url'.
    :return: A genanki Deck object.
    """
    try:
        # Start by logging the input flashcards
        st.write("Generating Anki flashcards...")

        deck_id = random.randrange(1 << 30, 1 << 31)
        model_id = random.randrange(1 << 30, 1 << 31)

        st.write(f"Deck ID: {deck_id}, Model ID: {model_id}")

        # Define Anki model for the flashcards
        my_model = genanki.Model(
            model_id,
            'Language Learning Model',
            fields=[
                {'name': 'Recto'},
                {'name': 'Verso'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Recto}}',
                    'afmt': '{{Verso}}',
                },
            ])

        my_deck = genanki.Deck(deck_id, 'Language Learning Flashcard Deck')

        media_files = []  # List to store audio file paths

        # Log the total number of flashcards
        st.write(f"Total flashcards to process: {len(flashcards)}")

        # Loop through each flashcard and add it to the deck
        for index, flashcard in enumerate(flashcards):
            st.write(f"Processing flashcard {index + 1} / {len(flashcards)}")
            front = flashcard['lang_b_text']
            back = f"{flashcard['lang_a_text']}, [sound:{flashcard['audio_a_url']}]"
            
            st.write(f"Front: {front}, Back: {back}")

            note = genanki.Note(
                model=my_model,
                fields=[front, back]
            )

            # Add media file (audio) to the list
            if flashcard['audio_a_url']:
                st.write(f"Adding audio file: {flashcard['audio_a_url']}")
                media_files.append(flashcard['audio_a_url'])

            my_deck.add_note(note)

        # Package the deck and include media files
        package = genanki.Package(my_deck)
        package.media_files = media_files  # Attach media files to the package
        package.write_to_file('language_flashcards.apkg')

        st.write("Anki package created successfully!")
        return my_deck

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write(f"Error details: {e}")

