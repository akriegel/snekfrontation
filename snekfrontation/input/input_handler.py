"""
Define the `InputHandler` class for accepting input requests from the game
logic and returning user input (or mock input for tests, etc.).
"""

from abc import ABC, abstractmethod

from snekfrontation.input.input_request import InputRequest
from snekfrontation.input.input_response import InputResponse


class InputHandler(ABC):
    """
    ABC to define the typeclass for input handling.
    """

    @abstractmethod
    def request(self, request: InputRequest) -> InputResponse:
        """
        Process an input request.
        """
        pass

    @abstractmethod
    def complain(self, msg):
        """
        Complain to the user that their input was wrong. (Don't include asking
        for new input.)
        """
        pass
