from _vendor.pyrsistent import PClass


def safer_type(*args):
    if len(args) < 3:
        raise RuntimeError("Type introspection is not supported.")

    name: str
    bases: tuple
    attributes: dict

    name, bases, attributes = args
    bases = (PClass,) + bases

    return type(name, bases, attributes)
