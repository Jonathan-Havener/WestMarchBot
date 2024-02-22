import re


class Quest:
    def __init__(self, dm, level_range, players, adventure_date):
        self.dm = dm
        self.level_range = level_range
        self.players = players
        self.adventure_date = adventure_date


import pickle
def load_info():
    filename = "thread_data.pkl"
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def generate_quest_objects():
    with open("thread_data.pkl", "rb") as f:
        data = pickle.load(f)

    pattern = r"le?ve?ls? ?(\d)-?(?:(\d)|\+)"

    quest_objs = []

    for quest in data:
        if not re.search(pattern, quest, re.IGNORECASE):
            continue
        level_duple = re.findall(pattern, quest, re.IGNORECASE)[0]
        level_range = range(int(level_duple[0]), int(level_duple[1]) + 1) \
            if level_duple[1] \
            else range(int(level_duple[0]), 12 + 1)
        dm = data[quest].owner
        message_authors = [message["author"] for message in data[quest].messages]
        players = set(message_authors)

        quest_objs.append(Quest(dm=dm, level_range=level_range, players=players, adventure_date=data[quest].created_at))

    return quest_objs


import matplotlib.pyplot as plt
def generate_level_histograms():
    quest_objs = generate_quest_objects()
    levels = [(num, quest.adventure_date) for quest in quest_objs for num in quest.level_range]
    level_list = sorted(set(level for level, _ in levels))

    for level in level_list:
        level_data = [date for l, date in levels if l == level]
        plt.figure(figsize=(6, 3))
        plt.hist(level_data, bins=12, alpha=0.5)
        plt.title(f'Frequency of Level {level} Over Time')
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    print("Done")

# level_ranges = [re.findall(pattern, quest, re.IGNORECASE)[0] for quest in data if
#                 re.search(pattern, quest, re.IGNORECASE)]
# level_ranges = [range(level_range[0], level_range[1]) if level_range[1] else range(level_range[0], 12)
#                 for level_range in level_ranges]
