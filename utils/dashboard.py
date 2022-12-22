
import base64
import boto3
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from io import BytesIO


dashbaord_bucket = "strava-dashboard"
html_filename = 'index.html'
s3 = boto3.client('s3')
figsize = (12, 2.5)


def create_fig(df, col, color, title):
    """ Create mileage figure
    """
    fig = plt.figure(figsize=figsize)
    plt.plot(
        df.index, 
        df[col], 
        c=color, 
        linewidth=3
    )

    plt.title(title)
    plt.ylabel('Mileage')

    return fig


def update_dashboard(df):
    """
    Generate html from matplotlib plot
    """
    figures = [
        create_fig(df, 'distance_monthly_ma', '#FBC15E', 'Monthly Mileage'),
        create_fig(df, 'distance_week_ma', '#348ABD', 'Weekly Mileage'),
    ]
    tmpfiles = [BytesIO() for _ in range(len(figures))]

    html = ""
    for fig, tmpfile in zip(figures, tmpfiles):
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html += f'<center><img src=\'data:image/png;base64,{encoded}\'></ceneter>'

    s3.put_object(
        Bucket=dashbaord_bucket,
        Key=html_filename,
        Body=html,
        ContentType="text/html",
    )
