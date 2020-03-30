import re

from marshmallow import ValidationError

from api.utilities.messages.serialization import serialization_messages

string_regex = re.compile(r"^[a-zA-Z0-9]+(([' .-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$")


def validate_name(data):
    """
        Checks if given string is at least 1 character and only contains letters,
        numbers and non consecutive fullstops, hyphens, spaces and apostrophes.
        Raises validation error otherwise.
    """
    if data and not re.match(string_regex, data):
        raise ValidationError(serialization_messages['string_characters'])
