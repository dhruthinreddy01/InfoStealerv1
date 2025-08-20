from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session, g
import os
import json
import datetime
import uuid
from werkzeug.utils import secure_filename
from collections import Counter
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'infosec-educational-demo'
DATA_DIR = 'stolen_data'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Supported languages
LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी'
}

# UI translations (add more as needed)
UI_STRINGS = {
    'en': {
        'project_title': 'InfoSnare Web',
        'subtitle': 'Ethical Info Stealer Simulation for Cybersecurity Training',
        'disclaimer': '⚠️ Educational Simulation Only – No real data is accessed or stored.',
        'system_info': 'System Info',
        'clipboard': 'Clipboard Text',
        'website': 'Website URL',
        'username': 'Username',
        'password': 'Password',
        'file_upload': 'Fake Document Name (optional)',
        'file_upload_help': 'Upload a fake file to simulate document exfiltration (no real files are processed).',
        'submit': 'Simulate Steal',
        'os': 'Operating System',
        'antivirus': 'Antivirus',
        'location': 'Location (simulated)',
        'report_title': 'Simulated "Stolen" Report',
        'download_report': 'Download Report',
        'back_to_form': 'Back to Form',
        'footer': 'Made with ❤️ by Dhruthi N. Reddy – For Cybersecurity Training Only',
        'for_edu': 'For educational use only. No real data is collected.',
        'toggle_dark': 'Toggle dark mode',
        'language': 'Language',
        'hindi': 'हिंदी',
        'english': 'EN',
        'field_empty': 'Not provided',
        'field_ok': 'Captured',
        'field_missing': 'Missing',
    },
    'hi': {
        'project_title': 'इन्फो-स्नेयर वेब',
        'subtitle': 'साइबर सुरक्षा प्रशिक्षण के लिए नैतिक इन्फो-चोरी सिमुलेशन',
        'disclaimer': '⚠️ केवल शैक्षिक सिमुलेशन – कोई वास्तविक डेटा एक्सेस या संग्रहित नहीं किया जाता।',
        'system_info': 'सिस्टम जानकारी',
        'clipboard': 'क्लिपबोर्ड टेक्स्ट',
        'website': 'वेबसाइट यूआरएल',
        'username': 'यूज़रनेम',
        'password': 'पासवर्ड',
        'file_upload': 'फेक डॉक्युमेंट नाम (वैकल्पिक)',
        'file_upload_help': 'डॉक्युमेंट एक्सफिल सिमुलेट करने के लिए फेक फाइल अपलोड करें (कोई असली फाइल प्रोसेस नहीं होती)।',
        'submit': 'सिमुलेट चोरी',
        'os': 'ऑपरेटिंग सिस्टम',
        'antivirus': 'एंटीवायरस',
        'location': 'स्थान (काल्पनिक)',
        'report_title': 'सिम्युलेटेड "चोरी" रिपोर्ट',
        'download_report': 'रिपोर्ट डाउनलोड करें',
        'back_to_form': 'फॉर्म पर वापस जाएं',
        'footer': '❤️ से बनाया - धृति एन. रेड्डी द्वारा – केवल साइबर सुरक्षा प्रशिक्षण के लिए',
        'for_edu': 'केवल शैक्षिक उपयोग के लिए। कोई वास्तविक डेटा संग्रहित नहीं किया जाता।',
        'toggle_dark': 'डार्क मोड टॉगल करें',
        'language': 'भाषा',
        'hindi': 'हिंदी',
        'english': 'EN',
        'field_empty': 'प्रदान नहीं किया गया',
        'field_ok': 'कैप्चर किया गया',
        'field_missing': 'गायब',
    }
}

def get_lang():
    return session.get('lang', 'en')

def t(key):
    lang = get_lang()
    return UI_STRINGS.get(lang, UI_STRINGS['en']).get(key, key)

@app.before_request
def before_request():
    g.lang = get_lang()
    g.t = t
    g.LANGUAGES = LANGUAGES

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('form'))

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def sanitize_input(text):
    """Basic input sanitization to prevent XSS in simulation."""
    if not isinstance(text, str):
        return ''
    return text.replace('<', '&lt;').replace('>', '&gt;').strip()

# --- User routes ---
@app.route('/', methods=['GET'])
def form():
    return render_template('form.html', t=t, lang=g.lang, LANGUAGES=LANGUAGES)

@app.route('/submit', methods=['POST'])
def submit():
    # Get and sanitize user input
    os_field = sanitize_input(request.form.get('os', ''))
    system_info = sanitize_input(request.form.get('system_info', ''))
    antivirus = sanitize_input(request.form.get('antivirus', ''))
    location = sanitize_input(request.form.get('location', ''))
    clipboard = sanitize_input(request.form.get('clipboard', ''))
    website = sanitize_input(request.form.get('website', ''))
    username = sanitize_input(request.form.get('username', ''))
    password = sanitize_input(request.form.get('password', ''))
    fakefile = request.files.get('fakefile')
    fakefile_name = ''
    if fakefile and fakefile.filename:
        fakefile_name = secure_filename(fakefile.filename)
        # Do not save the file, just record the name for simulation

    # Simulated metadata
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr or '127.0.0.1'
    user_agent = request.user_agent.string or 'Unknown'
    session_id = str(uuid.uuid4())[:8]

    # Prepare data dict
    data = {
        'os': os_field,
        'system_info': system_info,
        'antivirus': antivirus,
        'location': location,
        'clipboard': clipboard,
        'website': website,
        'username': username,
        'password': password,
        'fakefile_name': fakefile_name,
        'timestamp': timestamp,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'session_id': session_id
    }

    # Save to JSON file
    filename = f"info_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id}.json"
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        flash(f"Error saving report: {e}", 'danger')
        return redirect(url_for('form'))

    # Pass filename for download
    return render_template('result.html', data=data, filename=filename, t=t, lang=g.lang, LANGUAGES=LANGUAGES)

@app.route('/download/<filename>')
def download_report(filename):
    # Secure the filename and send the file for download
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f"Download failed: {e}", 'danger')
        return redirect(url_for('form'))

# --- Admin routes ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Login form
    if not session.get('admin_logged_in'):
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == ADMIN_PASSWORD:
                session['admin_logged_in'] = True
                return redirect(url_for('admin'))
            else:
                flash('Incorrect password.', 'danger')
        return render_template('admin_login.html', t=t, lang=g.lang, LANGUAGES=LANGUAGES)

    # List all reports
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    files.sort(reverse=True)
    reports = []
    os_list = []
    for fname in files:
        try:
            with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                report = json.load(f)
                report['filename'] = fname
                reports.append(report)
                os_list.append(report.get('os', 'Unknown'))
        except Exception:
            continue
    # Stats
    total_reports = len(reports)
    most_common_os = Counter(os_list).most_common(1)[0][0] if os_list else 'N/A'
    return render_template('admin_dashboard.html', reports=reports, total_reports=total_reports, most_common_os=most_common_os, t=t, lang=g.lang, LANGUAGES=LANGUAGES)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('admin'))

@app.route('/admin/view/<filename>')
def admin_view(filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('admin_view.html', data=data, filename=filename, t=t, lang=g.lang, LANGUAGES=LANGUAGES)
    except Exception as e:
        flash(f"Could not open report: {e}", 'danger')
        return redirect(url_for('admin'))

@app.route('/admin/delete/<filename>', methods=['POST'])
def admin_delete(filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        os.remove(file_path)
        flash('Report deleted.', 'success')
    except Exception as e:
        flash(f"Delete failed: {e}", 'danger')
    return redirect(url_for('admin'))

@app.route('/admin/download/<filename>')
def admin_download(filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f"Download failed: {e}", 'danger')
        return redirect(url_for('admin'))

@app.route('/admin/download_all')
def admin_download_all():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    # Create a zip of all reports in memory
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for fname in os.listdir(DATA_DIR):
            if fname.endswith('.json'):
                zf.write(os.path.join(DATA_DIR, fname), arcname=fname)
    mem_zip.seek(0)
    return send_file(mem_zip, as_attachment=True, download_name='all_reports.zip', mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True) 