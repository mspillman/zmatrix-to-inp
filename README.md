# zmatrix-to-inp

The code in this repository has been completely rewritten, and I have also written a convenient web app to save you from having to download the script and run it locally. It can be accessed here:

[https://zm-to-inp.streamlit.app/](https://zm-to-inp.streamlit.app/)

Contact markspillman *at* gmail.com for queries.

#### Requires:
- Python 3.x for zmatrixtoinp.py

The output file is for use with [TOPAS](https://www.bruker.com/products/x-ray-diffraction-and-elemental-analysis/x-ray-diffraction/xrd-software/overview/topas.html) which is also available with an [academic license](http://www.topas-academic.net/)

#### Settings:
###### B for non H atoms = "bnonH"

When refining a single global B-iso value for non-hydrogen atoms, set to "bnonH" by default, or your preferred variable name if you want to change this. If running the code locally, supply the keyword argument `bnonH` to the Zmatrix class during initialisation of the object. You may also prefer to set it to a numerical value of your choice (e.g. `bnonH = 3`). When using the global B-iso value, you also need to remember to include the parameter definition in the inp. For example:

`prm bnonH 1`

This will automatically be refined.

###### B for H atoms = "bH"

When refining a single global B iso value for hydrogens, set to `bH` or your preferred variable name. Otherwise, it can be set to a numerical value of your choice. Remember to include the parameter definition in the inp. This can be an independent parameter, or set in relation to the bnonH parameter, e.g.:

`prm bH = bnonH * 1.2;`

###### refinement_macro = "R"

Allows the user to define their own macro name for torsion angle refinement. Default is "R". This will automatically be placed adjacent to freely rotating torsion angles, and the macro will be defined at the start of the output of the script/web app. This should also be supplied to the Zmatrix class during initialisation as the keyword argument `refinement_macro`.

###### useH = True

Toggles the inclusion of hydrogen atoms when mapping the rigid bodies onto the DASH solution. Allowed settings are True or False. This should also be supplied to the Zmatrix class during initialisation as the keyword argument `useH`.
#### Local script usage:

If you accept the default settings for all settings described above, call the script from the directory containing the Z-matrices you wish to convert, and supply the filenames as command line arguments. To convert the Z-matrices "test_1.zmatrix" and "test_2.zmatrix" you would run the following command:

`python zm-to-inp.py test_1.zmatrix test_2.zmatrix`

It will write out a file called "map_ZMs.inp" which can then be used as described in the instructions for use with TOPAS below.

Alternatively, start a python interpreter or write a simple script and write something like the following:

```python
from zmatrixtoinp import Zmatrix
files = ["test_1.zmatrix", "test_2.zmatrix"]
ZMs = []
# First read in the Z-matrices, and create Zmatrix objects for each one
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = f.readlines()
    zm = Zmatrix(name=file)
    zm.read_zmatrix(data)
    ZMs.append(zm)
# Now loop over each ZM and write out the new sites and rigid bodies.
# If it is the first ZM, we will want to output a bit of extra information for
# the CIF, hence the call to the zm.first_ZM_output() method
for i, zm in enumerate(ZMs):
    if i == 0:
        inp = zm.first_ZM_output()
    inp += zm.write_rigid_body()
# Now loop over the ZMs again, this time outputting the distance restraints to
# map the rigid bodies onto the CIF atom sites
for i, zm in enumerate(ZMs):
    inp += zm.write_distance_restraints(header=i==0)
inp += zm.final_ZM_output()
# Finally, write the resultant .inp to disk
with open("map_ZMs.inp","w", encoding="utf-8") as f:
    f.writelines(inp)
print("Success: map_ZMs.inp written")
```



#### Output file

The script writes out a file with the ".inp" extension, into the working directory. By default, the filename is "map_ZMs.inp".

#### Instructions for use with TOPAS

The following instructions assume a basic familiarity with TOPAS used via launch mode. For more detailed information, see the TOPAS manual and excellent [tutorials by John Evans](https://topas.webspace.durham.ac.uk/).

1. Once the crystal structure has been solved as normal, save the solution as a .cif and create a TOPAS Rietveld refinement input file. Perform a scale-factor-only Rietveld refinement to ensure everything has worked correctly. The easiest way to do this is to use the [Durham TOPAS jEdit tools](https://topas.webspace.durham.ac.uk/) to set up the .inp file and to read in the .cif.

2. Once the scale-only Rietveld .inp file has been created and has been run successfully, use DASH, [which is now available for free](https://github.com/ccdc-opensource/dash), to create Z-matrices **from the solution .cif** - this is important as it means the Z-matrices contain the same torsion angles found in the solution. Once these Z-matrices have been obtained, use this web app to convert them into the correct TOPAS format. Download the resultant .inp file, and open it in a text editor. Copy and paste the contents of the whole file to the bottom of the scale-only Rietveld .inp file. Save this as "map-zmatrices.inp".

3. The next step is to map the rigid bodies onto the solution. To do this, we need to run the "map-zmatrices.inp" file you just saved. This will map the Z-matrices onto the solution atom sites, and will automatically generate a .cif to make it easy to check for successful mapping. Once the .inp has run, first check that the mapping has been successful.
    - Look at the final Rwp for this run - it should be (almost) zero at the end of the refinement.
    - Open the newly created cif that is generated by TOPAS - "mapped_ZMs.cif" to check that the rigid bodies have been mapped onto the DASH solution. For example, using Mercury, open the CIF then select the "Label Atoms" option. If the only atoms visible have the letter Z after them, then the mapping has been successful.

4. If the mapping completed successfully, open the map-zmatrices.out file in a text editor. Delete the original atom sites (i.e. those that were in the original scale only Rietveld file which do not end with a "Z") and delete all of the distance restraints, the "only_penalties" keyword and the "Out_CIF_STR("mapped_ZMs.cif") line. Once this has been done, save the file as "rigid_body_refinement.inp" and continue with the refinement. The app adds comments to make it easier to find and delete the correct sections of the file.

5. Rigid-body based Rietveld refinement can now proceed using the newly created rigid_body_refinement.inp as the basis.