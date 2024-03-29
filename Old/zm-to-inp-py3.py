import sys
import os
import re

'''
Converts a DASH z-matrices to the correct format for use with rigid body
Rietveld refinements in Topas.

USAGE:
Call the script on its own and be prompted to supply the filenames of z-matrices
to convert, or supply the filenames via command line arguments, e.g.

python zm-to-inp.py filename1.zmatrix filename2.zmatrix filename3.zmatrix

'''

use_H_atoms_in_restraints = False
beq_for_H = "bH;"
beq_for_nonH = "bnonH;"
include_torsion_refinement_macro = True
torsion_refinement_macro_name = "R"

# Check an entered file name and extension to see if it exists, and if not, prompt for one.
def checkfilename(file, extension):
    question = "Enter name of "+extension+" file: "
    if file == None:
        file = input(question)
        file2 = file.rpartition('.') # Check to see if the full filename has been entered or just the root (without mol2 extension)
        if len(file2[2]) < 1:
            file = file+extension
        elif file2[2] == file:
            file = file+extension
        else:
            if file2[2] != extension[1:]:
                print("You must supply a file with the correct extension! Unknown extension:",file2[2])
    else:
        if file.rpartition(".")[2] == file:
            file = file+extension
        if file.rpartition(".")[2] != extension[1:]:
            print(file.rpartition("."))
            print("You must supply a file with the correct extension! Unknown extension:","."+file.rpartition(".")[2],"for file",file)
            print("Autocorrecting to",extension)
            file = file.rpartition(".")[0]+extension
    while not os.path.exists(file):
        print("\nCannot find file with name",file,"\nPlease double check and try again, or type exit to quit.")
        file = input(question)
        if file == "exit":
            exit()
        else:
            file2 = file.rpartition('.') # Check to see if the full filename has been entered or just the root (without mol2 extension)
            if file2[2] == file:
                file = file+extension
            elif len(file2[2]) < 1:
                file = file+extension
            else:
                if file2[2] != extension[1:]:
                    print("You must supply a file with the correct extension! Unknown extension:",file2[2])
    return file

# Read a z-matrix and convert to the topas z-matrix format. Also extracts a list of atom labels and checks for unique atom labels.
def read_zmatrix(filename):
    i = 0
    atom_labels = []
    topas_zm = ["{:<12}".format("rigid")]
    with open(filename, "r") as ZM_in:
        for line in ZM_in:
            line = list(filter(None,line.strip().split(" ")))
            if i > 2:
                atom_labels.append(line[13])
                # First line of topas ZM has the first atom only - line[13]
                if i == 3:
                    topas_zm.append("{:<15}{:<9}".format('   z_matrix',line[13]+'Z'))
                # Second line introduces a new atom (line[14]) and a bond length - line[1]
                if i == 4:
                    topas_zm.append("{:<15}{:<9}{:<9}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1]))
                # Third atom (line[15]), so need bond length and angle - line[1], line[3]
                if i == 5:
                    topas_zm.append("{:<15}{:<9}{:<9}{:<15}{:<9}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1],line[15]+'Z',line[3]))
                # Now requires fourth atom (line[16]) and therefore bond length, angle and torsion angle - line[1], line[3], line[5]
                if i > 5:
                    if include_torsion_refinement_macro == True:
                        if line[6] == "1":
                            topas_zm.append("{:<15}{:<9}{:<9}{:<15}{:<9}{:<15}{:<9}{:<9}{:<15}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1],line[15]+'Z',\
                            line[3],line[16]+'Z',torsion_refinement_macro_name,line[5],"\'Refineable torsion"))
                        else:
                            topas_zm.append("{:<15}{:<9}{:<9}{:<15}{:<9}{:<15}{:<9}{:<9}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1],line[15]+'Z',\
                            line[3],line[16]+'Z',"",line[5]))
                    else:
                        if line[6] == "1":
                            topas_zm.append("{:<15}{:<9}{:<9}{:<15}{:<9}{:<15}{:<15}{:<15}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1],line[15]+'Z',\
                            line[3],line[16]+'Z',line[5],"\'Refineable torsion"))
                        else:
                            topas_zm.append("{:<15}{:<9}{:<9}{:<15}{:<9}{:<15}{:<15}{:<15}".format('   z_matrix',line[13]+'Z',line[14]+'Z',line[1],line[15]+'Z',\
                            line[3],line[16]+'Z',line[5]))
            i+=1
    ZM_in.close()
    unique_atom_labels = set(atom_labels)
    if len(unique_atom_labels) != len(atom_labels):
        print("\n\nDUPLICATE ATOM LABELS FOUND IN Z-MATRIX! ATOMS MUST HAVE UNIQUE LABELS TO WORK IN TOPAS.")
        print("\nUnique atom labels: ",len(unique_atom_labels))
        print("Number of atoms supplied: ", len(atom_labels))
        for item in unique_atom_labels:
            atom_labels.remove(item)
        print("Duplicate(s) found: ", atom_labels)
        exit("\nEXITING")
    return topas_zm, atom_labels

# Check that a supplied string is an element and if not, warn user and allow them to correct it.
def is_element(element):
    elements = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc",\
                "Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb",\
                "Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm",\
                "Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl",\
                "Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md",\
                "No","Lr","Rf","Db","Sg","Bh","Hs","Mt"]
    if element not in elements:
        print("Unknown element",element,". Please modify the inp with correct site occupant before use in Topas")
        element = input("If you wish to modify the element now, please enter the symbol for the element, or leave blank to continue: ")
        if len(element) == 0:
            pass
        else:
            element = is_element(element)
    return element

# Get the site labels for topas, and then create the list of distance restraints for z-matrix mapping
def get_sites_and_restraints(atom_labels):
    site_list = []
    distance_restraints = []

    for item in atom_labels:
        if len(re.findall("[a-z]",item)) > 0:
            element = re.findall("[A-Z]",item)[0]+re.findall("[a-z]",item)[0]
        else:
            element = re.findall("[A-Z]",item)[0]
        element = ''.join(element)
        element = is_element(element)

        if element == "H":
            beq = beq_for_H
        else:
            beq = beq_for_nonH

        site_format = "{: <5}{: <7}{: <15}{: <3}{: <10}"
        site_entry = site_format.format("site",item+"Z","x  0  y  0  z  0   occ  ",element,"1.0   beq = "+beq)
        site_list.append("{: <60}".format(site_entry))

        distance_restraints_format = "{: <15}{: <9}{: <9}{: <10}"
        if ((use_H_atoms_in_restraints == True) or (element != "H")):
            distance_restraints.append(distance_restraints_format.format('Distance_Restrain(',item,item+'Z,','0,0,0,1)'))

    return site_list, distance_restraints

# Main function, includes code for writing out the final topas inp file
def converter_main():
    # Specify z-matrices for conversion via command line arguments, or prompt user for the filenames if not supplied.
    files = []
    if len(sys.argv) == 1:
        try:
            number = int(input("Enter number of Z-matrices to convert: "))
        except:
            print("You did not enter a number! Please try again")
            exit()
        for i in range(0,number):
            filename = checkfilename(None,".zmatrix")
            files.append(filename)
    else:
        for filename in sys.argv[1:]:
            filename = checkfilename(filename,".zmatrix")
            files.append(filename)

    # Read each Z-matrix and store the required information in a list called "all_info"
    all_info = []
    rotate_translate = ['rotate @ 0 qa 1','rotate @ 0 qb 1','rotate @ 0 qc 1','translate ta @ 0','translate tb @ 0','translate tc @ 0']
    i = 0
    for filename in files:
        topas_zm, atom_labels = read_zmatrix(filename)
        site_list, distance_restraints = get_sites_and_restraints(atom_labels)
        if i == 0:
            all_info.append([['\''+filename+' - site list\n']+site_list+['\n'],
				['\''+filename+' - rigid body\n']+topas_zm+['\n']+rotate_translate+['\n'],\
            ["\'Once Z-matrix mapping is complete, delete all lines below this one"]+['\''+filename+' - mapping restraints\n']+distance_restraints+['\n']])
        else:
            all_info.append([['\''+filename+' - site list\n']+site_list+['\n'],
			['\''+filename+' - rigid body\n']+topas_zm+['\n']+rotate_translate+['\n'],\
            ['\''+filename+' - mapping restraints\n']+distance_restraints+['\n']])
        i+=1

    # Create an output name based on the input filenames
    outname = ""
    for filename in files:
        outname += filename.partition(".zmatrix")[0]+"_"
    outname +='rigid-body.inp'

    with open(outname, "w") as output_inp:
        output_inp.write("\'Once Z-matrix mapping is complete, delete all lines above this one that begin with the keyword \'site\'\n\n")
        if include_torsion_refinement_macro == True:
            output_inp.write("macro "+torsion_refinement_macro_name+" {}   \' insert @ symbol between curly brackets to toggle torsion refinement, i.e. {@}\n\n")
        i = 0
        while i < len(all_info[0]):
            for entry in all_info:
                for line in entry[i]:
                    output_inp.write(str(line)+"\n")
            i+=1
        output_inp.write("only_penalties\n\nchi2_convergence_criteria 0.000001\n\nOut_CIF_STR(\"mapped_ZMs.cif\")")

    output_inp.close()

    print('\nSuccess. File written to ', outname)

if __name__ == "__main__":
    converter_main()
