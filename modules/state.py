import copy
import json
from pathlib import Path

from modules.extraction import refresh_incident_metadata


MERGE_FIELDS = [
    "incident_type",
    "location_text",
    "last_seen_time",
    "victim_count",
    "weather_or_field_condition",
    "access_notes",
]


def load_state(path: str) -> dict | None:
    state_path = Path(path)
    if not state_path.exists():
        return None
    return json.loads(state_path.read_text(encoding="utf-8"))


def merge_incidents(previous: dict | None, incoming: dict, raw_text: str = "") -> dict:
    if not previous:
        merged = copy.deepcopy(incoming)
        merged.setdefault("conflicts", [])
        return refresh_incident_metadata(merged, raw_text)

    merged = copy.deepcopy(previous)
    merged.setdefault("conflicts", [])

    for field in MERGE_FIELDS:
        _merge_scalar(merged, incoming, field)

    _merge_coordinates(merged, incoming)
    _merge_nested_scalar(merged, incoming, ["reporter", "name"])
    _merge_nested_scalar(merged, incoming, ["reporter", "contact"])
    _merge_nested_scalar(merged, incoming, ["reporter", "relation"], conflict_on_difference=False)
    _merge_victim_field(merged, incoming, "last_clothing")
    _merge_victim_field(merged, incoming, "condition", conflict_on_difference=False, append_unique=True)
    _merge_victim_field(merged, incoming, "notes", conflict_on_difference=False, append_unique=True)

    return refresh_incident_metadata(merged, raw_text)


def _is_present(value) -> bool:
    return value not in [None, "", [], {}]


def _normalize(value) -> str:
    return str(value).strip().lower()


def _record_conflict(target: dict, field: str, existing, incoming) -> None:
    if not _is_present(existing) or not _is_present(incoming):
        return
    if _normalize(existing) == _normalize(incoming):
        return
    conflict = {
        "field": field,
        "existing": existing,
        "incoming": incoming,
        "status": "needs_officer_resolution",
    }
    if conflict not in target.setdefault("conflicts", []):
        target["conflicts"].append(conflict)


def _merge_scalar(target: dict, incoming: dict, field: str, conflict_on_difference: bool = True) -> None:
    incoming_value = incoming.get(field)
    if field == "incident_type" and incoming_value == "lainnya":
        return
    if not _is_present(incoming_value):
        return
    existing = target.get(field)
    if _is_present(existing) and _normalize(existing) != _normalize(incoming_value):
        if conflict_on_difference:
            _record_conflict(target, field, existing, incoming_value)
        return
    target[field] = incoming_value


def _merge_nested_scalar(target: dict, incoming: dict, path: list[str], conflict_on_difference: bool = True) -> None:
    incoming_value = _get_nested(incoming, path)
    if not _is_present(incoming_value):
        return
    existing = _get_nested(target, path)
    field = ".".join(path)
    if _is_present(existing) and _normalize(existing) != _normalize(incoming_value):
        if conflict_on_difference:
            _record_conflict(target, field, existing, incoming_value)
        return
    _set_nested(target, path, incoming_value)


def _merge_victim_field(
    target: dict,
    incoming: dict,
    field: str,
    conflict_on_difference: bool = True,
    append_unique: bool = False,
) -> None:
    incoming_victim = (incoming.get("victims") or [{}])[0]
    target.setdefault("victims", [{}])
    target_victim = target["victims"][0]
    incoming_value = incoming_victim.get(field)
    if not _is_present(incoming_value):
        return
    existing = target_victim.get(field)
    full_field = f"victims.0.{field}"
    if append_unique and _is_present(existing):
        target_victim[field] = _join_unique(existing, incoming_value)
        return
    if _is_present(existing) and _normalize(existing) != _normalize(incoming_value):
        if conflict_on_difference:
            _record_conflict(target, full_field, existing, incoming_value)
        return
    target_victim[field] = incoming_value


def _merge_coordinates(target: dict, incoming: dict) -> None:
    incoming_coords = incoming.get("coordinates") or {}
    if not _is_present(incoming_coords.get("lat")) or not _is_present(incoming_coords.get("lng")):
        return
    target.setdefault("coordinates", {"lat": None, "lng": None})
    existing = target["coordinates"]
    if _is_present(existing.get("lat")) and (
        existing.get("lat") != incoming_coords.get("lat") or existing.get("lng") != incoming_coords.get("lng")
    ):
        _record_conflict(target, "coordinates", existing, incoming_coords)
        return
    target["coordinates"] = incoming_coords


def _join_unique(existing: str, incoming: str) -> str:
    parts = []
    for value in [existing, incoming]:
        for part in str(value).split(","):
            clean = part.strip()
            if clean and clean.lower() not in [item.lower() for item in parts]:
                parts.append(clean)
    return ", ".join(parts)


def _get_nested(obj: dict, path: list[str]):
    current = obj
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _set_nested(obj: dict, path: list[str], value) -> None:
    current = obj
    for key in path[:-1]:
        current = current.setdefault(key, {})
    current[path[-1]] = value
