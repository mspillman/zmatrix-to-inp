import streamlit as st
from zmatrixtoinp import Zmatrix

st.title("Z-matrix to inp converter")
"""Upload Z-matrix files and get TOPAS rigid bodies. Z-matrices must be in DASH
format. To use this tool, you should first [solve](https://github.com/mspillman/gallop)
the crystal structure of interest, then generate a DASH formatted Z-matrix
**from that solution** before proceeding.

DASH is now open-source and freely available
[here](https://github.com/ccdc-opensource/dash).
It is able to convert a variety of crystallographic formats to Z-matrices."""

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