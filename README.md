# zmatrix-to-inp

Note - I've just refactorerd the code and tidied things up a lot compared to the spaghetti code that I wrote almost a decade ago! I've also written a convenient web app to save you from having to download the script and run it locally. It can be accessed here:

[https://zm-to-inp.streamlit.app/](https://zm-to-inp.streamlit.app/)

I will update the rest of this README when I get time to reflect the updates.

---

Easily convert DASH Z-matrices into TOPAS rigid bodies

Contact markspillman *at* gmail.com for queries.

#### Requires:
- [Python 2.7](https://www.python.org/) for zm-to-inp.py
- Python 3.x for zm-to-inp-py3.py  
 
 Extremely limited testing has been done for Python 3, but it does seem to work. Feel free to get in touch if it doesn't!

The output file is for use with [TOPAS](https://www.bruker.com/products/x-ray-diffraction-and-elemental-analysis/x-ray-diffraction/xrd-software/overview/topas.html) which is also available with an [academic license](http://www.topas-academic.net/)

#### Settings:
###### use_H_atoms_in_restraints = False

Toggles the inclusion of hydrogen atoms when mapping the rigid bodies onto the DASH solution. Allowed settings are True or False.

###### beq_for_nonH = "bnonH;"

When refining a single global B-iso value for non-hydrogen atoms, set to "bnonH;", otherwise, set to a numerical value of your choice (e.g. `beq_for_nonH = "3"`). When using the global B-iso value, you also need to remember to include the parameter definition in the inp. For example:

`prm bnonH 1`

This will automatically be refined.

###### beq_for_H = "bH;"

When refining a single global B iso value for hydrogens, set to "bH;", otherwise, set to a numerical value of your choice. Remember to include the parameter definition in the inp. This can be an independent parameter, or set in relation to the bnonH parameter, e.g.:

`prm bH = bnonH * 1.2;`

###### include_torsion_refinement_macro = True

Automatically inserts a macro definition to easily allow users to toggle the refinement of torsion angles, and places the macro name (see below) in the TOPAS rigid bodies for torsion angles flagged as refineable by DASH.

###### torsion_refinement_macro_name = "R"

Allows the user to define their own macro name for torsion angle refinement.

#### Script usage:

Call the script from the directory containing the Z-matrices you wish to convert:

`python zm-to-inp.py`

You will then be prompted to supply the filenames of the Z-matrices you wish to convert. Alternatively, you can supply the filenames as command line arguments. To convert the Z-matrices "test_1.zmatrix" and "test_2.zmatrix" you would run the following command:

`python zm-to-inp.py test_1.zmatrix test_2.zmatrix`

#### Output file

The script writes out a file with the ".inp" extension, into the same directory that contains the Z-matrices. The .inp filename is based on the filenames of the Z-matrices converted, with "_rigid-body.inp" appended. For example, if the Z-matrix "test_1.zmatrix" was converted, then the resultant output inp file would be "test_1_rigid-body.inp". Similarly, if the Z-matrices "test_1.zmatrix" and "test_2.zmatrix" were used, then the resultant output file would be "test_1_test_2_rigid-body.inp"

#### Instructions for use with TOPAS

The following instructions assume a basic familiarity with TOPAS used via _launch mode_. For more detailed information, see the TOPAS manual and excellent [tutorials by John Evans](https://community.dur.ac.uk/john.evans/topas_academic/topas_main.htm).

1. Once the crystal structure has been solved using DASH as normal, save the solution as a .cif and create a TOPAS Rietveld refinement input file. Perform a scale-factor-only Rietveld refinement to ensure everything has worked correctly. The easiest way to do this is to use the [Durham TOPAS jEdit tools](https://community.dur.ac.uk/john.evans/topas_academic/topas_main.htm) to set up the .inp file and to read in the .cif. 

2. Once the scale-only Rietveld .inp file has been created and has been run successfully, use DASH to create Z-matrices from the solution .cif - this is important as it means the Z-matrices contain the same torsion angles found in the solution. Once these Z-matrices have been obtained, use zm-to-inp.py to convert them into the correct TOPAS format (see above for instructions for using the script). Open the resultant .inp file in a text editor, then copy and paste the contents of the _whole file_ to the bottom of the scale-only Rietveld .inp file. Save this as "map-zmatrices.inp".

3. The next step is to map the rigid bodies onto the DASH solution. To do this, we need to run the "map-zmatrices.inp" file. This will map the Z-matrices onto the DASH solution atom sites, and will automatically generate a .cif to make it easy to check for successful mapping. Once the .inp has run, first check that the mapping has been successful. 
i. Look at the final Rwp for this run - it should be (almost) zero at the end of the refinement.
ii. Open the newly created cif that is generated by TOPAS - "mapped_ZMs.cif" to check that the rigid bodies have been mapped onto the DASH solution. For example, using Mercury, open the CIF then select the "Label Atoms" option. If the only atoms visible have the letter Z after them, then the mapping has been successful.


4. If the mapping completed successfully, open the map-zmatrices.out file in a text editor. Delete the original atom sites (i.e. those that were in the original scale only Rietveld file which do not end with a "Z") and delete all of the distance restraints, the "only_penalties" keyword and the "Out_CIF_STR("mapped-ZMs.cif") line. Once this has been done, save the file as "rigid_body_refinement.inp" and continue with the refinement. The script will add comments to make it easier to delete the correct sections of the file.
 
5. Rigid-body based Rietveld refinement can now proceed using the newly created rigid_body_refinement.inp as the basis.
