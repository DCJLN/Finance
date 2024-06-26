import pandas as pd

# classes
from technical_indicator import TechnicalIndicator


class InvestBot:
    def __init__(self, fin_data: pd.DataFrame):
        self.fin_data = fin_data
        print(35 * "_")
        print("**New invest bot has been created**")
        print(35 * "_")
        print("")

    def bb_out_up_strategy(self, parameters: dict):
        """
        Investment strategy that will identify the first positive closing prices after crossing down the lower Bollinger
        band.
        @return: None
        """

        print("BB out-up strategy launched...")

        # Computing the 20-days SMA
        sma_values = TechnicalIndicator.sma(prices=self.fin_data['Adj Close'], days=parameters['rolling_days'])
        self.fin_data = self.fin_data.join(sma_values.rename('sma'))

        # Computing the Bollinger bands
        upper_bb, lower_bb = TechnicalIndicator.bollinger_bands(prices=self.fin_data['Adj Close'],
                                                                days=parameters['rolling_days'],
                                                                std_factor=parameters['std_factor'],
                                                                sma=self.fin_data['sma'])
        self.fin_data = self.fin_data.join(upper_bb).join(lower_bb)

        signals = []
        i = 0
        while i < len(self.fin_data):
            if i == 0:
                signals.append(False)
                i += 1
            elif self.fin_data.iloc[i]['Adj Close'] < self.fin_data.iloc[i]['lower_bb'] \
                    and self.fin_data.iloc[i - 1]['Adj Close'] > self.fin_data.iloc[i - 1]['lower_bb']:
                for j in range(i, len(self.fin_data)):
                    if self.fin_data.iloc[j]['Adj Close'] > self.fin_data.iloc[j - 1]['Adj Close']:
                        signals.append(True)
                        i = j + 1
                        break
                    else:
                        signals.append(False)
            else:
                signals.append(False)
                i += 1
        self.fin_data['signal'] = signals
        print(f"=> {sum(self.fin_data['signal'])} signal(s) found during the period.")

        return self.fin_data

    def back_testing(self):
        """

        @return:
        """
        if 'signal' not in self.fin_data.columns or self.fin_data['signals'].empty:
            print("Please compute investing signals before backtesting it.")
            raise ValueError



