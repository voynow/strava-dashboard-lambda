
def get_code(encoded):

    return f"""
    <!DOCTYPE html>
    <html>
        
        <head>
            <title>Strava Analytics Dashboard</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #CCE2EF;
                    font-family: Helvetica;
                }}
                img {{
                    border-radius: 10px;
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 10px 20px rgba(0, 0, 0, 0.23);
                }}
            </style>
        </head>

        <body>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; width: 75%;">
                <h1 style="color: #434343;">Strava Analytics</h1>
                <p style="font-size: 16px; color: #434343; font-weight: bold;">Don't know what strava is? <a href="https://www.strava.com/athletes/98390356">Check out my profile</a></p>
                <img src='data:image/png;base64,{encoded}' alt="matplotlib fig derived from strava data" style="margin: 20px auto; width: 100%;">
                <div style="width: 75%; margin: auto;">
                    <p style="font-size: 20px; color: #434343;">TODO: Add project description with other info/links to code and account</p>
                </div>
            </div>
        </body>

    </html>
    """