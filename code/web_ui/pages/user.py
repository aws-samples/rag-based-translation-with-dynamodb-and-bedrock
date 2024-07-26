from utils.menu import menu_with_redirect

import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
from openpyxl.utils import get_column_letter
from tempfile import NamedTemporaryFile
from openpyxl.worksheet.views import SheetView

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")


def copy_border(source_cell, target_cell):
    if source_cell.border.left.style:
        target_cell.border = Border(left=source_cell.border.left,
                                    right=source_cell.border.right,
                                    top=source_cell.border.top,
                                    bottom=source_cell.border.bottom)
    else:
        target_cell.border = Border(left=Side(style=None),
                                    right=Side(style=None),
                                    top=Side(style=None),
                                    bottom=Side(style=None))

def copy_sheet_format(source_sheet, target_sheet):
    # Copy column widths
    for i, column in enumerate(source_sheet.columns):
        column_letter = get_column_letter(i + 1)
        if column_letter in source_sheet.column_dimensions:
            target_sheet.column_dimensions[column_letter].width = source_sheet.column_dimensions[column_letter].width

    # Copy cell formats and merged cells
    for row in source_sheet.rows:
        for cell in row:
            if isinstance(cell, openpyxl.cell.cell.MergedCell):
                continue  # Skip merged cells
            target_cell = target_sheet.cell(cell.row, cell.column)
            target_cell.font = cell.font.copy()
            copy_border(cell, target_cell)
            target_cell.fill = cell.fill.copy()
            target_cell.number_format = cell.number_format
            target_cell.protection = cell.protection.copy()
            target_cell.alignment = cell.alignment.copy()

    # Copy merged cell ranges
    for merged_range in source_sheet.merged_cells.ranges:
        target_sheet.merge_cells(str(merged_range))
        
    # Copy Gridlines setting
    if source_sheet.sheet_view:
        if not target_sheet.sheet_view:
            target_sheet.sheet_view = SheetView()
        target_sheet.sheet_view.showGridLines = source_sheet.sheet_view.showGridLines

def main():
    st.title("Excel 文件解析器（支持多工作表、编辑和保存，保留格式）")

    # 文件上传
    uploaded_file = st.file_uploader("选择一个Excel文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件名
        st.write("文件名:", uploaded_file.name)

        # 读取Excel文件中的所有工作表
        xlsx = pd.ExcelFile(uploaded_file)
        sheet_names = xlsx.sheet_names

        # 为每个工作表创建一个选项卡
        tabs = st.tabs(sheet_names)

        # 创建一个字典来存储所有工作表的DataFrame
        all_dfs = {}

        # 遍历每个工作表
        for i, sheet_name in enumerate(sheet_names):
            with tabs[i]:
                # 读取当前工作表，不使用第一行作为列名
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
                all_dfs[sheet_name] = df

                # 显示工作表名称
                st.subheader(f"工作表: {sheet_name}")

                # 使用编辑功能显示数据框
                edited_df = st.data_editor(df)
                all_dfs[sheet_name] = edited_df

                # 显示基本统计信息
                st.write("基本统计信息:")
                st.write(edited_df.describe())

        # 添加保存功能
        new_filename = st.text_input("输入新的文件名（不包括扩展名）:", value=uploaded_file.name.split('.')[0])
        if st.button("保存修改后的Excel"):
            if new_filename:
                # 创建一个临时文件
                with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    # 复制原始文件以保留格式
                    uploaded_file.seek(0)
                    workbook = load_workbook(uploaded_file)
                    
                    # 更新每个工作表的数据，同时保留格式
                    for sheet_name, df in all_dfs.items():
                        if sheet_name in workbook.sheetnames:
                            sheet = workbook[sheet_name]
                            workbook.remove(sheet)
                        new_sheet = workbook.create_sheet(title=sheet_name)
                        
                        # 处理 <NA> 值
                        df = df.replace({pd.NA: np.nan})
                        
                        # 写入所有数据，包括第一行
                        for r_idx, row in enumerate(df.itertuples(index=False), 1):
                            for c_idx, value in enumerate(row, 1):
                                if pd.isna(value):  # 处理 NaN 值
                                    value = None
                                new_sheet.cell(row=r_idx, column=c_idx, value=value)
                        
                        # 复制原始格式
                        if sheet_name in xlsx.sheet_names:
                            original_sheet = load_workbook(uploaded_file)[sheet_name]
                            copy_sheet_format(original_sheet, new_sheet)
                    
                    # 保存修改后的工作簿
                    workbook.save(tmp.name)
                    
                    # 读取临时文件的内容
                    with open(tmp.name, "rb") as file:
                        excel_data = file.read()
                
                # 提供下载按钮
                st.download_button(
                    label=f"下载修改后的Excel文件",
                    data=excel_data,
                    file_name=f"{new_filename}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success(f"文件已保存为 {new_filename}.xlsx")
            else:
                st.error("请输入有效的文件名")


main()