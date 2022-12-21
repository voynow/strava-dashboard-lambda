
from utils import data, dashboard

def lambda_handler(event, context):

    df = data.preprocessing()
    dashboard.update_dashboard(df)

    return 1
