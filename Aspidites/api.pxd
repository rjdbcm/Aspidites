#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
# Aspidites

cdef list wrap_lines(str text, str padchar, int width, list wrapped_lines, int pad)

cdef list wrap(str text, int width, int pad, str padchar)
