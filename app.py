import streamlit as st

st.set_page_config(page_title="Apple Style Calculator", layout="centered")

# Inject Apple-style CSS
st.markdown("""
    <style>
    .stButton > button {
        height: 60px;
        width: 60px;
        border-radius: 50%;
        font-size: 24px;
        margin: 4px;
        border: none;
        background-color: #333;
        color: white;
    }
    .stButton > button.operator {
        background-color: #f39c12;
    }
    .stButton > button.function {
        background-color: #a5a5a5;
        color: black;
    }
    .display-box {
        background-color: #1c1c1c;
        color: white;
        font-size: 48px;
        text-align: right;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        height: 80px;
    }
    .button-row {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Logic
def handle_input(label):
    if label == "C":
        st.session_state.expression = ""
    elif label == "=":
        try:
            st.session_state.expression = str(eval(st.session_state.expression))
        except:
            st.session_state.expression = "Error"
    else:
        if st.session_state.expression == "Error":
            st.session_state.expression = ""
        st.session_state.expression += label

# Display
st.markdown(f"<div class='display-box'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

# Button layout
button_rows = [
    [("C", "function"), ("", ""), ("", ""), ("/", "operator")],
    [("7", ""), ("8", ""), ("9", ""), ("*", "operator")],
    [("4", ""), ("5", ""), ("6", ""), ("-", "operator")],
    [("1", ""), ("2", ""), ("3", ""), ("+", "operator")],
    [("0", ""), (".", ""), ("=", "operator")],
]

for row in button_rows:
    cols = st.columns(4)
    for i, (label, style) in enumerate(row + [("", "")] * (4 - len(row))):  # pad if short row
        if label:
            btn_label = f"<span class='{style}'>{label}</span>"
            with cols[i]:
                if st.button(label, key=label):
                    handle_input(label)

