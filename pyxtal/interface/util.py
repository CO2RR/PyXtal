from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from ase import Atoms

"""
scripts to perform structure conformation
"""
def pymatgen2ase(struc):
    atoms = Atoms(symbols = struc.atomic_numbers, cell = struc.lattice.matrix)
    atoms.set_scaled_positions(struc.frac_coords)
    return atoms

def ase2pymatgen(struc):
    lattice = struc._cell
    coordinates = struc.get_scaled_positions()
    species = struc.get_chemical_symbols()
    return Structure(lattice, species, coordinates)

def symmetrize_cell(struc, mode='C'):
    """
    symmetrize structure from pymatgen, and return the struc in conventional/primitive setting
    Args:
    struc: ase type
    mode: output conventional or primitive cell
    """
    P_struc = ase2pymatgen(struc)
    finder = SpacegroupAnalyzer(P_struc,symprec=0.06,angle_tolerance=5)
    if mode == 'C':
        P_struc = finder.get_conventional_standard_structure()
    else:
        P_struc = finder.get_primitive_standard_structure()

    return pymatgen2ase(P_struc)

def good_lattice(struc):
    maxvec = 25.0
    minvec = 2.5
    maxangle = 150
    minangle = 30
    para = struc.get_cell_lengths_and_angles()
    if (max(para[:3])<maxvec) and (max(para[3:])<maxangle) and (min(para[3:])>minangle):
        return True
    else:
        return False


