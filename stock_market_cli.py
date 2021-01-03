""" Example or something

    Is this not informative enough?

    Load a specific stock
    Then apply a specific TA on it

    Do this because AlphaVantage only allows 5 API calls per minutes.
    This way we only need 1 call, and can apply TA to the result without
    using an API request.

    Finviz for data
    Multiple TA with kind stock

    Do my own personal Fundamental Analysis Dataframe
    Do option to explain important key metrics

    Do own personal Technical Analysis with multiple indicators perhaps?

    Split Menu into fa, ta and pred. Fundamental Analysis, Technical Analysis and Prediction, respectively.

"""

import argparse
import pandas as pd
from stock_market_helper_funcs import *
import stock_market_menu as smm
from fundamental_analysis import menu as fam
from technical_analysis import menu as tam

# delete this important when automatic loading tesla
#i.e. when program is done
import config_bot as cfg
from alpha_vantage.timeseries import TimeSeries

# -----------------------------------------------------------------------------------------------------------------------
def print_help(s_ticker, s_start, s_interval, b_is_market_open):
    """ Print help
    """
    print("What do you want to do?")
    print("   gainers     show latest top gainers")
    print("   sectors     show sectors performance")
    print("   view        view and load a specific stock ticker for technical analysis")
    print("   clear       clear a specific stock ticker from analysis")
    print("   load        load a specific stock ticker for analysis")
    print("   help        help to see this menu again")
    print("   quit        to abandon the program")

    s_intraday = (f'Intraday {s_interval}', 'Daily')[s_interval == "1440min"]
    if s_ticker and s_start:
        print(f"\n{s_intraday} Stock: {s_ticker} (from {s_start.strftime('%Y-%m-%d')})")
    elif s_ticker:
        print(f"\n{s_intraday} Stock: {s_ticker}")
    else:
        print("\nStock: ?")
    print(f"Market {('CLOSED', 'OPEN')[b_is_market_open]}.")

    if s_ticker:
        print("\nMenus:")
        print("   fa          fundamental analysis")
        print("   ta          technical analysis")
        print("   pred        prediction techniques")

    '''
        print("\nPrediction:")
        print("   ma")
        print("   ema")
        print("   lr")
        print("   knn")
        print("   arima")
        print("   rnn")
        print("   lstm")
        print("   prophet")
    '''


# -----------------------------------------------------------------------------------------------------------------------
def main():
    """ Main function of the program
    """ 

    s_ticker = ""
    s_start = ""
    df_stock = pd.DataFrame()
    b_intraday = False
    s_interval = "1440min"

    # Set stock by default to speed up testing
    s_ticker = "NIO"
    s_start = datetime.strptime("2020-06-04", "%Y-%m-%d")
    ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format='pandas')
    df_stock, d_stock_metadata = ts.get_daily_adjusted(symbol=s_ticker, outputsize='full')  
    df_stock = df_stock[s_start:] 
    # Delete above in the future

    
    # Add list of arguments that the main parser accepts
    menu_parser = argparse.ArgumentParser(prog='stock_market_bot', add_help=False)
    menu_parser.add_argument('cmd', choices=['gainers', 'sectors', 'view', 'clear', 'load', 
                                             'fa', 'ta', 'help', 'quit'])

    # Add list of arguments that the fundamental analysis parser accepts
    fa_parser = argparse.ArgumentParser(prog='fundamental_analysis', add_help=False)
    fa_parser.add_argument('fa', choices=['info', 'help', 'q', 'quit',
                                          'overview', 'key', 'profile', 'rating', 'quote', 'enterprise', 'dcf', # details
                                          'income', 'balance', 'cash', 'earnings', # financial statement
                                          'metrics', 'ratios', 'growth']) # ratios
                                             
    # Add list of arguments that the technical analysis parser accepts
    ta_parser = argparse.ArgumentParser(prog='technical_analysis', add_help=False)
    ta_parser.add_argument('ta', choices=['help', 'q', 'quit',
                                          'ema', 'sma', 'vwap', # overlap
                                          'cci', 'macd', 'rsi', 'stoch', # momentum
                                          'adx', 'aroon', # trend
                                          'bbands', # volatility
                                          'ad', 'obv']) # volume


    # Print first welcome message and help
    print("\nWelcome to Didier's Stock Market Bot\n")
    print_help(s_ticker, s_start, s_interval, b_is_stock_market_open())
    print("\n")

    # Loop forever and ever
    while True:
        # Get input command from user
        as_input = input('> ')
        
        # Parse main command of the list of possible commands
        try:
            (ns_known_args, l_args) = menu_parser.parse_known_args(as_input.split())

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue

        # --------------------------------------------------- GAINERS --------------------------------------------------
        if ns_known_args.cmd == 'gainers':
            smm.gainers(l_args)

        # --------------------------------------------------- SECTORS --------------------------------------------------
        if ns_known_args.cmd == 'sectors':
            smm.sectors(l_args)

        # --------------------------------------------------- CLEAR ----------------------------------------------------
        elif ns_known_args.cmd == 'clear':
            print("Clearing stock ticker to be used for analysis")
            s_ticker = ""
            s_start = ""

        # ---------------------------------------------------- LOAD ----------------------------------------------------
        elif ns_known_args.cmd == 'load':
            [s_ticker, s_start, s_interval, df_stock] = smm.load(l_args, s_ticker, s_start, s_interval, df_stock)

        # ---------------------------------------------------- VIEW ----------------------------------------------------
        elif ns_known_args.cmd == 'view':
            smm.view(l_args, s_ticker, s_start, s_interval, df_stock)

        # ---------------------------------------------------- HELP ----------------------------------------------------
        elif ns_known_args.cmd == 'help':
            print_help(s_ticker, s_start, s_interval, b_is_stock_market_open())

        # ----------------------------------------------------- QUIT ----------------------------------------------------
        elif ns_known_args.cmd == 'quit':
            print("Hope you made money today. Good bye my lover, good bye my friend.\n")
            return
        
        # ------------------------------------------- FUNDAMENTAL ANALYSIS ---------------------------------------------
        elif ns_known_args.cmd == 'fa':
            b_quit = fam.fa_menu(fa_parser, s_ticker, s_start, s_interval)

            if b_quit:
                print("Hope you made money today. Good bye my lover, good bye my friend.\n")
                return
            else:
                print_help(s_ticker, s_start, s_interval, b_is_stock_market_open())

        # -------------------------------------------- TECHNICAL ANALYSIS ----------------------------------------------
        elif ns_known_args.cmd == 'ta':
            b_quit = tam.ta_menu(ta_parser, df_stock, s_ticker, s_start, s_interval)

            if b_quit:
                print("Hope you made money today. Good bye my lover, good bye my friend.\n")
                return
            else:
                print_help(s_ticker, s_start, s_interval, b_is_stock_market_open())

        # ------------------------------------------------ PREDICTION --------------------------------------------------


        # --------------------------------------------------------------------------------------------------------------
        else:
            print('Shouldnt see this command!')

        print("")

if __name__ == "__main__":
    main()
