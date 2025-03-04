import csv
import json


def convert_to_csv(people):
    with open('../src/results/people.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Grade', '55m', '200m', '300m', '400m', '600m', '800m', '1000m', '1200m', '1600m', '1609m (mile)', '3200m'])
        for name in people:
            person = people[name]
            writer.writerow([name, person['grade'], person.get('55m', ''), person.get('200m', ''), person.get('300m', ''), person.get('400m', ''), person.get('600m', ''), person.get('800m', ''), person.get('1000m', ''), person.get('1200m', ''), person.get('1600m', ''), person.get('1609m', ''), person.get('3200m', '')])

def convert_top_5_to_csv(top_per_event):
    # Get all unique events
    events = list(top_per_event.keys())

    # Prepare rows where each row contains (name, time) pairs per event
    max_rows = max(len(top_per_event[event]) for event in events)
    rows = []

    for i in range(max_rows):
        row = []
        for event in events:
            if i < len(top_per_event[event]):
                row.append(top_per_event[event][i]["name"])
                row.append(top_per_event[event][i]["time"])
            else:
                row.extend(["", ""])  # Empty placeholders if fewer than max rows
        rows.append(row)

    # Write to CSV
    with open("../src/results/top_5", "w", newline="") as f:
        writer = csv.writer(f)

        # Write header
        header = []
        for event in events:
            header.extend([event, ""])
        writer.writerow(header)

        # Write data rows
        writer.writerows(rows)


def save_people_json(people, suffix=''):
    os.makedirs('../src/results', exist_ok=True)
    with open(f'../src/results/people{suffix}.json', 'w') as file:
        json.dump(people, file, indent=4)

def save_top_5_json(top_per_event, suffix=''):
    os.makedirs('../src/results', exist_ok=True)
    with open(f'../src/results/top_5{suffix}.json', 'w') as file:
        json.dump(top_per_event, file, indent=4)

def save_top_relays(top_relays, suffix=''):
    os.makedirs('../src/results', exist_ok=True)
    with open(f'../src/results/top_relays{suffix}.json', 'w') as file:
        json.dump(top_relays, file, indent=4)