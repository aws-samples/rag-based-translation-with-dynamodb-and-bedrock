import streamlit as st
import hmac
import yaml
import os

yaml_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(yaml_path, 'r') as f:
    config_data = yaml.safe_load(f)

def _check_password():
    """Authenticate user and manage login state."""
    if st.session_state.get("authenticated"):
        return True

    with st.form("Credentials"):
        st.title("Amazon LLM Translate Tool")
        st.caption("尝鲜版 用户名：:blue[demo_user] 密码: :blue[demo_password123]")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
        st.info(f"需要支持请联系 {config_data['support']}")

    if submitted:
        if username in st.secrets["passwords"] and hmac.compare_digest(
            password,
            st.secrets.passwords[username],
        ):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = st.secrets.roles.get(username, "user")  # Default to "user" if role not specified
            st.rerun()
        else:
            st.error("User not known or password incorrect.")

    return False


def _authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("home.py", label="Amazon Bedrock Translate", icon="⚧")
    st.sidebar.page_link("pages/user.py", label="File Translate", icon="🚎")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Dictionary Term Config", icon="🔑")
        # st.sidebar.page_link(
        #     "pages/super-admin.py",
        #     label="Translation PE Config",
        #     icon="🎛",
        #     disabled=st.session_state.role != "super-admin",
        # )
    st.sidebar.divider()
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    st.sidebar.write(f"Your role is: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        _logout()
        
    st.sidebar.divider()
    st.sidebar.info(f"需要支持请联系 {config_data['support']}")


def _unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    # st.sidebar.page_link("home.py", label="Log in")
    pass

def _logout():
    """Log out the current user."""
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    st.rerun()


def menu():
    # Determine if a user is logged in or not, then show the correct
    if not _check_password():
        _unauthenticated_menu()
        st.stop()
    else:
        _authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if not _check_password():
        st.switch_page("home.py")
    menu()
    
