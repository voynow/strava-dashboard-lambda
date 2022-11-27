
import boto3
import json
import pandas as pd

bucket_name = "strava-raw"
s3 = boto3.resource('s3')

def get_activities():
    """
    Get activities JSON from raw bucket
    """
    activities = []
    for obj in s3.Bucket(bucket_name).objects.all():
        body_bytes = obj.get()['Body'].read()
        activities.append(json.loads(body_bytes))
    return activities
    

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

    return pd.DataFrame([{key: activity[key] for key in unique_keys} for activity in activities])