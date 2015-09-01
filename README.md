# zmatrix-to-inp
Easily convert DASH Z-matrices into TOPAS rigid bodies

#### Requires:
- [Python 2.7](https://www.python.org/)          
 Other versions of Python may also work, but this has not been tested.

#### Settings:
###### use_H_atoms_in_restraints = False

Toggles the inclusion of hydrogen atoms when mapping the rigid bodies onto the DASH solution

###### beq_for_nonH = "bnonH;"

When refining a single global B iso value for non-hydrogen atoms, set to "bnonH;", otherwise, set to a numerical value of your choice. Remember to include the parameter definition in the inp. For example:

`prm bnonH 1`

This will automatically be refined.

###### beq_for_H = "bH;"

When refining a single global B iso value for hydrogens, set to "bH;", otherwise, set to a numerical value of your choice. Remember to include the parameter definition in the inp. This can be an independent parameter, or set in relation to the bnonH parameter, e.g.:

`prm bH = bnonH * 1.2;`

###### include_torsion_refinement_macro = True

Automatically inserts a macro definition to toggle the refinement of torsion angles, and places the macro name (see below) in the rigid body for torsion angles flagged as refineable by DASH.

###### torsion_refinement_macro_name = "R"

Allows the user to define their own macro name for torsion angle refinement.
