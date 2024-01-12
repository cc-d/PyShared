class NotPrintableError(Exception):
    """Custom exception to be raised when both repr and str fail"""

    def __init__(self, obj, e_repr, e_str):
        self.obj_type = type(obj)
        self.repr_exception = e_repr
        self.str_exception = e_str
        self.message = (
            "<NotPrintable {obj_type} object repr_exception={e_repr!r} "
            "str_exception={e_str!r}>".format(
                obj_type=self.obj_type, e_repr=e_repr, e_str=e_str
            )
        )
        super().__init__(self.message)
