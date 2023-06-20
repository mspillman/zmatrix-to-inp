import streamlit as st
from zmatrixtoinp import Zmatrix

st.title("Z-matrix to inp converter")
with st.sidebar:
    option = st.radio("Options",["Converter","Instructions"])

if option == "Instructions":
    with open("Instructions.md", "r") as f:
        instructions = f.read()
    st.markdown(instructions)
else:

    st.write("## Upload files")
    st.write("You can upload multiple Z-matrices simultaneously")

    uploaded_file = st.file_uploader("Choose a file","zmatrix",
                                        accept_multiple_files=True)
    if len(uploaded_file) > 0:
        # To read file as bytes:
        ZMs = []
        for item in uploaded_file:
            data = item.getvalue().decode().split("\n")
            zmatrix = Zmatrix(name=item.name)
            zmatrix.read_zmatrix(data)
            ZMs.append(zmatrix)
        for i, zm in enumerate(ZMs):
            if i == 0:
                output = zm.first_ZM_output()
            output = zm.write_rigid_body(output)
        for i, zm in enumerate(ZMs):
            output = zm.write_distance_restraints(output, i==0)
        output = zm.final_ZM_output(output)
        with open("map_ZMs.inp","w") as f:
            f.writelines(output)
        st.download_button(
            label="Download inp",
            data = "".join(output),
            file_name = "map_ZMs.inp",
            mime="text"
            )