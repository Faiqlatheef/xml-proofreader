import streamlit as st
import tempfile
import difflib

from app.cli import process_file

st.set_page_config(page_title="XML Proofreader", layout="wide")

st.title("🧠 XML Proofreader (GenAI) by Faiq")
st.write("Upload XML and Style Guide to detect and correct errors")

xml_file = st.file_uploader("Upload XML File", type=["xml"])
style_file = st.file_uploader("Upload Style Guide (DOCX)", type=["docx"])

lang = st.selectbox("Language", ["en"])

# Helper: highlight <error> tags
def highlight_errors(xml_text):
    import re

    def replacer(match):
        content = match.group(0)
        return f'<span style="background-color:#ffcccc; padding:2px;">{content}</span>'

    return re.sub(r"<error.*?>.*?</error>", replacer, xml_text)


if st.button("🚀 Process"):
    if xml_file and style_file:

        with st.spinner("Processing..."):

            # Save input
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as f:
                f.write(xml_file.read())
                xml_path = f.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as f:
                f.write(style_file.read())
                style_path = f.name

            output_path = xml_path.replace(".xml", ".corrected.xml")

            # Run pipeline
            process_file(xml_path, style_path, lang, output_path)

            # Read files
            with open(xml_path, "r", encoding="utf-8") as f:
                original = f.read()

            with open(output_path, "r", encoding="utf-8") as f:
                corrected = f.read()

        st.success("✅ Processing complete!")

        # 🔥 SIDE BY SIDE VIEW
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Original XML")
            st.code(original, language="xml")

        with col2:
            st.subheader("✅ Corrected XML (Highlighted)")
            highlighted = highlight_errors(corrected)
            st.markdown(highlighted, unsafe_allow_html=True)

        # 🔥 DIFF VIEW
        st.subheader("🔍 Differences (Before vs After)")

        diff = difflib.HtmlDiff().make_file(
            original.splitlines(),
            corrected.splitlines(),
            fromdesc="Original",
            todesc="Corrected"
        )

        st.components.v1.html(diff, height=500, scrolling=True)

        # 🔥 DOWNLOAD
        st.download_button(
            "📥 Download Corrected XML",
            corrected,
            file_name="corrected.xml",
            mime="text/xml"
        )

    else:
        st.warning("Please upload both XML and Style Guide.")