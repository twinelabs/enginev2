"""
div_job
--------

Runs matching process.
"""

from analytics.goodness import cluster_evaluation
import numpy as np
import pandas as pd

def run_div_job():
    file_names = ['data/cluster1.csv', 'data/cluster2.csv', 'data/cluster3.csv', 'data/cluster4.csv']
    
    k = 6
    
    all_clusters = [pd.DataFrame.from_csv(f) for f in file_names]
    
    # Country is not formatted well enough to run diversity...
    # Industries have multiple. It will be difficult to run normal diversity.
    # 
    columns_names = [('Please indicate your gender:','Gender'), 
                    ('4. How introspective (reflective) are you on a scale of 1-10 (1=not at all, 10=very)?', 'Introspection'),
                    ('What motivates you? (Please rank order choices) (Influence / Power)', 'Influence / Power'),
                    ('What motivates you? (Please rank order choices) (Achievement)', 'Achievement'),
                    ('What motivates you? (Please rank order choices) (Personal Relationships)', 'Personal Relationships'),
                    ('What motivates you? (Please rank order choices) (Wealth)', 'Wealth'),
                    ('What motivates you? (Please rank order choices) (Intellectual Stimulation)', 'Intellectual Stimulation')
                    ]
    
    dfs = []
    for column_name in columns_names:
        metrics = []
        for cluster in all_clusters:
            values = cluster[column_name[0]]
            cluster_types = [values[i:i+k] for i in range(0,len(values),6)]
            metrics.append(cluster_evaluation.evaluate_clusters(cluster_types))
            # Should try with zscores somehow?
                 
        file_columns = [file_names[i] + '_' + column_name[1] for i in range(len(file_names))]  
        column_output = pd.DataFrame(metrics, index=file_columns) 
        dfs.append(column_output)
        
    final_df = pd.concat(dfs)
    final_df.to_csv('div_job.csv')  
    return final_df
    
if __name__ == '__main__':
    run_div_job()
    
