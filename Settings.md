##### B for non H atoms = "bnonH"

When refining a single global B-iso value for non-hydrogen atoms, set to "bnonH" by default, or your preferred variable name if you want to change this. If running the code locally, supply the keyword argument `bnonH` to the Zmatrix class during initialisation of the object. You may also prefer to set it to a numerical value of your choice (e.g. `bnonH = 3`). When using the global B-iso value, you also need to remember to include the parameter definition in the inp. For example:

`prm bnonH 1`

This will automatically be refined.

##### B for H atoms = "bH"

When refining a single global B iso value for hydrogens, set to `bH` or your preferred variable name. Otherwise, it can be set to a numerical value of your choice. Remember to include the parameter definition in the inp. This can be an independent parameter, or set in relation to the bnonH parameter, e.g.:

`prm bH = bnonH * 1.2;`

##### refinement_macro = "R"

Allows the user to define their own macro name for torsion angle refinement. Default is "R". This will automatically be placed adjacent to freely rotating torsion angles, and the macro will be defined at the start of the output of the script/web app. This should also be supplied to the Zmatrix class during initialisation as the keyword argument `refinement_macro`.

##### useH = True

Toggles the inclusion of hydrogen atoms when mapping the rigid bodies onto the DASH solution. Allowed settings are True or False. This should also be supplied to the Zmatrix class during initialisation as the keyword argument `useH`.