def get_page_html(form_data=None):
    print("About to return page 2 (static version)")

    page_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Australia Climate Watch - State View</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <header class="site-header">
        <h1>Australia Climate Watch</h1>
        <nav class="nav-bar">
            <a href="/">Home</a>
            <a href="/page2a" class="active">State View</a>
            <a href="/page3a">Compare Regions</a>
        </nav>
    </header>

    <main class="state-view-main">
        <section class="state-selection">
            <h2>Select state</h2>
            <div class="state-buttons">
                <button class="state-btn">VIC</button>
                <button class="state-btn">NSW</button>
                <button class="state-btn">QLD</button>
                <button class="state-btn">WA</button>
                <button class="state-btn">SA</button>
                <button class="state-btn">TAS</button>
                <button class="state-btn">NT</button>
            </div>
        </section>

        <section class="station-info">
            <h3>STATION: Adelaide Airport</h3>
            <p><strong>STATION ID:</strong> 260123</p>
            <div class="station-stats">
                <div class="stat-item">🔥 <strong>Max Temp:</strong> 33°C</div>
                <div class="stat-item">🌧️ <strong>Rainfall This Week:</strong> 12mm</div>
                <div class="stat-item alert">🚨 <strong>Status:</strong> Fire Alert Active</div>
            </div>
            <a href="#" class="view-station-btn">View Station →</a>
        </section>

        <section class="filter-search">
            <h3>FILTER SEARCH</h3>
            <div class="filter-options">
                <label><input type="checkbox" name="filter" value="rain"> Most Rain</label>
                <label><input type="checkbox" name="filter" value="temp"> Highest Temp</label>
                <label><input type="checkbox" name="filter" value="fire"> Fire Alerts</label>
                <label><input type="checkbox" name="filter" value="safe"> Safe Zones</label>
            </div>
        </section>

        <section class="station-detail">
            <h3>STATION NAME: ADELAIDE STATION</h3>
            <div class="alert-box">
                <p>⚠️ "A Fire Warning is in effect – Stay indoors 2–5pm"</p>
            </div>
            <div class="text-summary">
                <p>"This region will experience dry heat and minimal rainfall for the next 5 days. No flooding risk detected."</p>
            </div>
        </section>

        <section class="database-results">
            <h2>Database Results (Sample Static Table)</h2>
            <table class='data-table'>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Year</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>Firestorm</td>
                    <td>2023</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Rainy Days</td>
                    <td>2021</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Climate Shift</td>
                    <td>2022</td>
                </tr>
            </table>
        </section>
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
</html>
"""
    return page_html

