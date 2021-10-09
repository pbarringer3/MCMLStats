import pandas as pd
import names
import random
import os


def generate_fake_roster(file_path: str) -> None:
    schools = ['HA', 'HAC', 'Pittsford-Mendon', 'Greece Olympia',
               'Penfield', 'Brighton']

    with open(file_path, 'w') as outfile:
        outfile.write('Last Name,First Name,Grade,School\n')
        for school in schools:
            for _ in range(10):
                l_name = names.get_last_name()
                f_name = names.get_first_name()
                grade = random.randrange(8, 13)
                outfile.write(f'{l_name},{f_name},{grade},{school}\n')


def generate_test_data(file_path: str) -> None:
    empty_stats = pd.read_csv(file_path)
    categories = empty_stats.keys()[4:10]

    for row in empty_stats.index:
        empty_stats.loc[row, categories] = get_random_score()

    os.remove(file_path)
    empty_stats.to_csv(file_path, index=False)


def get_random_score():
    indices = [x for x in range(6)]
    scores = [None for _ in indices]

    if random.random() > .9:
        return scores

    sample = random.sample(indices, 3)
    for index in sample:
        scores[index] = random.randrange(0, 7)

    return scores


if __name__ == "__main__":
    # generate_fake_roster('./2021/roster.csv')
    generate_test_data('./2021/Meet 2.csv')
