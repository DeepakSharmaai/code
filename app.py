import streamlit as st
from summarizer import parse_openapi, generate_summary

st.set_page_config(page_title="API Doc Summarizer", layout="centered")

st.title("📄 API Doc Summarizer")
st.markdown("Upload your OpenAPI (Swagger) YAML file or paste it below:")

# Upload or paste OpenAPI YAML
uploaded_file = st.file_uploader("Upload OpenAPI YAML", type=["yaml", "yml"])
yaml_input = st.text_area("Or paste OpenAPI YAML here")

if uploaded_file:
    yaml_str = uploaded_file.read().decode("utf-8")
elif yaml_input:
    yaml_str = yaml_input
else:
    yaml_str = ""

if yaml_str and st.button("Summarize API"):
    with st.spinner("Parsing and summarizing..."):
        parsed = parse_openapi(yaml_str)
        if parsed:
            summary = generate_summary(parsed)
            st.success("✅ Summary generated")
            st.text_area("📘 API Summary", summary, height=300)
        else:
            st.error("❌ Could not parse the YAML. Please check the syntax.")
