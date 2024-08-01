import streamlit as st
import openpyxl
from openpyxl.styles import PatternFill
from io import BytesIO
from utils.menu import menu_with_redirect
from utils.langdetect import detect_language_of
import time
import asyncio
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
DEFAULT_TARGET_LANG = 'CHS'

# Get available dictionaries, models, and supported language codes
model_list = list_translate_models()
dictionaries = list_dictionary_ids() or ['default_dictionary']
supported_lang_codes = list_supported_language_codes()

def init_streamlit():
    """
    Initialize the Streamlit interface.
    """
    menu_with_redirect()
    st.title("Excel File Translate")

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

async def process_excel(file, target_lang, model_id, dict_id, concurrency):
    """
    Process the Excel file asynchronously, mark cells not in the target language, 
    and collect statistics.

    Args:
        file (UploadedFile): The uploaded Excel file.
        target_lang (str): The translate target language code.
        model_id (str): Which model id you'd like to use
        dict_id(str): The dictionary id
        concurrency (int): Number of concurrent tasks

    Returns:
        bytes: The processed Excel file data.
        dict: A dictionary containing statistics about the file.
    """
    st.write("Processing...")
    start_time = time.time()
    workbook = openpyxl.load_workbook(file)
    progress_bar = st.progress(0)
    total_sheets = len(workbook.sheetnames)
    
    st.write(f"The Excel file contains {total_sheets} sheets.")
    
    total_rows = 0
    total_cells = 0
    non_target_cells = 0
    processed_cells = 0

    semaphore = asyncio.Semaphore(concurrency)  # Use the concurrency value from the slider

    async def process_cell(cell):
        nonlocal non_target_cells, processed_cells
        if cell.data_type == 's' and is_not_number(cell.value):
            lang = detect_language_of(cell.value)
            if lang != target_lang:
                # cell.fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                async with semaphore:
                    try:
                        # Use run_in_executor to run the synchronous translate_content function
                        translation, term_mapping = await asyncio.get_event_loop().run_in_executor(
                            None,
                            translate_content,
                            [cell.value],
                            lang,
                            target_lang,
                            dict_id,
                            model_id,
                        )
                        cell.value = translation.strip()
                        non_target_cells += 1
                    except Exception as e:
                        st.write(f"Error translating cell {cell.coordinate}: {e}")
        
        processed_cells += 1
        # Update progress bar
        progress = processed_cells / total_cells
        progress_bar.progress(progress)

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        sheet_rows = sheet.max_row
        sheet_cells = sheet.max_column * sheet_rows
        total_rows += sheet_rows
        total_cells += sheet_cells
        
        st.write(f"Processing sheet: {sheet_name} (Rows: {sheet_rows}, Cells: {sheet_cells})")

    tasks = []
    for sheet in workbook:
        for row in sheet.iter_rows():
            for cell in row:
                task = asyncio.create_task(process_cell(cell))
                tasks.append(task)
    
    await asyncio.gather(*tasks)

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

async def main():
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
            dictionaries
        )
        model_id = st.selectbox("Translation Model", model_list)
        target_lang = st.selectbox(
            "Target Language",
            supported_lang_codes
        )
        
        # Add a slider for concurrency control
        concurrency = st.slider("Concurrent Number", min_value=1, max_value=10, value=3, step=1)
        
        # Process the file
        if st.button("Translate File", type="primary", use_container_width=True):
            with st.spinner('Processing...'):
                processed_data, stats = await process_excel(uploaded_file, target_lang, model_id, dictionary_name, concurrency)
            
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
                label="Download Translated Excel File",
                data=processed_data,
                file_name=f"processed_{uploaded_file.name}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())