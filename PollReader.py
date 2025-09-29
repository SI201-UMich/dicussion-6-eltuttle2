import os
import unittest


class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        """
        Reads all of the raw data from the CSV and builds a dictionary where
        each key is the name of a column in the CSV, and each value is a list
        containing the data for each row under that column heading.

        There may be a couple bugs in this that you will need to fix.
        Remember that the first row of a CSV contains all of the column names,
        and each value in a CSV is seperated by a comma.
        """

        # iterate through each row of the data
        for i in self.raw_data:
            if i.startswith('month'):
                continue
            # split up the row by column
            row = i.strip().split(',')

            # map each part of the row to the correct column
            self.data_dict['month'].append(row[0])
            self.data_dict['date'].append(int(row[1]))
            sample_parts = row[2].split()
            self.data_dict['sample'].append(int(sample_parts[0]))
            self.data_dict['sample type'].append(sample_parts[1])
            self.data_dict['Harris result'].append(float(row[3]))
            self.data_dict['Trump result'].append(float(row[4]))


    def highest_polling_candidate(self):
        """
        This method should iterate through the result columns and return
        the name of the candidate with the highest single polling percentage
        alongside the highest single polling percentage.
        If equal, return the highest single polling percentage and "EVEN".

        Returns:
            str: A string indicating the candidate with the highest polling percentage or EVEN,
             and the highest polling percentage.
        """
        max_trump = max(self.data_dict["Trump result"])
        max_harris = max(self.data_dict["Harris result"])
        if max_trump > max_harris:
            return f"Trump {max_trump*100:.1f}%"
        elif max_trump < max_harris:
            return f"Harris {max_harris*100:.1f}%"
        else:
            return f"EVEN {max_harris*100:.1f}%"


    def likely_voter_polling_average(self):
        """
        Calculate the average polling percentage for each candidate among likely voters.

        Returns:
            tuple: A tuple containing the average polling percentages for Harris and Trump
                   among likely voters, in that order.
        """
        harris_sum = 0
        trump_sum = 0
        count = 0
        for i, stype in enumerate(self.data_dict['sample type']):
            if stype == 'LV':
                harris_sum += self.data_dict['Harris result'][i]
                trump_sum += self.data_dict['Trump result'][i]
                count += 1
        return (harris_sum / count, trump_sum / count)


    def polling_history_change(self):
        """
        Calculate the change in polling averages between the earliest and latest polls.

        This method calculates the average result for each candidate in the earliest 30 polls
        and the latest 30 polls, then returns the net change.

        Returns:
            tuple: A tuple containing the net change for Harris and Trump, in that order.
                   Positive values indicate an increase, negative values indicate a decrease.
        """
        n = 30
        harris_earliest = sum(self.data_dict['Harris result'][:n]) / n
        trump_earliest = sum(self.data_dict['Trump result'][:n]) / n
        harris_latest = sum(self.data_dict['Harris result'][-n:]) / n
        trump_latest = sum(self.data_dict['Trump result'][-n:]) / n
        return (harris_latest - harris_earliest, trump_latest - trump_earliest)


class TestPollReader(unittest.TestCase):
    """
    Test cases for the PollReader class.
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self
