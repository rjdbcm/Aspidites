from ._vendor.pyrsistent import PClass


def safer_type(*args):
    name: str
    bases: tuple
    attributes: dict
    if len(args) < 2:
        raise RuntimeError("Type introspection is not supported.")
    elif len(args) == 2:
        name, attributes = args
        bases = (PClass,)
    else:
        name, bases, attributes = args
        bases = (PClass,) + bases

    return type(name, bases, dict(attributes))
