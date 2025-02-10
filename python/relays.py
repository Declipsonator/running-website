import itertools


def parse_time(time_str):
    """
    Parse a time string in the format 'mm:ss.xx' into seconds (as a float).
    For example, '00:06.68' -> 6.68 and '01:32.06' -> 92.06.
    """
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    else:
        # If the time is given as just seconds
        return float(time_str)


def canonical_team_key(team, legs):
    """
    Create a deduplication key for a given relay team assignment.

    Parameters:
      team: a tuple of athlete names in the order they are assigned to the relay legs.
      legs: a list of events corresponding to each leg (for example, ['2', '2', '4', '8']).

    For any event that appears more than once (e.g. the two "2" legs),
    we ignore the ordering of the athletes by sorting the names assigned to those legs.
    For legs with unique events, we include the athlete name along with its index to preserve ordering.

    Returns:
      A tuple that can be used as a key for deduplication.
    """
    # Build a mapping from event to all indices where it appears.
    event_indices = {}
    for i, event in enumerate(legs):
        event_indices.setdefault(event, []).append(i)

    key_parts = []
    processed_events = set()
    for i, event in enumerate(legs):
        if event in processed_events:
            continue
        indices = event_indices[event]
        if len(indices) > 1:
            # For events that occur more than once, ignore the order:
            sorted_names = tuple(sorted(team[j] for j in indices))
            key_parts.append((event, sorted_names))
        else:
            # For a unique event, include the index (to keep the original order) and the athlete name.
            key_parts.append((i, team[i]))
        processed_events.add(event)
    return tuple(key_parts)


def fastest_relays(athletes, legs, num_relays=5, deduplicate=True):
    """
    Compute the fastest relay combinations.

    Parameters:
      athletes: dict mapping athlete names to a dict of their times (as strings) for each event.
      legs: list of event keys corresponding to each relay leg (e.g., ['2', '2', '4', '8']).
      num_relays: number of top combinations to return.
      deduplicate: if True, combinations that differ only by swapping athletes among identical legs
                   will be treated as the same team.

    Returns:
      A list of tuples (team, total_time), where team is a tuple of tuples (athlete name, time)
      and total_time is the sum (in seconds) of their times.
    """

    # Build eligible candidates for each leg.
    eligible = []
    for leg in legs:
        leg_candidates = []
        for name, record in athletes.items():
            if leg in record:
                try:
                    t = parse_time(record[leg])
                    leg_candidates.append((name, t))
                except Exception:
                    continue
        if not leg_candidates:
            raise ValueError(f"No eligible athletes for leg '{leg}'")
        eligible.append(leg_candidates)

    seen = set()  # to store deduplication keys
    relay_combos = []

    # Generate every possible assignment (one athlete per leg).
    for combo in itertools.product(*eligible):
        names = [entry[0] for entry in combo]
        # Skip combinations that reuse an athlete.
        if len(set(names)) < len(names):
            continue
        total_time = sum(entry[1] for entry in combo)
        team = tuple(combo)

        if deduplicate:
            # Use the canonical key that groups legs with identical events.
            key = canonical_team_key(names, legs)
            if key in seen:
                continue
            seen.add(key)

        relay_combos.append({'team': team, 'total_time': round(total_time, 2)})

    # Sort by total time and return the top N.
    relay_combos.sort(key=lambda x: x['total_time'])
    return relay_combos[:num_relays]