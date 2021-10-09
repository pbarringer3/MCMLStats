import pandas as pd
import os
from pandas.core.frame import DataFrame


# Define string constants
LAST_NAME = "Last Name"
FIRST_NAME = "First Name"
GRADE = "Grade"
SCHOOL = "School"
TOTAL = "Total Points"
COUNT = "# of Students"
RATINGS = "Category Rating"
RAT_SUM = "Rating Sum"
RAT_A = "Rating A"
RAT_B = "Rating B"
FINAL_RATING = "Final Individual Rating"

KEY = [LAST_NAME, FIRST_NAME, GRADE, SCHOOL]


def calculate_stats(filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """ Reads in the csv file provided and returns two DataFrames, first, one
    corresponding to the provided file with an additional column representing
    the students' ratings for the given meet, second, one with the category
    stats. """

    # Define the columns used for scoring
    START_COL = 4
    END_COL = 9

    # Load the data
    meet_data = pd.read_csv(filename)
    columns_to_save = meet_data.keys()

    # Get the categories and rate them
    categories = list(columns_to_save[START_COL:END_COL+1])
    category_dict = {}
    category_dict["Category"] = categories
    category_dict[COUNT] = [meet_data[category].count()
                            for category in categories]
    category_dict[TOTAL] = [meet_data[category].sum()
                            for category in categories]

    category_dict[RATINGS] = \
        [meet_data[category].sum()/meet_data[category].count() * 5
            for category in categories]

    # Get the sum of each student's points
    meet_data[TOTAL] = meet_data[categories].sum(axis=1)

    # Map played categories to 1 and unplayed to 0
    categories_played = meet_data[categories].notnull().astype(int)

    # Create a Series to use for dot-product to find the sum of 3 category
    # ratings for each student amd store in original DataFrame
    rating_series = pd.Series(category_dict[RATINGS], index=categories)
    rating_sum = categories_played.dot(rating_series)
    meet_data[RAT_SUM] = rating_sum

    # Calculate Rating A, Rating B, and Final Rating
    meet_data[RAT_A] = meet_data[TOTAL] / meet_data[RAT_SUM]
    meet_data[RAT_B] = (meet_data[categories] / rating_series).sum(axis=1) / 3
    meet_data[FINAL_RATING] = (meet_data[RAT_A] + meet_data[RAT_B]) / 2

    # Add the rating to the columns I want to return
    final_rating_index = pd.Index([FINAL_RATING])
    columns_to_save = columns_to_save.append(final_rating_index)

    # Name return data in a readable way
    student_data = meet_data[columns_to_save]
    category_data = pd.DataFrame.from_dict(category_dict)

    return student_data, category_data


def create_meet_file(year: int, meet: int, categories: list[str]) -> None:
    """ Looks for an existing roster and creates a csv file for the given meet
    based on this roster and the categories provided. The file can then be
    edited in any spreadsheet editor. All the columns for scores will be blank.
    The columns for last name, first name, grade, and school will be retained
    from the roster file.

    If the directory doesn't exist yet for the year, this function creates it.

    Safeguards against accidentally overwriting existing data by seeing if the
    file already exists. If it does, the function raises a FileExistsError.
    If the user wants a new file, they must manually delete the old file first.

    The existing roster is a requirement. If there isn't one in the current
    year, this function will look to the previous year and update all the
    students' grades, creating a new roster file for this year. If the previous
    year also doesn't have a roster, a FileNotFoundError is raised. """
    directory = str(year)
    filename = f'Meet {meet}.csv'

    # Check for directory and create if needed.
    if not os.path.exists(directory):
        os.mkdir(directory)

    # Check for file to prevent it being overwritten.
    # Provide error message in this case.
    relative_file_path = f'./{directory}/{filename}'
    if os.path.exists(relative_file_path):
        raise FileExistsError(
            "A file for this meet already exists.\n\nIf you wish to replace "
            "it, you must delete the existing file manually before creating "
            "the new one with this program.\n\nYou can find the existing file "
            f"in the {directory} directory. It will be titled '{filename}'.")

    # Get the roster, provide error if one doesn't exist
    roster: DataFrame
    roster_filename = 'roster.csv'
    current_roster_path = f'./{directory}/{roster_filename}'
    previous_roster_path = f'./{int(directory)-1}/{roster_filename}'

    if os.path.exists(current_roster_path):
        roster = pd.read_csv(current_roster_path)

    # Otherwise get and update the previous year's roster
    elif os.path.exists(previous_roster_path):
        roster = pd.read_csv(previous_roster_path)
        roster = update_grades(roster)
        roster.to_csv(f'./{directory}/{roster_filename}', index=False)

    # If neither exist, they need to create a roster first.
    else:
        raise FileNotFoundError(
            f"No roster file was found.\n\nPlease check the {directory} or "
            f"{int(directory)-1} directories for a file titled "
            f"'{roster_filename}'.\n\nIf such a file doesn't exist, it must "
            "be created manually.\n\nDirections for creating this file can be "
            "found in the file 'README.md' which can be opened with any text "
            "editor or online at https://github.com/pbarringer3/MCMLStats.")

    # Add columns for the categories
    roster[categories] = None

    # Write the desired contents to the file.
    roster.to_csv(relative_file_path, index=False)


def create_reports(year: int, meet: int) -> None:
    """ This function triggers the analasys of the provided file and the
    creation of all the files and reports needed for the given meet. """
    directory = str(year)
    filename = f'Meet {meet}.csv'

    scores_path = f'./{directory}/{filename}'
    # Check directory and file existence
    if not os.path.exists(scores_path):
        raise FileNotFoundError(
            "Meet Data Not Found\n\nIn order to calculate the stats for the "
            "requested meet, the program looks in its own directory for a "
            f"folder named '{year}' and a file in that folder named "
            f"'{filename}'.\n\nThe directory structure is fundamental to this "
            "program's execution and must be followed. You can read more in "
            "the file 'README.md' which can be opened with any text editor "
            "or online at https://github.com/pbarringer3/MCMLStats.")

    # Create subdirectory for reports and data files.
    subdirectory = f'./{directory}/Meet {meet}'
    prefix = f'{subdirectory}/Meet {meet}'
    if not os.path.exists(subdirectory):
        os.mkdir(subdirectory)
    else:
        raise FileExistsError(
            "Existing Folder Error\n\nThis program will create a subfolder in "
            f"the {directory} folder called 'Meet {meet}' along with all of "
            "its contents. Please remove or rename the existing folder "
            f"'Meet {meet}' in the {directory} folder.")

    # Analyze file
    student_data, category_data = calculate_stats(scores_path)

    # Create csv file with student scores and ratings
    ratings_path = f'{prefix} with Student Ratings.csv'
    student_data.to_csv(ratings_path, index=False)

    # Create csv file with category ratings
    category_path = f'{prefix} Category Ratings.csv'
    category_data.to_csv(category_path, index=False)

    # Create csv file with just roster and ratings for the year
    update_annual_ratings(student_data, year, meet)

    # Generate all pdf reports
    generate_reports()

    # Create backup of old roster file if it exists
    roster_path = f'./{directory}/roster.csv'
    if os.path.exists(roster_path):
        new_roster_path = f'{prefix} Roster Backup.csv'
        os.rename(roster_path, new_roster_path)

    # Create updated roster file based on this meet's students
    student_data[KEY].to_csv(roster_path, index=False)


def generate_reports():
    pass


def update_annual_ratings(student_data: pd.DataFrame, year: int,
                          meet: int) -> None:
    """ Creates a file comprised of each student with their ratings for each
    meet along with columns for their average rating and averages with dropped
    meet(s)."""
    personal_with_rating = KEY + [FINAL_RATING]
    prefix = f'./{year}/Cumulative Ratings - Meet'
    out_path = f'{prefix} {meet}.csv'
    renamed = {FINAL_RATING: f'Meet {meet} Rating'}
    data_out = student_data[personal_with_rating].rename(columns=renamed)

    # If Meet 1, just create with personal info and this meet rating
    if meet == 1:
        data_out.to_csv(out_path, index=False)
        return

    # Check for previous ratings file existence.
    previous_path = f'{prefix} {meet-1}.csv'
    if not os.path.exists(previous_path):
        raise FileNotFoundError(
            "Cumulative Ratings File Error\n\nThe cumulative ratings file from"
            f" Meet {meet-1} wasn't found in the {year} folder. You should be "
            "able to recover from this error by rerunning the stats for any "
            "meets that are missing their cumulative data files.\n\nRemember, "
            "No statistics files in this folder or any subfolders should be "
            "deleted. They are very small files and aren't taking up an "
            "appreciable amount of hard drive space.\n\nIf you can't figure "
            "out how to recover from this error, contact the program designer "
            "at patrick.barringer@gmail.com"
        )

    # Open previous ratings, merge with current ratings, and save to csv
    previous_ratings = pd.read_csv(previous_path)
    merged = pd.merge(previous_ratings, data_out, on=KEY, how='outer')
    merged.to_csv(out_path, index=False)


def update_grades(roster: pd.DataFrame) -> pd.DataFrame:
    """ This function removes all the seniors from the roster
    DataFrame and adds a year to all the remaining students' grades."""
    roster = roster[roster['Grade'] != 12]
    roster['Grade'] = roster['Grade'] + 1
    return roster


if __name__ == '__main__':
    update_annual_ratings(pd.DataFrame(), '1')
