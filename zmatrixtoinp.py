class Zmatrix(object):
    """
    Read a DASH Z-matrix and convert to a TOPAS rigid body
    """
    def __init__(self,name=None):
        self.name = name
        self.bond = []
        self.angle = []
        self.torsion = []
        self.atom1 = []
        self.atom2 = []
        self.atom3 = []
        self.atom4 = []
        self.refine = []
        self.element = []
        self.occupancy = []

    def read_zmatrix(self,zmatrix):
        """
        Read the DASH formatted Z-matrix

        Args:
            zmatrix (list): A list of strings, with each corresponding to one
                line in the input z-matrix. Effectively, this is the output of
                f.readlines() where f is the Z-matrix
        """
        for i, line in enumerate(zmatrix):
            if i > 2:
                line = list(filter(None, line.strip().split(" ")))
                if len(line) > 0:
                    self.element.append(line[0])
                    self.bond.append(line[1])
                    self.angle.append(line[3])
                    self.torsion.append(line[5])
                    self.refine.append("R" if line[6] == "1" else "")
                    self.occupancy.append(line[11])
                    self.atom1.append(line[13])
                    if i > 3:
                        self.atom2.append(line[14])
                    if i > 4:
                        self.atom3.append(line[15])
                    if i > 5:
                        self.atom4.append(line[16])

    def first_ZM_output(self):
        """
        Writes the preamble for the output .inp assuming that this is the first
        in a set of Z-matrices that need to be mapped onto the sites

        Returns:
            list: A list containing strings corresponding to the output lines of
                    the TOPAS .inp
        """
        output = [
            "\'Once Z-matrix mapping is complete, delete all lines above this one that begin with the keyword \'site\'\n",
            "macro R {}   \' insert @ symbol between curly brackets to toggle torsion refinement, i.e. {@}\n\n"
            ]
        return output

    def write_rigid_body(self, output=None):
        """
        Writes out a TOPAS rigid body using the information from the Z-matrix

        Args:
            output (list): This is a list of strings, which will eventually be
                written to a .inp file.

        Returns:
            list: A list containing strings corresponding to the output lines of
                    the TOPAS .inp
        """
        if output is None:
            output = []
        output.append(f"\n\'{self.name} - site list\n\n")
        for i, atom in enumerate(self.atom1):
            atom += "Z"
            site = f"site {atom:<5}       x  0  y  0  z  0      occ {self.element[i]:<2}  {self.occupancy[i]}      beq = bnonH;\n"
            output.append(site)
        output.append(f"\n\n\'{self.name} - rigid body\n")
        output.append("\nrigid\n")
        for i, atom in enumerate(self.atom1):
            atom += "Z"
            site = f"    z_matrix   {atom:<7}"
            if i > 0:
                atom2 = self.atom2[i-1]+"Z"
                site += f"{atom2:<7} {self.bond[i]:<14}"
            if i > 1:
                atom3 = self.atom3[i-2]+"Z"
                site += f"{atom3:<7} {self.angle[i]:<14}"
            if i > 2:
                atom4 = self.atom4[i-3]+"Z"
                site += f"{atom4:<7} {self.refine[i]:<3} {self.torsion[i]}"
            else:
                site = "    " + site.strip() # tidy up trailing white space
            site += "\n"
            output.append(site)
        output.append("\nrotate @ 0 qa 1\n")
        output.append("rotate @ 0 qb 1\n")
        output.append("rotate @ 0 qc 1\n")
        output.append("translate ta @ 0\n")
        output.append("translate tb @ 0\n")
        output.append("translate tc @ 0\n")
        return output

    def write_distance_restraints(self, output=None, header=False):
        """
        Writes the distance restraints for each of the atom pairs (original and
        Z-matrix), which TOPAS uses to map the rigid bodies onto the atom sites

        Args:
            output (list): _description_. Defaults to None.
            header (bool, optional): Write a hint to the reader to delete the
                following lines once mapping is complete. Only needed for the
                first Z-matrix. Defaults to False.

        Returns:
            list: A list containing strings corresponding to the output lines of
                    the TOPAS .inp
        """
        if output is None:
            output = []
        if header:
            output.append("\n\n\'Once Z-matrix mapping is complete, delete all lines below this one\n")
        output.append(f"\n\'{self.name} - mapping restraints\n\n")
        for atom in self.atom1:
            atomz = atom+"Z"
            site = f"Distance_Restrain({atom:<7} {atomz},  0,0,0,1)\n"
            output.append(site)
        return output

    def final_ZM_output(self, output):
        output.append("\n\nonly_penalties\n")
        output.append("\nchi2_convergence_criteria 0.000001\n")
        output.append("\nOut_CIF_STR(\"mapped_ZMs.cif\")")
        return output

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) == 1:
        print("You must supply at least one Z-matrix as an argument")
    else:
        files = []
        for filename in sys.argv[1:]:
            if filename.rsplit(".", maxsplit=1)[-1] == "zmatrix":
                if os.path.isfile(filename):
                    files.append(filename)
                else:
                    raise FileNotFoundError(filename)
            else:
                print(f"Unrecognized file extension for {filename}")
        ZMs = []
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                data = f.readlines()
            zmatrix = Zmatrix(name=file)
            zmatrix.read_zmatrix(data)
            ZMs.append(zmatrix)
        for i, zm in enumerate(ZMs):
            if i == 0:
                output = zm.first_ZM_output()
            output = zm.write_rigid_body(output)
        for i, zm in enumerate(ZMs):
            output = zm.write_distance_restraints(output, i==0)
        output = zm.final_ZM_output(output)
        with open("map_ZMs.inp","w", encoding="utf-8") as f:
            f.writelines(output)
        print("Success: map_ZMs.inp written")