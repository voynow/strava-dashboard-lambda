
import base64
import boto3
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from io import BytesIO


dashbaord_bucket = "strava-dashboard"
html_filename = 'index.html'
s3 = boto3.client('s3')
figsize = (14, 6)


def create_fig(df, heatmap):

    fig = plt.figure(constrained_layout=True, figsize=figsize)
    axs = fig.subplot_mosaic(
        [['Left', 'TopRight'],['Left', 'BottomRight']],
        gridspec_kw={'width_ratios':[3, 7]}
    )
    fig.tight_layout(pad=3.0)

    axs['Left'].set_title("Philly Running Heatmap")
    axs['Left'].imshow(heatmap, cmap="Spectral_r")
    axs['Left'].tick_params(left=False, bottom=False)
    axs['Left'].axis('off')

    axs['TopRight'].set_title('Monthly Mileage')
    axs['TopRight'].set_ylabel('Mileage')
    axs['TopRight'].plot(
        df.index, 
        df['distance_monthly_ma'], 
        c='#FBC15E',
        linewidth=3
    )

    axs['BottomRight'].set_title('Weekly Mileage')
    axs['BottomRight'].set_ylabel('Mileage')
    axs['BottomRight'].plot(
        df.index, 
        df['distance_week_ma'], 
        c='#348ABD', 
        linewidth=3
    )

    return fig


def update_dashboard(df, heatmap):
    """
    Generate html from matplotlib plot
    """

    tmpfile = BytesIO()
    fig = create_fig(df, heatmap)

    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = f'<center><img src=\'data:image/png;base64,{encoded}\'></ceneter>'

    s3.put_object(
        Bucket=dashbaord_bucket,
        Key=html_filename,
        Body=html,
        ContentType="text/html",
    )
