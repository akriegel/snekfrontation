"""
Define the `InputResponse` class to contain the values for input retrieved from
a user based on an `InputRequest`.
"""


class InputResponse:
    """
    Class to hold data from a user response to an input request.
    """

    def __init__(self, data):
        self.data = data
