
from utils import data, dashboard

def lambda_handler(event, context):

    df = data.preprocessing()
    heatmap = data.get_philly_heatmap()

    dashboard.update_dashboard(df, heatmap)

    return 1
