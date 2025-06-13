import pyhtml

def get_page_html(form_data=None):
    print("About to return page 2 (dynamic with form and results)")

    # Default values for form inputs if none submitted
    state = form_data.get('state')[0] if form_data and 'state' in form_data else ""
    lat_start = form_data.get('lat_start')[0] if form_data and 'lat_start' in form_data else ""
    lat_end = form_data.get('lat_end')[0] if form_data and 'lat_end' in form_data else ""
    metric = form_data.get('metric')[0] if form_data and 'metric' in form_data else "MaxTemp"
    sort_by = form_data.get('sort_by')[0] if form_data and 'sort_by' in form_data else "Region"

    results = []
    error_msg = ""

    if form_data:
        try:
            lat_start_val = float(lat_start)
            lat_end_val = float(lat_end)

            if not (-90 <= lat_start_val <= 90 and -90 <= lat_end_val <= 90):
                error_msg = "Latitude values must be between -90 and 90."
            elif lat_start_val > lat_end_val:
                error_msg = "Start latitude must be less than or equal to end latitude."
            elif state == "":
                error_msg = "Please select a state."
            else:
                # Escape state to prevent SQL errors
                state_escaped = state.replace("'", "''")

                # Validate metric and sort_by inputs (only allow known safe values)
                valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
                valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

                if metric not in valid_metrics:
                    metric = 'MaxTemp'
                if sort_by not in valid_sort_by:
                    sort_by = 'Region'

                # Build query string with injected sanitized values (no params tuple)
                query = f"""
                    SELECT s.Region, COUNT(*) as Number_Weather_Stations, 
                           ROUND(AVG(w.{metric}), 2) as Average_Metric
                    FROM WeatherData w
                    JOIN Sites s ON w.Location = s.SiteID
                    WHERE s.State = '{state_escaped}'
                      AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
                    GROUP BY s.Region
                    ORDER BY {sort_by} ASC;
                """

                # Call your get_results_from_query without params tuple
                results = pyhtml.get_results_from_query("weatherdata.db", query)

        except ValueError:
            error_msg = "Latitude inputs must be valid numbers."
        except Exception as e:
            error_msg = f"Error running query: {e}"

    # Build the results table rows as HTML
    table_rows_html = ""
    if results:
        for row in results:
            region, num_stations, avg_metric = row
            table_rows_html += f"""
            <tr>
                <td>{region}</td>
                <td>{num_stations}</td>
                <td>{avg_metric}</td>
            </tr>"""
    elif form_data and not error_msg:
        table_rows_html = "<tr><td colspan='3'>No results found.</td></tr>"

    # Build the entire page HTML string (unchanged)
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Australia Climate Watch - State View</title>
    <link rel="stylesheet" href="/style.css" />
</head>
<body>
    <header class="site-header">
        <h1>Australia Climate Watch</h1>
        <nav class="nav-bar">
            <a href="/">Home</a>
            <a href="/page2a" aria-current="page">State View</a>
            <a href="/page3a">Compare Regions</a>
        </nav>
    </header>

    <main class="state-main">
        <h2>🌍 Explore Weather Stations by State</h2>
        <form method="GET" action="/page2a" class="filter-bar">
            <label for="state">Select State:</label>
            <select id="state" name="state" required>
                <option value="">--Select State--</option>
                <option value="VIC" {"selected" if state=="VIC" else ""}>Victoria</option>
                <option value="NSW" {"selected" if state=="NSW" else ""}>New South Wales</option>
                <option value="QLD" {"selected" if state=="QLD" else ""}>Queensland</option>
                <option value="WA" {"selected" if state=="WA" else ""}>Western Australia</option>
                <option value="SA" {"selected" if state=="SA" else ""}>South Australia</option>
                <option value="TAS" {"selected" if state=="TAS" else ""}>Tasmania</option>
                <option value="NT" {"selected" if state=="NT" else ""}>Northern Territory</option>
                <option value="ACT" {"selected" if state=="ACT" else ""}>ACT</option>
            </select>

            <label for="lat_start">Start Latitude:</label>
            <input type="number" step="0.01" min="-90" max="90" id="lat_start" name="lat_start" value="{lat_start}" required />

            <label for="lat_end">End Latitude:</label>
            <input type="number" step="0.01" min="-90" max="90" id="lat_end" name="lat_end" value="{lat_end}" required />

            <label for="metric">Select Climate Metric:</label>
            <select id="metric" name="metric" required>
                <option value="MaxTemp" {"selected" if metric=="MaxTemp" else ""}>Max Temperature</option>
                <option value="MinTemp" {"selected" if metric=="MinTemp" else ""}>Min Temperature</option>
                <option value="Rainfall" {"selected" if metric=="Rainfall" else ""}>Rainfall</option>
            </select>

            <label for="sort_by">Sort By:</label>
            <select id="sort_by" name="sort_by" required>
                <option value="Region" {"selected" if sort_by=="Region" else ""}>Region</option>
                <option value="Number_Weather_Stations" {"selected" if sort_by=="Number_Weather_Stations" else ""}>Number of Stations</option>
                <option value="Average_Metric" {"selected" if sort_by=="Average_Metric" else ""}>Average Metric</option>
            </select>

            <button type="submit">Filter</button>
        </form>

        <section class='table-container'>
            <table class='data-table'>
                <thead>
                    <tr>
                        <th>Region</th>
                        <th>Number of Stations</th>
                        <th>Average Metric</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </section>

        {f"<p style='color:red;'>{error_msg}</p>" if error_msg else ""}
    </main>

    <footer class="site-footer">
        <div class="footer-icons">ⓘ ♿ 🎧</div>
        <div class="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Contact</a>
            <a href="#">About</a>
        </div>
    </footer>
</body>
</html>"""

    return page_html

