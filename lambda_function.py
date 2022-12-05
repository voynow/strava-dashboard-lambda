
import strava_utils

def lambda_handler(event, context):

    df = strava_utils.data_preprocessing()
    fig = strava_utils.create_fig(df)
    strava_utils.update_dashboard(fig)

    return 1