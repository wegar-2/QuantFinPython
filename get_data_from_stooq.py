import pandas as pd
import datetime


################################################################################
##### this script contains method that is preparing a data frame using data ####
###### available at Stooq.com                                               ####
################################################################################


def validate_date_format_yyy_mm_dd(date_text):
    """
    Function validate_date_format_yyy_mm_dd checks whether the format of the
    string passed to it is YYYY-MM-DD. If it is not, an error is raised
    :param date_text: date to be validated, object of class string
    :return: does not return anything
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def get_daily_data_from_stooq(ticker_symbol, start_date, end_date):
    """
    get_daily_data_from_stooq - method returns a pd.DataFrame of closing prices
    made using daily data available at stooq.com.
    :param ticker_symbol: ticker symbol under which an asset is available 
            at Stooq.com
    :param start_date: the starting date for the time series 
    :param end_date: the ending data for the time series
    :return: pd.DataFrame object with the closing prices. Dates 
    are in column "Date", prices are in column "Close"
    """
    # check whether the start_date and end_date are strings
    if isinstance(start_date, str) and isinstance(end_date, str):
        pass
    else:
        raise ValueError("Dates passed to the function are not strings!!!")
    # validate formats of dates passed to the function
    validate_date_format_yyy_mm_dd(start_date)
    print("Validation of start_date format result: positive...")
    validate_date_format_yyy_mm_dd(end_date)
    print("Validation of end_date format result: positive...")
    d_1 = start_date.replace("-", "")
    d_2 = end_date.replace("-", "")
    temp_url = "https://stooq.com/q/d/l/?s=" + ticker_symbol + "&d1=" \
               + d_1 + "&d2=" + d_2 + "&i=d"
    print("Getting data from URL: ", temp_url)
    # try-except block to catch the cases when the ticker symbol is nonexistent
    try:
        data_in = pd.read_csv(temp_url, usecols=['Date', 'Close'],
                              parse_dates=[0])
    except ValueError:
        print("ValueError occurred! Probably a nonexistent ticker has been"
              " passed to the function")
    except Exception:
        print("General error has occurred! Please check function arguments...")
    else:
        # if data is obtained, rename "Close" ===> ticker name
        data_in.rename(columns={"Close": ticker_symbol}, inplace=True)
    return data_in


# class inheriting from the general Exception - to be used in the next function
class NotAListPassed(Exception):
    pass


def get_daily_data_from_stooq_for_tickers(ticker_symbols_list,
                                          start_date, end_date):
    # check whether the first argument passed to the function is actually list
    if isinstance(ticker_symbols_list, list):
        pass
    else:
        # raise error and stop function execution if not a list
        raise NotAListPassed("The first argument passed to the function is "
                             "not a list - ERROR!")
    # walk through list of symbols
    for k in range(len(ticker_symbols_list)):
        ticker_symbol = ticker_symbols_list[k]
        print("Ticker symbol in this iteration: ", ticker_symbol)
        if k==0:
            df_joint_data = get_daily_data_from_stooq(ticker_symbol,
                                                      start_date, end_date)
            df_joint_data.rename(columns={"Close": ticker_symbol})
        else:
            # get data
            df_temp_data = get_daily_data_from_stooq(ticker_symbol,
                                                      start_date, end_date)
            df_temp_data.rename(columns={"Close": ticker_symbol}, inplace=True)
            # attach to the pre-existing data frame
            df_joint_data = df_joint_data.merge(right=df_temp_data,
                                                left_on="Date",
                                                right_on="Date",
                                                how="outer", sort=True)
    # further data processing: clearing, NAs servicing, etc.
    print("Top 3 rows before adjustments...")
    print(df_joint_data.head(3))

    df_joint_data.set_index("Date", inplace=True)
    df_joint_data.fillna(method="ffill", inplace=True)
    df_joint_data.fillna(method="bfill", inplace=True)

    print("Top 3 rows after adjustments...")
    print(df_joint_data.head(3))

    return df_joint_data