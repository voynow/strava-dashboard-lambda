
import strava_utils

def lambda_handler(event, context):

    df = strava_utils.data_preprocessing()
    fig = strava_utils.create_fig(df)
    resp = strava_utils.update_dashboard(fig)

    return resp

print(lambda_handler({}, {}))