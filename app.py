import streamlit as st
import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell
import base64
import matplotlib
matplotlib.use("Agg")

st.title("📊 Notebook Auto Runner - Full Output")

uploaded_file = st.file_uploader("Upload notebook (.ipynb)", type=["ipynb"])

if uploaded_file is not None:
    nb = nbformat.read(uploaded_file, as_version=4)

    nb.cells.insert(0, new_code_cell("%matplotlib inline"))

    st.write("Đang chạy notebook...")
    client = NotebookClient(nb, kernel_name="python3", timeout=600)
    client.execute()

    st.success("Notebook chạy xong ✅")

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            st.markdown(cell.source)
        elif cell.cell_type == 'code':
            outputs = cell.get('outputs', [])
            for output in outputs:
                if output.output_type in ['execute_result', 'display_data']:
                    data = output.get('data', {})

                    if 'text/markdown' in data:
                        st.markdown(data['text/markdown'])
                    if 'text/plain' in data:
                        st.code(data['text/plain'])
                    if 'image/png' in data:
                        img_bytes = base64.b64decode(data['image/png'])
                        st.image(img_bytes)
                    if 'image/svg+xml' in data:
                        st.image(data['image/svg+xml'], format="svg")
                    if 'text/html' in data:
                        st.components.v1.html(data['text/html'], height=500, scrolling=True)
