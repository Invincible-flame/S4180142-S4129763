
import pyhtml

def get_page_html(form_data=None):
    print("About to return State View page")
    print(f"Raw form_data: {form_data}")  # Debug print to check exact received data

    # Get user inputs safely from form or set defaults
    if form_data and 'state' in form_data:
        # form_data values might be a list, get first element safely
        state_raw = form_data.get('state')
        if isinstance(state_raw, list):
            state = state_raw[0]
        else:
            state = state_raw
    else:
        state = ''

    # Hardcoded latitudes for testing
    lat_start_val = -38.0
    lat_end_val = -34.0

    metric = form_data.get('metric', ['MaxTemp'])[0] if form_data else 'MaxTemp'
    sort_by = form_data.get('sort_by', ['Region'])[0] if form_data else 'Region'

    print(f"Parsed inputs -> state: {state}, metric: {metric}, sort_by: {sort_by}")  # Debug print

    table1_results, table2_results = [], []
    error_msg = ""

    try:
        if not state:
            error_msg = "Please select a state."
        else:
            # Escape single quotes for safety
            state_escaped = state.replace("'", "''")

            valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
            valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

            if metric not in valid_metrics:
                metric = 'MaxTemp'
            if sort_by not in valid_sort_by:
                sort_by = 'Region'

            query1 = f"""
                SELECT s.Name, s.Region, s.Latitude
                FROM Sites s
                WHERE s.State = '{state_escaped}'
                  AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
                ORDER BY s.Region;
            """

            query2 = f"""
                SELECT s.Region,
                       COUNT(*) AS Number_Weather_Stations,
                       ROUND(AVG(w.{metric}), 2) AS Average_Metric
                FROM WeatherData w
                JOIN Sites s ON w.Location = s.SiteID
                WHERE s.State = '{state_escaped}'
                  AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
                GROUP BY s.Region
                ORDER BY {sort_by};
            """

            table1_results = pyhtml.get_results_from_query("weatherdata.db", query1)
            table2_results = pyhtml.get_results_from_query("weatherdata.db", query2)

    except Exception as e:
        error_msg = f"Error: {e}"

    table1_html = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in table1_results
    ]) or "<tr><td colspan='3'>No results found.</td></tr>"

    table2_html = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in table2_results
    ]) or "<tr><td colspan='3'>No summary data found.</td></tr>"

    return f"""
<html>
<head>
  <title>Climate Summary</title>
  <link rel="stylesheet" href="/style.css" />
</head>
<body>
  <header class="site-header">
    <h1>Explore Weather Stations</h1> <h1>Australia Climate Watch</h1>
        <nav class="nav-bar">
            <a href="/" class="active">Home</a>
            <a href="/page2a">State View</a>
            <a href="/page3a">Compare Regions</a>
        </nav>

  </header>

  <main class="state-view-main">
    <form method='GET' action='/page2a' class="filter-search">
      <label>State:
        <select name='state' required>
          <option value=''>--Select--</option>
          {''.join([f"<option value='{s}' {'selected' if s == state else ''}>{s}</option>" for s in ['VIC','NSW','QLD','WA','SA','TAS','NT','ACT']])}
        </select>
      </label>
      <p>Latitude range is fixed for testing: from {lat_start_val} to {lat_end_val}</p>

      <label>Metric:
        <select name='metric'>
          <option value='MaxTemp' {'selected' if metric == 'MaxTemp' else ''}>MaxTemp</option>
          <option value='MinTemp' {'selected' if metric == 'MinTemp' else ''}>MinTemp</option>
          <option value='Rainfall' {'selected' if metric == 'Rainfall' else ''}>Rainfall</option>
        </select>
      </label>

      <label>Sort By:
        <select name='sort_by'>
          <option value='Region' {'selected' if sort_by == 'Region' else ''}>Region</option>
          <option value='Number_Weather_Stations' {'selected' if sort_by == 'Number_Weather_Stations' else ''}># Stations</option>
          <option value='Average_Metric' {'selected' if sort_by == 'Average_Metric' else ''}>Avg Metric</option>
        </select>
      </label>

      <button type='submit' class="cta-button">Submit</button>
    </form>

    <p style='color:red;'>{error_msg}</p>

    <section class="station-info">
      <h2>📍 Weather Stations in Selected State</h2>
      <table class="data-table" border='1'>
        <thead>
          <tr><th>Site Name</th><th>Region</th><th>Latitude</th></tr>
        </thead>
        <tbody>
          {table1_html}
        </tbody>
      </table>
    </section>

    <section class="station-detail">
      <h2>📊 Regional Climate Summary</h2>
      <table class="data-table" border='1'>
        <thead>
          <tr><th>Region</th><th>Number Weather Stations</th><th>Average {metric}</th></tr>
        </thead>
        <tbody>
          {table2_html}
        </tbody>
      </table>
    </section>
  </main>

  <footer class="site-footer">
    <p>&copy; 2025 Climate Data Viewer</p>
  </footer>
</body>
</html>
"""


