import networkx as nx

from app.models.schemas import (
    AccountMatch,
    AggregatedProfile,
    ConnectionEdge,
    MentionMatch,
    PhotoMatch,
)
from app.services.confidence import score_account_confidence


def build_profile(
    primary_identifier: str,
    accounts: list[AccountMatch],
    mentions: list[MentionMatch],
    photos: list[PhotoMatch],
    username: str | None = None,
) -> AggregatedProfile:
    dedup_accounts: dict[str, AccountMatch] = {}
    for account in accounts:
        updated = account
        if username:
            updated.confidence = score_account_confidence(username, account.url)
        dedup_accounts[f"{updated.platform}:{updated.url}"] = updated

    dedup_mentions = {(m.source, m.url): m for m in mentions}
    dedup_photos = {(p.source, p.url): p for p in photos}

    graph = nx.Graph()
    graph.add_node(primary_identifier)

    edges: list[ConnectionEdge] = []
    for account in dedup_accounts.values():
        graph.add_node(account.url)
        graph.add_edge(primary_identifier, account.url, relation="account")
        edges.append(ConnectionEdge(source=primary_identifier, target=account.url, relation="account"))

    for mention in dedup_mentions.values():
        graph.add_node(mention.url)
        graph.add_edge(primary_identifier, mention.url, relation="mention")
        edges.append(ConnectionEdge(source=primary_identifier, target=mention.url, relation="mention"))

    for photo in dedup_photos.values():
        graph.add_node(photo.url)
        graph.add_edge(primary_identifier, photo.url, relation="photo")
        edges.append(ConnectionEdge(source=primary_identifier, target=photo.url, relation="photo"))

    risk_notes = [
        "Results are probabilistic and must be human-verified.",
        "Use only with lawful purpose and documented consent.",
        "Do not use outputs for harassment, stalking, or discrimination.",
    ]

    return AggregatedProfile(
        primary_identifier=primary_identifier,
        accounts=list(dedup_accounts.values()),
        mentions=list(dedup_mentions.values()),
        photo_matches=list(dedup_photos.values()),
        graph_edges=edges,
        risk_notes=risk_notes,
    )
