import hmac
import resource
import streamlit as st
import subprocess
import tf2onnx
import netron
from utils.differential_testing import *
import streamlit.components.v1 as components
import threading
import time

st.set_page_config(
    page_title="HomePage",
    page_icon="🏠",
)

def set_limits():
    # Limit the process to use a maximum of 1 CPU second
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    
    # Limit the process to a maximum memory usage of 100MB
    resource.setrlimit(resource.RLIMIT_AS, (100*1024*1024, 100*1024*1024))

def execute_code_safely(code: str) -> tuple:
    if st.session_state["current_user"] == 'admin':
        preexec_fn = None
    else:
        preexec_fn = set_limits
    try:
        # Using a separate python executable to run the code
        result = subprocess.run(
            ["python3", "-c", code],
            stdout=subprocess.PIPE,     # Capture standard output
            stderr=subprocess.PIPE,     # Capture standard error
            preexec_fn=preexec_fn,      # Set resource limits before executing
            timeout=100                   # Kill the process if it runs for more than 5 seconds
        )
        
        # Return the combined stdout and stderr
        return (result.stdout.decode("utf-8"), result.stderr.decode("utf-8"))

    except subprocess.TimeoutExpired:
        return ("", "Execution timed out!")
    except Exception as e:
        return ("", f"Error: {str(e)}")
    
def execute_model_safely(code: str) -> tuple:
    return ("", "")

def check_password():
    """Returns `True` if the user had a correct password."""
    
    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.session_state["current_user"] = None
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["current_user"] = st.session_state["username"]
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

def fetch_version_number(option):
    if option == 'TensorFlow':
        return '2.16.0.dev20231101'
    elif option == 'PyTorch':
        return '2.2.0'
    elif option == 'TVM':
        return '0.15.dev0'

def show_model(model_path, port):
    #netron.start(model_path, address=("127.0.0.1", port), browse=True)
    components.iframe(f"http://localhost:{port}", height=500, scrolling=True)
    
def main():
    st.title("🕵️‍♂️ TensorScope -- Deep Learning Infra Fuzzing Platform")
    
    # option = st.selectbox('Target Framework', ('TensorFlow', 'PyTorch', 'TVM'))
    # st.write(f'{option} version: {fetch_version_number(option)}')
    
    is_authed = check_password()
    st.write(f'Current user: {st.session_state["current_user"]}')
    
    api = st.text_input("Enter an API that you want to test here:", placeholder="tf.dynamic_stitch")
    source_framework = st.selectbox(
    'Select the source framework',
    ('TensorFlow', 'PyTorch', 'MindSpore', 'ONNX',))
    target_framework = st.selectbox(
    'Select the target framework',
    ('ONNX', 'MindSpore', 'PyTorch', 'TensorFlow',))
    st.write(f"🧪 between {source_framework} 🆚 {target_framework}")
    if st.button("Find Counterparts & Constraints"):
        if is_authed == False: 
            st.error("😕 You need to authenticate first.")
            return
        #m1, m2 = gen_model_pair(api, source_framework, target_framework)
        m1 = "onnx_test/tf_model/tf.raw_ops.AdjustContrastv2_frozen_graph.pb"
        m2 = "onnx_test/onnx_model/tf.raw_ops.AdjustContrastv2_model.onnx"
        st.write("This is the 1st computational graph.")
        
        def display_netron(path, port):
            os.system(f'netron {path} -p {port}')
    
        thread = threading.Thread(target=display_netron, args=(m1,8081))
        thread.start()
        time.sleep(1)
        show_model(m1, 8081)
        
        st.write("This is the 2nd computational graph.")
        
        thread = threading.Thread(target=display_netron, args=(m2,8082))
        thread.start()
        time.sleep(1)
        show_model(m2, 8082)
        # Execute code and display output (to be implemented in next steps)
        # output, err = execute_code_safely(code)
        # st.text_area("Output", value=output, height=300, max_chars=None)
        # st.text_area("Error", value=err, height=300, max_chars=None)
    
    # code = st.text_area("Enter a DL model that you want to test here:")
    if st.button("Start Differential Testing"):
        if is_authed == False: 
            st.error("😕 You need to authenticate first.")
            return
        # Execute code and display output (to be implemented in next steps)
        # output, err = execute_model_safely(code)
        # st.text_area("Output", value=output, height=300, max_chars=None)
        # st.text_area("Error", value=err, height=300, max_chars=None)
        with open("onnx_test/onnx_fuzz_log/onnx_test.log", 'r') as f:
            log = f.read()
        st.text_area("Output", value=log, height=300, max_chars=None)

if __name__ == "__main__":
    main()
