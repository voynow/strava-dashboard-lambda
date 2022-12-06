
import base64
import boto3
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from io import BytesIO


raw_bucket = "strava-raw"
dashbaord_bucket = "strava-dashboard"
html_filename = 'index.html'
s3_recource = boto3.resource('s3')
s3_client = boto3.client('s3')


def get_activities():
    """
    Get activities JSON from raw bucket
    """
    activities = []
    for obj in s3_recource.Bucket(raw_bucket).objects.all():
        body_bytes = obj.get()['Body'].read()
        activities.append(json.loads(body_bytes))
    return activities


def clean(df):
    
    # update date col as pandas datetime
    df['date'] = pd.to_datetime(df['start_date'].apply(lambda x: x.split("T")[0]))
    df.drop(['start_date'], axis=1, inplace=True)
    
    # meters -> miles
    df['distance'] *= 0.000621371
    
    return df
    

def activities_to_df(activities):
    """
    Create pandas dataframe from list of activities
    """
    keys = []
    [[keys.append(item) for item in activity] for activity in activities]
    unique_keys = set(keys)

    keys_by_activity = [[key for key in activity] for activity in activities]
    for keys in keys_by_activity:
        remove_keys = []
        for key in unique_keys:
            if key not in keys:
                remove_keys.append(key)
        for key in remove_keys:
            unique_keys.remove(key)
    
    activities = [{key: activity[key] for key in unique_keys} for activity in activities]
    return clean(pd.DataFrame(activities))


def fill_missing_dates(df):
    """
    Add rows for dates where no activity exists
    """
    if 'date' not in df.columns:
        raise ValueError("Missing required column: 'date'")
    
    date_range = pd.date_range(df['date'].min(), df['date'].max())
    dates_df = pd.DataFrame(date_range, columns=['date'])
    joined_df = dates_df.set_index('date').join(df.set_index('date'))
    
    return joined_df


def data_preprocessing():
    """
    Facilitates S3 operations, preprocessing, and transformation for analytics
    """
    activities = get_activities()
    df = activities_to_df(activities)

    run_df = df[df['type'] == 'Run']
    run_df = fill_missing_dates(run_df)

    run_df['distance'] = run_df['distance'].apply(lambda x: 0 if np.isnan(x) else x)
    run_df['distance_ma'] = run_df['distance'].rolling(30).sum()

    return run_df


def create_fig(df):
    """
    create plot for monthly mileage
    """
    fig = plt.figure(figsize=(10, 6))
    plt.plot(
        df.index, 
        df['distance_ma'], 
        c='#5589C1', 
        linewidth=3
    )

    plt.title('Monthly Mileage')
    plt.xlabel('Date')
    plt.ylabel('Mileage')

    return fig


def update_dashboard(fig):
    """
    Generate html from matplotlib plot
    """
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = f'<img src=\'data:image/png;base64,{encoded}\'>'

    return s3_client.put_object(
        Bucket=dashbaord_bucket,
        Key=html_filename,
        Body=html,
        ContentType="text/html",
    )
