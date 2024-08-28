import streamlit as st
import boto3
from utils.menu import menu_with_redirect
import json

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to super-admins")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")

st.divider()

ssm = boto3.client('ssm')

def get_parameters_by_path(path):
    try:
        response = ssm.get_parameters_by_path(
            Path=path,
            Recursive=True,
            WithDecryption=True
        )
        return response['Parameters']
    except Exception as e:
        st.error(f"Error fetching parameters: {str(e)}")
        return []

def update_parameter(name, value):
    try:
        ssm.put_parameter(
            Name=name,
            Value=value,
            Type='String',
            Overwrite=True
        )
        st.success(f"Parameter {name} updated successfully!")
        return True
    except Exception as e:
        st.error(f"Error updating parameter: {str(e)}")
        return False

def fetch_parameters():
    if st.session_state.path:
        st.session_state.parameters = get_parameters_by_path(st.session_state.path)
        for param in st.session_state.parameters:
            param_key = f"param_{param['Name']}"
            if param_key not in st.session_state:
                st.session_state[param_key] = {
                    'editing': False,
                    'value': param['Value']
                }
    else:
        st.warning("Please enter a valid path.")

def toggle_edit(param_name):
    param_key = f"param_{param_name}"
    st.session_state[param_key]['editing'] = not st.session_state[param_key]['editing']

def update_param_value(param_name):
    param_key = f"param_{param_name}"
    new_value = st.session_state[f"input_{param_name}"]
    if update_parameter(param_name, new_value):
        st.session_state[param_key]['value'] = new_value
        st.session_state[param_key]['editing'] = False

def cancel_edit(param_name):
    param_key = f"param_{param_name}"
    st.session_state[param_key]['editing'] = False

st.title("AWS Parameter Store Manager")

# Initialize session state
if 'parameters' not in st.session_state:
    st.session_state.parameters = []
if 'path' not in st.session_state:
    st.session_state.path = ""

# Input for parameter path
st.session_state.path = st.text_input("Enter Parameter Store Path:", value=st.session_state.path)
st.button("Fetch Parameters", on_click=fetch_parameters)

# Display parameters
for param in st.session_state.parameters:
    st.write(f"**{param['Name']}**")
    param_key = f"param_{param['Name']}"
    
    if st.session_state[param_key]['editing']:
        new_value = st.text_area(
            "Value",
            value=st.session_state[param_key]['value'],
            key=f"input_{param['Name']}"
        )
        col1, col2 = st.columns([1, 1])
        col1.button("Update", key=f"update_{param['Name']}", on_click=update_param_value, args=(param['Name'],))
        col2.button("Cancel", key=f"cancel_{param['Name']}", on_click=cancel_edit, args=(param['Name'],))
    else:
        st.text_area(
            "Value",
            value=st.session_state[param_key]['value'],
            key=f"display_{param['Name']}",
            disabled=True
        )
        st.button("Edit", key=f"edit_{param['Name']}", on_click=toggle_edit, args=(param['Name'],))
    
    st.write("---")  # Separator between parameters