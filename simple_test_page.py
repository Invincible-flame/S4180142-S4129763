
# def get_page_html(form_data=None):
#     from pyhtml import get_results_from_query

#     # Use default test values if no form data
#     state = form_data.get('state', ['VIC'])[0] if form_data else 'VIC'
#     lat_start = form_data.get('lat_start', ['-38'])[0] if form_data else '-38'
#     lat_end = form_data.get('lat_end', ['-36'])[0] if form_data else '-36'
#     metric = form_data.get('metric', ['MaxTemp'])[0] if form_data else 'MaxTemp'
#     sort_by = form_data.get('sort_by', ['Region'])[0] if form_data else 'Region'

#     error_msg = ""
#     results = []

#     try:
#         # Escape single quotes in state to prevent SQL errors
#         state_escaped = state.replace("'", "''")
#         lat_start_float = float(lat_start)
#         lat_end_float = float(lat_end)

#         # Sanitize metric and sort_by to avoid SQL injection by limiting allowed values
#         valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
#         valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

#         if metric not in valid_metrics:
#             metric = 'MaxTemp'
#         if sort_by not in valid_sort_by:
#             sort_by = 'Region'

#         query = f"""
#             SELECT 
#                 s.Region, 
#                 COUNT(*) AS Number_Weather_Stations, 
#                 ROUND(AVG(w.{metric}), 2) AS Average_Metric
#             FROM WeatherData w
#             JOIN Sites s ON w.Location = s.SiteID
#             WHERE s.State = '{state_escaped}'
#               AND s.Latitude BETWEEN {lat_start_float} AND {lat_end_float}
#             GROUP BY s.Region
#             ORDER BY {sort_by} ASC
#         """

#         results = get_results_from_query("weatherdata.db", query)

#     except Exception as e:
#         error_msg = f"Error running query: {e}"

#     # Build HTML table of results
#     rows_html = ""
#     if results:
#         for region, num_stations, avg_metric in results:
#             rows_html += f"<tr><td>{region}</td><td>{num_stations}</td><td>{avg_metric}</td></tr>"
#     else:
#         rows_html = "<tr><td colspan='3'>No results found.</td></tr>"

#     # Return simple HTML page
#     html = f"""
#     <html>
#     <head><title>Test Query Results</title></head>
#     <body>
#         <h2>Weather Stations Summary</h2>
#         <p>State: {state}, Latitude Between: {lat_start} and {lat_end}, Metric: {metric}, Sorted By: {sort_by}</p>
#         <table border="1" cellpadding="5" cellspacing="0">
#             <thead>
#                 <tr>
#                     <th>Region</th>
#                     <th>Number of Stations</th>
#                     <th>Average Metric</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {rows_html}
#             </tbody>
#         </table>
#         <p style="color:red;">{error_msg}</p>
#     </body>
#     </html>
#     """

#     return html

def get_page_html(form_data=None):
    from pyhtml import get_results_from_query

    # Form input defaults or actual user input
    state = form_data.get('state', ['VIC'])[0] if form_data else 'VIC'
    lat_start = form_data.get('lat_start', ['-38'])[0] if form_data else '-38'
    lat_end = form_data.get('lat_end', ['-36'])[0] if form_data else '-36'
    metric = form_data.get('metric', ['MaxTemp'])[0] if form_data else 'MaxTemp'
    sort_by = form_data.get('sort_by', ['Region'])[0] if form_data else 'Region'

    error_msg = ""
    results = []

    try:
        # Input sanitization
        state_escaped = state.replace("'", "''")
        lat_start_float = float(lat_start)
        lat_end_float = float(lat_end)

        valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
        valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

        if metric not in valid_metrics:
            metric = 'MaxTemp'
        if sort_by not in valid_sort_by:
            sort_by = 'Region'

        query = f"""
            SELECT 
                s.Region, 
                COUNT(*) AS Number_Weather_Stations, 
                ROUND(AVG(w.{metric}), 2) AS Average_Metric
            FROM WeatherData w
            JOIN Sites s ON w.Location = s.SiteID
            WHERE s.State = '{state_escaped}'
              AND s.Latitude BETWEEN {lat_start_float} AND {lat_end_float}
            GROUP BY s.Region
            ORDER BY {sort_by} ASC
        """
        print(query)

        results = get_results_from_query("weatherdata.db", query)

    except ValueError:
        error_msg = "Latitude inputs must be valid numbers."
    except Exception as e:
        error_msg = f"Error running query: {e}"

    # Build result rows
    rows_html = ""
    if results:
        for region, num_stations, avg_metric in results:
            rows_html += f"<tr><td>{region}</td><td>{num_stations}</td><td>{avg_metric}</td></tr>"
    else:
        rows_html = "<tr><td colspan='3'>No results found.</td></tr>"

    # Return page with form and results
    html = f"""
    <html>
    <head>
        <title>State Query Page</title>
    </head>
    <body>
        <h1>Weather Station Summary</h1>
        <form method="get" action="/page2a">
            <label>State:
                <select name="state" required>
                    <option value="VIC" {"selected" if state=="VIC" else ""}>VIC</option>
                    <option value="NSW" {"selected" if state=="NSW" else ""}>NSW</option>
                    <option value="QLD" {"selected" if state=="QLD" else ""}>QLD</option>
                    <option value="WA" {"selected" if state=="WA" else ""}>WA</option>
                    <option value="SA" {"selected" if state=="SA" else ""}>SA</option>
                    <option value="TAS" {"selected" if state=="TAS" else ""}>TAS</option>
                    <option value="NT" {"selected" if state=="NT" else ""}>NT</option>
                    <option value="ACT" {"selected" if state=="ACT" else ""}>ACT</option>
                </select>
            </label><br><br>

            <label>Start Latitude:
                <input type="text" name="lat_start" value="{lat_start}" required />
            </label><br><br>

            <label>End Latitude:
                <input type="text" name="lat_end" value="{lat_end}" required />
            </label><br><br>

            <label>Metric:
                <select name="metric">
                    <option value="MaxTemp" {"selected" if metric=="MaxTemp" else ""}>MaxTemp</option>
                    <option value="MinTemp" {"selected" if metric=="MinTemp" else ""}>MinTemp</option>
                    <option value="Rainfall" {"selected" if metric=="Rainfall" else ""}>Rainfall</option>
                </select>
            </label><br><br>

            <label>Sort By:
                <select name="sort_by">
                    <option value="Region" {"selected" if sort_by=="Region" else ""}>Region</option>
                    <option value="Number_Weather_Stations" {"selected" if sort_by=="Number_Weather_Stations" else ""}>Number of Stations</option>
                    <option value="Average_Metric" {"selected" if sort_by=="Average_Metric" else ""}>Average Metric</option>
                </select>
            </label><br><br>

            <button type="submit">Submit</button>
        </form>

        <p style="color:red;">{error_msg}</p>

        <h2>Results</h2>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Number of Stations</th>
                    <th>Average Metric</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </body>
    </html>
    """

    return html
