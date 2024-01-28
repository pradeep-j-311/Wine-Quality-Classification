import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

class wine: 
    def __init__(self, dataframe): 
        self.df = dataframe

    def compute_threshold(self, series, no_of_deviations): 
        std_ = series.std() 
        threshold_max = series.mean() + no_of_deviations*std_ 
        threshold_min = series.mean() - no_of_deviations*std_ 

        return threshold_max, threshold_min 

    def remove_outliers(self, col, threshold_max, threshold_min): 
        self.df = self.df.reset_index(drop=True)
        outliers = self.df[(self.df[col] > threshold_max) | (self.df[col] < threshold_min)]
        new_frame = self.df.drop(outliers.index)
            
        return new_frame.reset_index(drop=True), outliers.reset_index(drop=True)

    def count_outliers(self, col, threshold_max, threshold_min): 
        self.df = self.df.reset_index(drop=True)
        outliers = self.df[(self.df[col]>threshold_max) | (self.df[col] < threshold_min)]
        no_outliers = len(outliers)

        return no_outliers

    def count_outliers_frame(self, no_deviations): 
        outlier_count = 0
        cleaned_frame = self.df.copy()
        for col in self.df: 
            threshold_max, threshold_min = self.compute_threshold(self.df[col], no_deviations)
            outlier_count += self.count_outliers(col, threshold_max, threshold_min)
            cleaned_frame, _ = self.remove_outliers(col, threshold_max, threshold_min)


        return outlier_count 

    def remove_outliers_frame(self, no_deviations): 
        outlier_entries = []
        cleaned_frame = self.df.copy()
        for col in self.df: 
            if self.df[col].dtype.name == 'float64': # only process floating number columns 
                threshold_max, threshold_min = self.compute_threshold(self.df[col], no_deviations)
                cleaned_frame, outliers = self.remove_outliers(col, threshold_max, threshold_min)
                outlier_entries.append(outliers)
        outlier_frame = pd.concat(outlier_entries)
        return cleaned_frame, outlier_frame