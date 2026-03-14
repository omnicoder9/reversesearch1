import re
from dataclasses import dataclass

import phonenumbers

from app.models.schemas import InputType, SearchInput

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


@dataclass
class ParsedInput:
    kinds: list[InputType]
    normalized: dict[str, str]


def parse_search_input(payload: SearchInput) -> ParsedInput:
    kinds: list[InputType] = []
    normalized: dict[str, str] = {}

    if payload.username:
        kinds.append(InputType.USERNAME)
        normalized["username"] = payload.username.strip().lower()

    if payload.email and EMAIL_REGEX.match(payload.email):
        kinds.append(InputType.EMAIL)
        normalized["email"] = payload.email.strip().lower()

    if payload.phone:
        try:
            parsed = phonenumbers.parse(payload.phone, None)
            if phonenumbers.is_valid_number(parsed):
                kinds.append(InputType.PHONE)
                normalized["phone"] = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                )
        except phonenumbers.NumberParseException:
            pass

    if payload.full_name:
        kinds.append(InputType.NAME)
        normalized["full_name"] = payload.full_name.strip().lower()

    if payload.photo_url:
        kinds.append(InputType.PHOTO_URL)
        normalized["photo_url"] = str(payload.photo_url)

    return ParsedInput(kinds=kinds, normalized=normalized)
