from pymcl.compile.bcs.bcs import BcsList
from pymcl.compile.bcs.entity import LoadEntityPosition
from pymcl.compile.bcs.stack import EntityPosition


def compile_pos_lookup(bcs_list: BcsList, qual, base):
    bcs_list.append(LoadEntityPosition(bcs_list.entity_locals.index(base), {
       "x": EntityPosition.PosVar.X,
       "y": EntityPosition.PosVar.Y,
       "z": EntityPosition.PosVar.Z
    }[qual]))


def compile_ent_attr_lookup(bcs_list, qual):
    qual = qual.split(".")
    qual_base = qual[0]

    if len(qual) == 2:
        if qual[1] in ["x", "y", "z"]:
            compile_pos_lookup(bcs_list, qual[1], qual_base)
