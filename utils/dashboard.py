
import base64
import boto3
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from io import BytesIO


dashbaord_bucket = "strava-dashboard"
html_filename = 'index.html'
s3 = boto3.client('s3')


def create_monthly_fig(df):
    """
    create plot for monthly mileage
    """
    fig = plt.figure(figsize=(11, 4))
    plt.plot(
        df.index, 
        df['distance_monthly_ma'], 
        c='#5589C1', 
        linewidth=3
    )

    plt.title('Monthly Mileage')
    plt.xlabel('Date')
    plt.ylabel('Mileage')

    return fig


def create_week_fig(df):
    """
    create plot for monthly mileage
    """
    fig = plt.figure(figsize=(11, 3.5))
    plt.plot(
        df.index, 
        df['distance_week_ma'], 
        c='#2bb58e', 
        linewidth=3
    )

    plt.title('Weekly Mileage')
    plt.xlabel('Date')
    plt.ylabel('Mileage')

    return fig


def update_dashboard(df):
    """
    Generate html from matplotlib plot
    """
    figures = [create_monthly_fig(df), create_week_fig(df)]
    tmpfiles = [BytesIO() for _ in range(len(figures))]

    html = ""
    for fig, tmpfile in zip(figures, tmpfiles):
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html += f'<center><img src=\'data:image/png;base64,{encoded}\'></ceneter>'

    return s3.put_object(
        Bucket=dashbaord_bucket,
        Key=html_filename,
        Body=html,
        ContentType="text/html",
    )
