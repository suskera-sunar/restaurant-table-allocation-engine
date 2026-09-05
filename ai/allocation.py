"""Pure-Python greedy table allocation logic."""


def choose_best_table(tables, party_size, occupied_table_ids=(), preferred_zone=""):
    """Return the tightest available table, or None when no table fits.

    Each table must expose ``capacity`` and ``id``. A ``zone`` attribute is
    optional and is used only as a tie-breaker when a preference is supplied.
    """
    occupied = set(occupied_table_ids)
    candidates = [
        table for table in tables
        if table.id not in occupied and table.capacity >= party_size
    ]
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda table: (
            table.capacity - party_size,
            0 if preferred_zone and table.zone == preferred_zone else 1,
            table.capacity,
            table.id,
        ),
    )
