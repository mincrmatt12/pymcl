def convert_qual(qual):
    return ".".join(qual.children)


def convert_type(type):
    return "::".join(type.children)


def convert_qual_or_type(qual_or_type):
    return convert_qual(qual_or_type) if qual_or_type.data == "qual" else convert_type(qual_or_type)
