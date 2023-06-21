import streamlit as st
from zmatrixtoinp import Zmatrix

st.set_page_config(page_title='ZM to inp', page_icon = ":test_tube:",
                    layout = 'centered', initial_sidebar_state = 'auto')

st.title("Z-matrix to inp converter:")
st.markdown("##### Easily convert from DASH Z-matrices to TOPAS rigid bodies")

with st.sidebar:
    option = st.radio("Options",["Converter","Instructions","About"])

if option == "Instructions":

    with open("Instructions.md", "r") as f:
        instructions = f.read()
    st.markdown(instructions)
elif option == "About":
    """This web app was written by [Mark Spillman](https://mspillman.github.io/blog/).
    The source code is available
    on my github [here](https://github.com/mspillman/zmatrix-to-inp). It can
    also be run as a standalone python script.
    Feel free to submit issues, suggestions and enhancements and I'll do my best
    to help."""
else:

    st.markdown("### Output settings")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bnonH = st.text_input("B for non-H atoms","bnonH")
    with col2:
        bH = st.text_input("B for H atoms", "bH")
    with col3:
        macro = st.text_input("Refinement macro", "R")
    with col4:
        useH = st.checkbox("Use H-atoms in restraints", True)
    st.write("### Upload Z-matrices")
    st.write("You can upload multiple Z-matrices simultaneously")

    uploaded_file = st.file_uploader("Choose a file","zmatrix",
                                        accept_multiple_files=True)
    if len(uploaded_file) > 0:
        # To read file as bytes:
        ZMs = []
        for item in uploaded_file:
            data = item.getvalue().decode().split("\n")
            zmatrix = Zmatrix(name=item.name, bnonH=bnonH, bH=bH,
                            refinement_macro=macro, useH=useH)
            zmatrix.read_zmatrix(data)
            ZMs.append(zmatrix)
        for i, zm in enumerate(ZMs):
            if i == 0:
                output = zm.first_ZM_output()
            output = zm.write_rigid_body(output)
        for i, zm in enumerate(ZMs):
            output = zm.write_distance_restraints(output, i==0)
        output = zm.final_ZM_output(output)
        #with open("map_ZMs.inp","w") as f:
        #    f.writelines(output)
        st.download_button(
            label="Download inp",
            data = "".join(output),
            file_name = "map_ZMs.inp",
            mime="text"
            )