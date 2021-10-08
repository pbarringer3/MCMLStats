import names
import random


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
    pass


if __name__ == "__main__":
    pass
