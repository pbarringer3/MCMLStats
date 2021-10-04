import pandas as pd
import tkinter as tk

from ui_elements import MCML_Stats


def main():
    # Create GUI
    root = tk.Tk()
    root.title('MCML Stats')
    stats_frame = MCML_Stats(root)
    stats_frame.mainloop()
    # print(calculate_scores("TestData.csv"))


def calculate_stats(filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    ''' Reads in the csv file provided and returns two DataFrames, first, one
    corresponding to the provided file with an additional column representing
    the students' ratings for the given meet, second, one with the category
    stats.

    filename should be a string ending in .csv
    '''
    if filename[-4:] != '.csv':
        raise ValueError("The provided file name must end in '.csv'.")

    # Define string constants
    TOTAL = "Total Points"
    COUNT = "# of Students"
    RATINGS = "Category Rating"
    RAT_SUM = "Rating Sum"
    RAT_A = "Rating A"
    RAT_B = "Rating B"
    FINAL_RATING = "Final Individual Rating"

    # Define the columns used for scoring
    START_COL = 3
    END_COL = 8

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


if __name__ == '__main__':
    main()


# cat_frame.to_csv('Category Rating.csv', index=False)
