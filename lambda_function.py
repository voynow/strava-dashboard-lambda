
from utils import data, dashboard

def lambda_handler(event, context):

    df = data.preprocessing()
    resp = dashboard.update_dashboard(df)

    return resp

lambda_handler({}, {})