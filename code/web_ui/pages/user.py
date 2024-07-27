import streamlit as st
import openpyxl
from openpyxl.styles import PatternFill
from io import BytesIO
from utils.menu import menu_with_redirect
from utils.langdetect import detect_language_of
import time
from utils.utils import (
    list_dictionary_ids,
    list_supported_language_codes,
    list_translate_models,
    translate_content,
)

# Streamlit page configuration
st.set_page_config(
    page_title="File Translate",
    page_icon="🚎",
)

# Global constant for target language
TARGET_LANG = 'CHS'

# Get available dictionaries, models, and supported language codes
model_list = list_translate_models()
dictionaries = list_dictionary_ids() or ['default_dictionary']
supported_lang_codes = list_supported_language_codes()

def init_streamlit():
    """
    Initialize the Streamlit interface.
    """
    menu_with_redirect()
    st.title("Excel File Language Processor")
    st.markdown(f"You are logged in as {st.session_state.role}.")

def is_not_number(text):
    """
    Check if the given text is not a number.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text is not a number, False otherwise.
    """
    try:
        float(text)
        return False
    except ValueError:
        return True

def process_excel(file, target_lang):
    """
    Process the Excel file, mark cells not in the target language, 
    and collect statistics.

    Args:
        file (UploadedFile): The uploaded Excel file.
        target_lang (str): The target language code.

    Returns:
        bytes: The processed Excel file data.
        dict: A dictionary containing statistics about the file.
    """
    start_time = time.time()
    workbook = openpyxl.load_workbook(file)
    progress_bar = st.progress(0)
    total_sheets = len(workbook.sheetnames)
    
    st.write(f"The Excel file contains {total_sheets} sheets.")
    
    total_rows = 0
    total_cells = 0
    non_target_cells = 0

    for sheet_index, sheet_name in enumerate(workbook.sheetnames):
        sheet = workbook[sheet_name]
        sheet_rows = sheet.max_row
        sheet_cells = sheet.max_column * sheet_rows
        total_rows += sheet_rows
        total_cells += sheet_cells
        
        st.write(f"Processing sheet: {sheet_name} (Rows: {sheet_rows}, Cells: {sheet_cells})")
        
        for row_index, row in enumerate(sheet.iter_rows(), 1):
            for cell in row:
                if cell.data_type == 's' and is_not_number(cell.value):
                    lang = detect_language_of(cell.value)
                    if lang != target_lang:
                        cell.fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                        non_target_cells += 1
            
            # Update progress bar
            progress = (sheet_index * sheet_rows + row_index) / (total_sheets * sheet_rows)
            progress_bar.progress(progress)

    end_time = time.time()
    processing_time = end_time - start_time

    buffer = BytesIO()
    workbook.save(buffer)
    
    return buffer.getvalue(), {
        "total_sheets": total_sheets,
        "total_rows": total_rows,
        "total_cells": total_cells,
        "non_target_cells": non_target_cells,
        "processing_time": processing_time
    }

def upload_file():
    """
    Handle file upload.

    Returns:
        UploadedFile: The uploaded Excel file.
    """
    return st.file_uploader("Select an Excel file", type=["xlsx", "xls"])

def main():
    """
    Main function to drive the Streamlit application.
    """
    # Initialize Streamlit interface
    init_streamlit()
    
    # File upload
    uploaded_file = upload_file()
    
    if uploaded_file is not None:
        st.write("Filename:", uploaded_file.name)
        
        # Selection for dictionary and model
        dictionary_name = st.selectbox(
            "Dictionary",
            dictionaries,
            index=dictionaries.index('anthropic.claude-3-haiku-20240307-v1:0') if 'anthropic.claude-3-haiku-20240307-v1:0' in dictionaries else 0
        )
        model_id = st.selectbox("Translation Model", model_list)
        target_lang = st.selectbox(
            "Target Language",
            supported_lang_codes,
            index=supported_lang_codes.index(TARGET_LANG) if TARGET_LANG in supported_lang_codes else 0
        )
        
        # Process the file
        if st.button("Process File"):
            with st.spinner('Processing...'):
                processed_data, stats = process_excel(uploaded_file, TARGET_LANG)
            
            # Display statistics
            st.success('Processing Complete!')
            st.write("Statistics:")
            st.write(f"- Total Sheets: {stats['total_sheets']}")
            st.write(f"- Total Rows: {stats['total_rows']}")
            st.write(f"- Total Cells: {stats['total_cells']}")
            st.write(f"- Non-target Language Cells: {stats['non_target_cells']}")
            st.write(f"- Processing Time: {stats['processing_time']:.2f} seconds")
            
            # Download the processed file
            st.download_button(
                label="Download Processed Excel File",
                data=processed_data,
                file_name=f"processed_{uploaded_file.name}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Run the main function
if __name__ == "__main__":
    main()
