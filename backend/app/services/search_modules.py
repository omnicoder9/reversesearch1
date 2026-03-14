from app.models.schemas import AccountMatch, MentionMatch, PhotoMatch

# Mock sources only. Replace with official APIs in production.
KNOWN_PLATFORMS = {
    "x": "https://x.com/{username}",
    "github": "https://github.com/{username}",
    "instagram": "https://instagram.com/{username}",
    "linkedin": "https://www.linkedin.com/in/{username}",
}


def search_username(username: str, platform: str | None = None) -> list[AccountMatch]:
    targets = [platform.lower()] if platform and platform.lower() in KNOWN_PLATFORMS else KNOWN_PLATFORMS.keys()
    out: list[AccountMatch] = []
    for p in targets:
        url = KNOWN_PLATFORMS[p].format(username=username)
        base = 90 if platform and p == platform.lower() else 72
        out.append(
            AccountMatch(
                platform=p,
                url=url,
                confidence=base,
                rationale="Exact handle pattern match from public profile URL template.",
            )
        )
    return out


def search_email(email: str) -> list[MentionMatch]:
    domain = email.split("@")[-1]
    return [
        MentionMatch(
            source="Public Paste Monitor",
            title=f"Potential mention tied to {domain}",
            url=f"https://example.org/search?q={email}",
            snippet="Email-like artifact found in public indexing source.",
            confidence=65,
        )
    ]


def search_name(full_name: str) -> list[MentionMatch]:
    query = full_name.replace(" ", "+")
    return [
        MentionMatch(
            source="Web Index",
            title=f"Public mention for {full_name.title()}",
            url=f"https://example.org/search?q={query}",
            snippet="Name match found in a public profile-like page.",
            confidence=58,
        )
    ]


def search_phone(phone: str) -> list[MentionMatch]:
    return [
        MentionMatch(
            source="Phone Metadata",
            title="Carrier/region metadata",
            url=f"https://example.org/phone/{phone}",
            snippet="Public metadata lookup candidate.",
            confidence=54,
        )
    ]


def search_photo(photo_url: str) -> list[PhotoMatch]:
    return [
        PhotoMatch(
            source="Image Similarity Index",
            url=photo_url,
            confidence=61,
        )
    ]
