import streamlit as st
import papermill as pm
import nbformat
from nbconvert import HTMLExporter
import tempfile
import os

st.title("📊 Notebook Runner with Papermill")

uploaded_file = st.file_uploader("Upload notebook (.ipynb)", type=["ipynb"])

if uploaded_file is not None:
    # Tạo file tạm lưu input notebook
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb") as tmp_in:
        tmp_in.write(uploaded_file.read())
        input_path = tmp_in.name

    # Tạo file tạm lưu output notebook sau khi chạy xong
    output_path = input_path.replace(".ipynb", "_executed.ipynb")

    try:
        st.info("Đang chạy notebook... ⏳")

        # Thực thi notebook bằng papermill
        pm.execute_notebook(input_path, output_path, kernel_name="python3")

        st.success("Chạy notebook thành công ✅")

        # Đọc output notebook đã thực thi
        with open(output_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Render ra HTML bằng nbconvert
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(nb)

        # Hiển thị HTML trong Streamlit
        st.components.v1.html(body, height=1200, scrolling=True)

    except Exception as e:
        st.error(f"Có lỗi khi chạy notebook: {str(e)}")

    # Xóa file tạm
    os.remove(input_path)
    os.remove(output_path)
