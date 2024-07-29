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

# Initialize AWS client
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
        return True
    except Exception as e:
        st.error(f"Error updating parameter: {str(e)}")
        return False

def fetch_parameters():
    if st.session_state.path:
        with st.spinner("Fetching parameters..."):
            st.session_state.parameters = get_parameters_by_path(st.session_state.path)
        if st.session_state.parameters:
            st.success(f"Found {len(st.session_state.parameters)} parameters")
        else:
            st.warning("No parameters found for the given path.")
        for param in st.session_state.parameters:
            param_key = f"param_{param['Name']}"
            if param_key not in st.session_state:
                st.session_state[param_key] = {
                    'editing': False,
                    'value': param['Value']
                }
    else:
        st.warning("Please enter a valid path.")

def toggle_edit(param):
    param_key = f"param_{param['Name']}"
    st.session_state[param_key]['editing'] = not st.session_state[param_key]['editing']

def update_param_value(param):
    param_key = f"param_{param['Name']}"
    new_value = st.session_state[f"input_{param['Name']}"]
    with st.spinner("Updating parameter..."):
        if update_parameter(param['Name'], new_value):
            st.session_state[param_key]['value'] = new_value
            st.session_state[param_key]['editing'] = False
            st.success(f"Parameter {param['Name']} updated successfully!")
        else:
            st.error(f"Failed to update parameter {param['Name']}")

def cancel_edit(param):
    param_key = f"param_{param['Name']}"
    st.session_state[param_key]['editing'] = False

def calculate_text_area_height(text):
    # Calculate height based on content length, with a minimum of 100 and maximum of 400
    return min(max(100, len(text) // 2), 400)

# st.set_page_config(page_title="AWS Parameter Store Manager", layout="wide")

st.title("AWS Parameter Store Manager")
st.write("Manage your AWS Parameter Store parameters with ease")

# Initialize session state
if 'parameters' not in st.session_state:
    st.session_state.parameters = []
if 'path' not in st.session_state:
    st.session_state.path = ""

# Input for parameter path
st.session_state.path = st.text_input("Enter Parameter Store Path:", value=st.session_state.path, placeholder="/your/parameter/path")
fetch_button = st.button("Fetch Parameters", on_click=fetch_parameters, use_container_width=True)

# Main content area
if st.session_state.parameters:
    st.header("Parameters")
    for param in st.session_state.parameters:
        with st.expander(f"{param['Name']}", expanded=True):
            param_key = f"param_{param['Name']}"
            
            if st.session_state[param_key]['editing']:
                new_value = st.text_area(
                    "Value",
                    value=st.session_state[param_key]['value'],
                    key=f"input_{param['Name']}",
                    height=calculate_text_area_height(st.session_state[param_key]['value'])
                )
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("Update", key=f"update_{param['Name']}", use_container_width=True):
                        update_param_value(param)
                with col2:
                    if st.button("Cancel", key=f"cancel_{param['Name']}", use_container_width=True):
                        cancel_edit(param)
            else:
                st.text_area(
                    "Value",
                    value=st.session_state[param_key]['value'],
                    key=f"display_{param['Name']}",
                    disabled=True,
                    height=calculate_text_area_height(st.session_state[param_key]['value'])
                )
                if st.button("Edit", key=f"edit_{param['Name']}", use_container_width=True):
                    toggle_edit(param)
else:
    st.info("No parameters fetched yet. Enter a path and click 'Fetch Parameters' to begin.")

# Footer
st.markdown("---")
st.markdown("Made with Streamlit")

# Display session_state in real-time
st.header("Session State")

session_state_dict = {
    'path': st.session_state.path,
    'parameters': [
        {
            'Name': param['Name'], 
            'Value': st.session_state[f"param_{param['Name']}"]['value'],
            'Editing': st.session_state[f"param_{param['Name']}"]['editing']
        } 
        for param in st.session_state.parameters
    ]
}

st.json(json.dumps(session_state_dict, indent=2))