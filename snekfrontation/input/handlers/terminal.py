"""
Define an input handler for simple terminal IO.
"""

from snekfrontation.input.input_handler import InputHandler
from snekfrontation.input.input_request import InputRequest
from snekfrontation.input.input_response import InputResponse


class InputHandlerTerminal(InputHandler):
    """
    Singleton implementing `InputHandler` using text-based input at a terminal.
    """

    def request(self, request: InputRequest) -> InputResponse:
        """
        Process an input request.
        """
        have_valid_input = False
        suggestions = "\n".join("    " + s for s in request.suggestions)
        msg = f"{request.msg}\nSuggested inputs:\n{suggestions}\nInput: "

        while not have_valid_input:
            user_input = input(msg)
            try:
                value = request.parse(user_input)
                request.validate(value)
            except (request.parse_err, request.validation_error) as e:
                self.complain(f"could not parse input: {str(e)}")
            else:
                have_valid_input = True

        return InputResponse(value)

    def complain(self, msg):
        """
        Complain to the user that their input was wrong. (Don't include asking
        for new input.)
        """
        print(msg)
