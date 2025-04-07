import pandas as pd
from app.barrier import SimpleBarrier

class DataIngestor:
    ''' Class for computing csv data and solving the requests '''
    def __init__(self, csv_path: str, barrier: SimpleBarrier):
        ''' Initialize DataIngestor instance'''
        self.csv_path = csv_path
        self.data = pd.read_csv(csv_path)
        self.barrier = barrier

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
            'activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
            'physical activity and engage in muscle-strengthening activities on 2 or '
            'more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity '
            'aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic '
            'activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities '
            'on 2 or more days a week',
        ]
        self.barrier.wait()

    def states_mean(self, question):
        ''' Returns a dictionary for states_mean request '''
        df = self.data[
            (self.data["Question"] == question) &
            (self.data["YearStart"] >= 2011) & (self.data["YearEnd"] <= 2022)
            ].groupby("LocationDesc")["Data_Value"].mean().sort_values()
        return df.to_dict()

    def state_mean(self, question, job_state):
        ''' Returns a dictionary for state_mean request '''
        df = self.data[
            (self.data["Question"] == question) &
            (self.data["LocationDesc"] == job_state) &
            (self.data["YearStart"] >= 2011) & (self.data["YearEnd"] <= 2022)]
        return {job_state: df["Data_Value"].mean()}

    def best5(self, question):
        ''' Returns a dictionary for best5 request '''
        df = self.data[
            (self.data["Question"] == question) &
            (self.data["YearStart"] >= 2011) & (self.data["YearEnd"] <= 2022)
            ].groupby("LocationDesc")["Data_Value"].mean().sort_values()

        if question in self.questions_best_is_min:
            result = df.head(5)
        else:
            result = df.tail(5).sort_values(ascending = False)
        return result.to_dict()

    def worst5(self, question):
        ''' Returns a dictionary for worst5 request '''
        df = self.data[
            (self.data["Question"] == question) &
            (self.data["YearStart"] >= 2011) & (self.data["YearEnd"] <= 2022)
            ].groupby("LocationDesc")["Data_Value"].mean().sort_values()

        if question in self.questions_best_is_min:
            result = df.tail(5).sort_values(ascending = False)
        else:
            result = df.head(5)
        return result.to_dict()

    def global_mean(self, question):
        ''' Returns a dictionary for global_mean request '''
        return {"global_mean": self.data[
            (self.data["Question"] == question) &
            (self.data["YearStart"] >= 2011) & (self.data["YearEnd"] <= 2022)
            ]["Data_Value"].mean()}

    def diff_from_mean(self, question):
        ''' Returns a dictionary for diff_from_mean request '''
        global_avg = self.global_mean(question)["global_mean"]
        states_avg = self.states_mean(question)
        return {state: (global_avg - avg) for state, avg in states_avg.items()}

    def state_diff_from_mean(self, question, job_state):
        ''' Returns a dictionary for states_diff_from_mean request '''
        global_avg = self.global_mean(question)["global_mean"]
        state_avg = self.state_mean(question, job_state)[job_state]
        return {job_state: (global_avg - state_avg)}

    def mean_by_category(self, question):
        df = self.data[
            (self.data["Question"] == question)
            ].groupby(["LocationDesc",
                       "StratificationCategory1",
                       "Stratification1"])["Data_Value"].mean()
        return {"(" + ", ".join(map(lambda x: "'" + str(x) + "'", key)) + ")"
                : value for key, value in df.to_dict().items()}

    def state_mean_by_category(self, question, job_state):
        df = self.data[
            (self.data["Question"] == question) &
            (self.data["LocationDesc"] == job_state)
            ].groupby(["StratificationCategory1", "Stratification1"])["Data_Value"].mean()
        return {job_state : {"(" + ", ".join(map(lambda x: "'" + str(x) + "'", key)) + ")"
                             : value for key, value in df.to_dict().items()}}
