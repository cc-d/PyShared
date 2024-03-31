class NotPrintableError(ValueError):
    """
    Raised when an object's __str__ and __repr__ methods both fail.

    ~obj: The problematic object, failing to print.
    ~str_error: Original exception from __str__ method failure.
    ~repr_error: Original exception from __repr__ method failure.
    -> None
    """

    def __init__(self, obj, str_error, repr_error):
        self.obj = obj
        self.str_error = str_error
        self.repr_error = repr_error
        self.message = (
            "<NotPrintableError: {obj_type} (ID: {obj_id}) "
            "__str__ error: {str_err}, __repr__ error: {repr_err}>".format(
                obj_type=type(self.obj).__name__,
                obj_id=id(self.obj),
                str_err=repr(self.str_error),
                repr_err=repr(self.repr_error),
            )
        )
        super().__init__(self.message)

    def __repr__(self):
        return self.message  # pragma: no cover
