#!/usr/bin/env python3
"""
InfoStealer-Analyzer Web UI: Ethical InfoStealer Detection & Education Tool
Strictly for defensive, educational, and ethical use only.
"""
from flask import Flask, render_template_string, request, send_file, jsonify
import os
import json
import csv
from datetime import datetime
from main import run_full_scan, FINDINGS

app = Flask(__name__)

BANNER = """
<div class='alert alert-primary mt-3' role='alert'>
  <h3>InfoStealer-Analyzer (Defensive Edition)</h3>
  <p>For Cybersecurity Education & Awareness<br>
  <b>Strictly for ethical, defensive, and educational use only.</b></p>
</div>
"""

THREAT_INTEL = [
    {
        'Scan Type': 'Suspicious Process Scan',
        'MITRE ATT&CK': 'T1057 (Process Discovery), T1204',
        'Description': 'Detects processes matching known malware names',
        'Link': 'https://attack.mitre.org/techniques/T1057/'
    },
    {
        'Scan Type': 'Suspicious Directory Scan',
        'MITRE ATT&CK': 'T1083 (File and Directory Discovery)',
        'Description': 'Looks for suspicious files in common drop locations',
        'Link': 'https://attack.mitre.org/techniques/T1083/'
    },
    {
        'Scan Type': 'Browser Data Access Scan',
        'MITRE ATT&CK': 'T1539 (Steal Web Session Cookie), T1114',
        'Description': 'Simulates browser data access attempts',
        'Link': 'https://attack.mitre.org/techniques/T1539/'
    },
    {
        'Scan Type': 'Discord Token Theft Scan',
        'MITRE ATT&CK': 'T1555 (Credentials from Password Stores)',
        'Description': 'Simulates Discord token theft attempts',
        'Link': 'https://attack.mitre.org/techniques/T1555/'
    },
    {
        'Scan Type': 'Vulnerable Path Scan',
        'MITRE ATT&CK': 'T1574 (Hijack Execution Flow)',
        'Description': 'Lists world-writable or sensitive paths',
        'Link': 'https://attack.mitre.org/techniques/T1574/'
    },
]

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>InfoStealer-Analyzer Web UI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-4">
    {{ banner|safe }}
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <a class="nav-link {% if active_tab == 'scan' %}active{% endif %}" href="/">Scan</a>
      </li>
      <li class="nav-item">
        <a class="nav-link {% if active_tab == 'threat' %}active{% endif %}" href="/threat">Threat Intelligence</a>
      </li>
    </ul>
    {% if active_tab == 'scan' %}
    <div class="card mb-3">
        <div class="card-body">
            <form method="post">
                <button class="btn btn-success" type="submit" name="action" value="scan">Run Scan</button>
                {% if findings %}
                <a href="/export/json" class="btn btn-primary ms-2">Export JSON</a>
                <a href="/export/csv" class="btn btn-secondary ms-2">Export CSV</a>
                <a href="/export/markdown" class="btn btn-info ms-2">Export Markdown Report</a>
                {% endif %}
            </form>
        </div>
    </div>
    {% if findings %}
    <div class="card">
        <div class="card-header">Scan Results ({{ findings|length }})</div>
        <div class="card-body p-0">
            <div class="table-responsive">
            <table class="table table-striped table-bordered mb-0">
                <thead>
                <tr>
                    {% for k in headings %}<th>{{ k }}</th>{% endfor %}
                </tr>
                </thead>
                <tbody>
                {% for row in findings %}
                <tr>
                    {% for k in headings %}<td>{{ row.get(k, '') }}</td>{% endfor %}
                </tr>
                {% endfor %}
                </tbody>
            </table>
            </div>
        </div>
    </div>
    {% endif %}
    {% elif active_tab == 'threat' %}
    <div class="card">
      <div class="card-header">Threat Intelligence Mapping (MITRE ATT&CK)</div>
      <div class="card-body p-0">
        <div class="table-responsive">
        <table class="table table-striped table-bordered mb-0">
          <thead>
            <tr>
              <th>Scan Type</th>
              <th>MITRE ATT&CK</th>
              <th>Description</th>
              <th>Reference</th>
            </tr>
          </thead>
          <tbody>
            {% for row in threat_intel %}
            <tr>
              <td>{{ row['Scan Type'] }}</td>
              <td>{{ row['MITRE ATT&CK'] }}</td>
              <td>{{ row['Description'] }}</td>
              <td><a href="{{ row['Link'] }}" target="_blank">MITRE Link</a></td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        </div>
      </div>
    </div>
    {% endif %}
    <footer class="mt-4 text-center text-muted">
        &copy; 2024 InfoStealer-Analyzer. For educational use only.
    </footer>
</div>
</body>
</html>
'''

LATEST_RESULTS = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global LATEST_RESULTS
    if request.method == 'POST' and request.form.get('action') == 'scan':
        LATEST_RESULTS = run_full_scan()
    headings = sorted({k for d in LATEST_RESULTS for k in d.keys()}) if LATEST_RESULTS else []
    return render_template_string(TEMPLATE, banner=BANNER, findings=LATEST_RESULTS, headings=headings, active_tab='scan', threat_intel=THREAT_INTEL)

@app.route('/threat')
def threat():
    return render_template_string(TEMPLATE, banner=BANNER, findings=[], headings=[], active_tab='threat', threat_intel=THREAT_INTEL)

@app.route('/export/<fmt>')
def export(fmt):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    if not LATEST_RESULTS:
        return 'No results to export.', 400
    if fmt == 'json':
        out_path = f'analyzer_results/web_{now}.json'
        with open(out_path, 'w') as f:
            json.dump(LATEST_RESULTS, f, indent=2)
        return send_file(out_path, as_attachment=True)
    elif fmt == 'csv':
        out_path = f'analyzer_results/web_{now}.csv'
        keys = sorted({k for d in LATEST_RESULTS for k in d.keys()})
        with open(out_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(LATEST_RESULTS)
        return send_file(out_path, as_attachment=True)
    elif fmt == 'markdown':
        out_path = f'analyzer_results/web_{now}.md'
        with open(out_path, 'w') as f:
            f.write(f"# InfoStealer-Analyzer Report\n\n")
            f.write(f"**Date:** {now}\n\n")
            f.write(f"## Findings ({len(LATEST_RESULTS)})\n\n")
            for i, finding in enumerate(LATEST_RESULTS, 1):
                f.write(f"### Finding {i}\n")
                for k, v in finding.items():
                    f.write(f"- **{k}**: {v}\n")
                f.write("\n")
            f.write("---\n\n## Recommendations\n")
            f.write("- Review all flagged processes and files.\n")
            f.write("- Ensure your system is patched and up to date.\n")
            f.write("- Use endpoint protection and monitor for suspicious activity.\n")
            f.write("- This report is for educational and awareness purposes only.\n")
        return send_file(out_path, as_attachment=True)
    else:
        return 'Unknown format', 400

if __name__ == '__main__':
    os.makedirs('analyzer_results', exist_ok=True)
    app.run(port=5001, debug=True) 