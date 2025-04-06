import os
import json
import pandas as pd
from app.barrier import SimpleBarrier

class DataIngestor:
    def __init__(self, csv_path: str, barrier: SimpleBarrier):
        # TODO: Read csv from csv_path
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
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
        self.barrier.wait()
    
    def states_mean(self, question):
        # Filter data frame by question column
        df = self.data[
            (self.data["Question"] == question) & 
            (self.data["YearStart"] >= 2011 & self.data["YearEnd"] <= 2022)]
        # Group by state and calculate the average of each state
        result = df.groupby("LocationAbbr")["Data_Value"].mean().sort_values()
        return result.to_dict()
    
    def state_mean(self, question, job_state):
        # Filter data frame by question column
        df = self.data[
            (self.data["Question"] == question) & 
            (self.data["YearStart"] >= 2011 & self.data["YearEnd"] <= 2022)]
        # Group by state and calculate the average of each state
        result = df.groupby(job_state)["Data_Value"].mean()
        return result.to_dict()
    
    def best5(self, question):
        # Filter data frame by question column
        df = self.data[
            (self.data["Question"] == question) & 
            (self.data["YearStart"] >= 2011 & self.data["YearEnd"] <= 2022)]
        # Group by state and calculate the average of each state
        df2 = df.groupby("LocationAbbr")["Data_Value"].mean().sort_values()
        if question in self.questions_best_is_min:
            result = df2.head(5)
        else:
            result = df2.tail(5).sort_values(by=["Data_Value"], ascending = False)
        return result.to_dict()
    
    def worst5(self, question):
        # Filter data frame by question column
        df = self.data[
            (self.data["Question"] == question) & 
            (self.data["YearStart"] >= 2011 & self.data["YearEnd"] <= 2022)]
        # Group by state and calculate the average of each state
        df2 = df.groupby("LocationAbbr")["Data_Value"].mean().sort_values()
        if question in self.questions_best_is_min:
            result = df2.tail(5).sort_values(by=["Data_Value"], ascending = False)
        else:
            result = df2.head(5)
        return result.to_dict()

    def global_mean(self, question):
        return self.data[
            (self.data["Question"] == question) & 
            (self.data["YearStart"] >= 2011 & self.data["YearEnd"] <= 2022)
            ]["Data_Value"].mean()
    
    def diff_from_mean(self, question):
        global_avg = self.global_mean(question)
        states_avg = self.states_mean(question)
        return {state: (global_avg - avg) for state, avg in states_avg.items()}
    
    def state_diff_from_mean(self, question, job_state):
        global_avg = self.global_mean(question)
        state_avg = self.state_mean(question, job_state)[job_state]
        return {job_state: (global_avg - state_avg)}

    def mean_by_category(self, question):
        pass
    def state_mean_by_category(self, question, job_state):
        pass
