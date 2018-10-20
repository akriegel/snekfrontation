"""
Define the `InputRequest` class for passing requests for user input from the
game logic up to IO.
"""

from typing import Callable, Generic, List, Tuple, TypeVar


# Generic type variable
T = TypeVar("T")
Failure = Tuple[bool, str]


class InputRequest(Generic[T]):
    """
    A class to represent a single instance of required user input, including
    functions to parse the actual value from a string and an input validator,
    along with their error types.

    Usage should be like this:

        # from game
        request = InputRequest(parser, parse_err, validator, validate_err)
        # from handler; loop until
        result = request.call().validate().result

    """

    def __init__(
        self,
        parser: Callable[[str], T],
        parse_err_type: type,
        validator: Callable[[T], Failure],
        validation_err_type: type,
        msg: str = '',
        suggest_inputs: List[str] = None,
    ):
        """
        Args:
            parser: function to convert string input to the final input type
            parse_err_type: exception to raise if parse fails
            validator: function to check input value is valid
            validation_err_type: exception to raise if validation fails
            msg: informative message used to ask for input
            suggest_inputs: list of suggested inputs (not enforced)
        """
        self._parser = parser
        self.parse_err = parse_err_type
        self._validator = validator
        self.validation_error = validation_err_type
        self.msg = msg
        self.suggestions = suggest_inputs or []

    def parse(self, input_string: str) -> T:
        return self._parser(input_string)

    def validate(self, value: T):
        """
        Check that a value given to satisfy the request is valid, otherwise
        raise the validation error provided at init.
        """
        success, msg = self._validator(value)
        if not success:
            raise self._validation_err(msg)
        return self
