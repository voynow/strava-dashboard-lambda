
import base64
import boto3
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from io import BytesIO


dashbaord_bucket = "strava-dashboard"
html_filename = 'index.html'
s3 = boto3.client('s3')


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


def update_dashboard(df):
    """
    Generate html from matplotlib plot
    """
    fig = create_fig(df)
    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = f'<img src=\'data:image/png;base64,{encoded}\'>'

    return s3.put_object(
        Bucket=dashbaord_bucket,
        Key=html_filename,
        Body=html,
        ContentType="text/html",
    )
