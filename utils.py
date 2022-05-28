"""
This script file contain GoogleSheet and ProcessCSV class.
GoogleSheet class responsibility:
    - authenticate with google sheet
    - reading google sheet data to pandas df
    - writing google sheet

we used two google sheet library:
    - gspread reading google sheet data
    - pygsheets for writing google sheet data

ProcessCSV class responsibility:
    - reading scrapy feed scraping csv file to pandas df
    - reading google worksheet data to pandas df
    - concat two df
    - filter duplicate
    - save a csv file
"""

import gspread
import pandas as pd
import pygsheets


CREDENTIALS = "prothomalo-credentials.json"
WORK_BOOK = "prothomalo_news_scraping_tools"


class GoogleSheet:
    """
    Google Sheet class responsibility:
            - authenticate with google sheet
            - reading worksheet as df
            - writing worksheet from csv file
    """


    def __init__(self, credentials, work_book) -> None:
        """
        it take credentials json file and google sheet work book to authenticate google sheet,
        this parameter will used both reading and writing google sheet module
        Parameters
        ----------
        credentials : json
            google sheet service account json file
        work_book : str
            authorize google workbook
        """

        self.credentials = credentials
        self.work_book = work_book



    def _authentication(self, action_type):
        """
        this method will authentication Google sheet and return workbook for future read and write
        Parameters
        ----------
        action_type : read|write
            if read it will use 'gspread'
            if write it will use 'pygsheets'

        Returns
        -------
        google sheet workbook
        """

        if action_type == "read":
            gspread_client = gspread.service_account(self.credentials)
            work_book = gspread_client.open(self.work_book)
            return work_book
        if action_type == "write":
            pygsheets_client = pygsheets.authorize(
                service_file=self.credentials)
            work_book = pygsheets_client.open(self.work_book)
            return work_book


    def reading_worksheet(self, work_sheet):
        """
        this method read a work sheet and return pandas df,
        it first authenticate with '_authentication' method then read worksheet
        Parameters
        ----------
        work_sheet : str
            authentication worksheet name from google sheet workbook
        Returns
        -------
        pandas df
        """

        # Workbook _authentication method
        work_book = self._authentication(action_type='read')
        worksheet = work_book.worksheet(work_sheet)
        df = pd.DataFrame(worksheet.get_all_records())
        return df


    def writing_worksheet(self, work_sheet, csv_file, drop_column=None):
        """
        this method write google worksheet with processed csv file,
        it remove header and columns name based on arguments
        and upload on google worksheet

        Parameters
        ----------
        work_sheet : str
            name of google worksheet which data frame update 
        csv_file : csv file
            name of process  CSV file for upload
        drop_columns: str
            columns name that drop before update google sheet
        """

        df = pd.read_csv(csv_file)   # Formate csv file

        # Cleaning CSV file; Drop columns, remove header as requirements
        if drop_column is not None:
            df = df.drop([drop_column, ], axis=1)
        df.columns = df.iloc[0]
        df = df[1:]

        work_book = self._authentication(action_type="write")
        worksheet = work_book.worksheet_by_title(work_sheet)
        worksheet.set_dataframe(df, (2, 1))




class ProcessCSV(GoogleSheet):
    """
    this class will do, this list of jobs:
            - reading csv to df
            - concat df and filter df
            - save processed csv file
    """
    
    def __init__(self, credentials, work_book, scraping_csv_file) -> None:
        super().__init__(credentials, work_book)
        self.scraping_csv_file = scraping_csv_file


    def _reading_scraping_csv(self):
        """
        this method read scraping csv file with df

        Returns
        -------
        _type_: df 
            scraping csv to pandas data frame
        """
        df = pd.read_csv(self.scraping_csv_file)
        return df



    def filter_duplicate(self, worksheet):
        """
        this method read existing scraping csv file and google sheet worksheet as pandas data frame,
        concat both df and filter duplicate.
        It return ready to upload csv file

        Returns
        --------
        csv file
        """

        scraping_data_df = self._reading_scraping_csv()
        google_worksheet_df = super().reading_worksheet(work_sheet=worksheet)
        processed_csv_df = pd.concat([scraping_data_df, google_worksheet_df]).drop_duplicates()
        processed_csv_df.to_csv("processed_file.csv", index=False)



if __name__ == '__main__':
    app = ProcessCSV(
        credentials="prothomalo-credentials.json",
        work_book=WORK_BOOK,
        scraping_csv_file="subheadline.csv",
        )
    app.filter_duplicate(worksheet="today-sub-headlines")
    



#     """
#     app = GoogleSheet(credentials=CREDENTIALS, work_book=WORK_BOOK)
#     # reading google sheet
#     df_headline = app.reading_worksheet(work_sheet="today-headlines")
#     df_sub_headline = app.reading_worksheet(work_sheet="today-sub-headlines")
#     df_headline.to_csv("df_headline.csv", index=False)
#     df_sub_headline.to_csv("df_sub_headline.csv", index=False)
# 
#     # writing work sheet
#     app.writing_worksheet(work_sheet="today-headlines", csv_file="subheadline.csv", drop_column="publish_date")
#     """


# class ProcessCSV(GoogleSheet):
#     """
#     this class will do, this list of jobs:
#             - reading csv to df
#             - concat df
#             - filter df
#             - save processed csv file
#     """

#     def __init__(self, credentials, work_book, csv_file) -> None:
#         super().__init__(credentials, work_book)
#         self.csv_file = csv_file


#     def _reading_scraping_csv(self):
#         """ this method read scraping csv file and convert into df """
#         df = pd.read_csv(self.csv_file)
#         return df


#     def filter_duplicate(self,):
#         scraping_data_df = self._reading_scraping_csv()
#         google_worksheet_df = super().reading_worksheet()


#         # Google sheet data
#         google_sheet = GoogleSheet(credentials=self.credentials, work_book=self.work_book)
#         df = google_sheet.reading_worksheet()


## Garbage ##
# df.to_csv("processed_archive.csv", index=False)
# app = GoogleSheet(credentials=CREDENTIALS, work_book=WORK_BOOK)
# df = app.reading_worksheet(work_sheet="today-headlines")
# app.writing_worksheet(work_sheet="today-headlines", csv_file="headline.csv")


# """
# this method will read a worksheet and return pandas df
# for reading google sheet to df, we used 'gspread' for its df feature
# """
# 
# 
# """ 
# writing google worksheet need to some prebuilt data cleaning process
# this method has two parameter
#         - work sheet, which google sheet want you update with processed df
#         - csv file, which csv file you want import
# """

#  """ this method read scraping csv file and convert into df """