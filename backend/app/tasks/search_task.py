from app.core.celery_app import celery_app
from app.models.schemas import SearchInput
from app.services.aggregator import build_profile
from app.services.input_parser import parse_search_input
from app.services.search_modules import (
    search_email,
    search_name,
    search_phone,
    search_photo,
    search_username,
)


@celery_app.task(name="search.execute")
def execute_search(payload: dict) -> dict:
    parsed_payload = SearchInput(**payload)
    parsed = parse_search_input(parsed_payload)

    accounts = []
    mentions = []
    photos = []

    username = parsed.normalized.get("username")
    if username:
        accounts.extend(search_username(username, parsed_payload.platform))

    email = parsed.normalized.get("email")
    if email:
        mentions.extend(search_email(email))

    full_name = parsed.normalized.get("full_name")
    if full_name:
        mentions.extend(search_name(full_name))

    phone = parsed.normalized.get("phone")
    if phone:
        mentions.extend(search_phone(phone))

    photo_url = parsed.normalized.get("photo_url")
    if photo_url:
        photos.extend(search_photo(photo_url))

    primary_identifier = (
        username
        or email
        or phone
        or full_name
        or photo_url
        or "unknown"
    )

    profile = build_profile(
        primary_identifier=primary_identifier,
        accounts=accounts,
        mentions=mentions,
        photos=photos,
        username=username,
    )
    return profile.model_dump()
