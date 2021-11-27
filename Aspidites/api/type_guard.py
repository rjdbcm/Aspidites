from Aspidites._vendor.pyrsistent import PMap
try:
    from .woma.library import final
except ImportError:
    from .final import final


def safer_type(*args):
    name: str
    bases: tuple
    attributes: PMap
    if len(args) < 2:
        raise RuntimeError("Type introspection is not supported.")
    name, attributes = args
    bases = tuple()
    t = type(name, bases, dict(attributes))
    return final()(t)
