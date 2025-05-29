import streamlit as st

st.set_page_config(page_title="Apple Style Calculator", layout="centered")

st.markdown(
    """
    <style>
    .calculator {
        background-color: #000;
        border-radius: 20px;
        padding: 20px;
        max-width: 300px;
        margin: auto;
    }
    .display {
        background-color: #1c1c1c;
        color: white;
        font-size: 48px;
        text-align: right;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .button-row {
        display: flex;
        margin-bottom: 10px;
    }
    .button {
        flex: 1;
        font-size: 24px;
        padding: 20px;
        margin: 2px;
        border: none;
        border-radius: 50%;
        background-color: #333;
        color: white;
        cursor: pointer;
    }
    .button.operator {
        background-color: #f39c12;
        color: white;
    }
    .button.function {
        background-color: #a5a5a5;
        color: black;
    }
    .button.zero {
        flex: 2;
        border-radius: 50px;
        text-align: left;
        padding-left: 35px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Layout using HTML (Streamlit doesn't support full grid-style UI)
def render_button(label, css_class="", span2=False):
    if st.button(label, key=label, use_container_width=True):
        handle_input(label)
    return f'<button class="button {css_class}{" zero" if span2 else ""}">{label}</button>'

# Handle logic
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

# Display calculator
st.markdown('<div class="calculator">', unsafe_allow_html=True)
st.markdown(f'<div class="display">{st.session_state.expression or "0"}</div>', unsafe_allow_html=True)

# Button layout
buttons = [
    [("C", "function"), ("", ""), ("", ""), ("/", "operator")],
    [("7", ""), ("8", ""), ("9", ""), ("*", "operator")],
    [("4", ""), ("5", ""), ("6", ""), ("-", "operator")],
    [("1", ""), ("2", ""), ("3", ""), ("+", "operator")],
    [("0", "", True), (".", ""), ("=", "operator")]
]

for row in buttons:
    cols = st.columns([2 if span else 1 for _, _, *span in row])
    for col, (label, css_class, *span) in zip(cols, row):
        if label:
            with col:
                st.markdown(
                    f"""
                    <form action="" method="post">
                        <input type="hidden" name="button" value="{label}">
                        <button type="submit" class="button {css_class}{' zero' if span else ''}">{label}</button>
                    </form>
                    """,
                    unsafe_allow_html=True
                )
        else:
            col.empty()
st.markdown("</div>", unsafe_allow_html=True)
