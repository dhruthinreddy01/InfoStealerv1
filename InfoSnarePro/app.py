import os
import json
import datetime
import uuid
import secrets
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session, g
from werkzeug.utils import secure_filename
from utils.risk import calculate_risk_score
from utils.pdfgen import generate_pdf

app = Flask(__name__)
app.secret_key = 'infonsarepro-secret-key'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
DATA_DIR = 'stolen_data'

LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी'
}

UI_STRINGS = {
    'en': {
        'project_title': 'InfoSnare Pro',
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
        'download_report': 'Download Report (.json)',
        'download_pdf': 'Download PDF',
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
        'risk_score': 'Risk Score',
        'risk_level': 'Risk Level',
        'summary': 'Summary',
        'high_risk': 'High risk: Most sensitive fields captured.',
        'medium_risk': 'Medium risk: Some sensitive fields captured.',
        'low_risk': 'Low risk: Minimal sensitive data captured.',
        'csrf_error': 'Session expired or invalid form. Please try again.',
        'required_error': 'Please fill all required fields.',
    },
    'hi': {
        'project_title': 'इन्फो-स्नेयर प्रो',
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
        'download_report': 'रिपोर्ट डाउनलोड करें (.json)',
        'download_pdf': 'पीडीएफ डाउनलोड करें',
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
        'risk_score': 'जोखिम स्कोर',
        'risk_level': 'जोखिम स्तर',
        'summary': 'सारांश',
        'high_risk': 'उच्च जोखिम: अधिकांश संवेदनशील फ़ील्ड कैप्चर किए गए।',
        'medium_risk': 'मध्यम जोखिम: कुछ संवेदनशील फ़ील्ड कैप्चर किए गए।',
        'low_risk': 'न्यून जोखिम: न्यूनतम संवेदनशील डेटा कैप्चर किया गया।',
        'csrf_error': 'सत्र समाप्त या अमान्य फॉर्म। कृपया पुनः प्रयास करें।',
        'required_error': 'कृपया सभी आवश्यक फ़ील्ड भरें।',
    }
}

def get_lang():
    return session.get('lang', 'en')

def t(key):
    lang = get_lang()
    return UI_STRINGS.get(lang, UI_STRINGS['en']).get(key, key)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(16)
    return session['_csrf_token']

@app.before_request
def before_request():
    g.lang = get_lang()
    g.t = t
    g.LANGUAGES = LANGUAGES
    g.csrf_token = generate_csrf_token()

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('form'))

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html', t=t, lang=g.lang, LANGUAGES=LANGUAGES, csrf_token=g.csrf_token)

@app.route('/submit', methods=['POST'])
def submit():
    # CSRF check
    if request.form.get('csrf_token') != session.get('_csrf_token'):
        flash(t('csrf_error'), 'danger')
        return redirect(url_for('form'))
    # Input validation
    required_fields = ['os', 'system_info', 'clipboard', 'username', 'password']
    for field in required_fields:
        value = request.form.get(field, '').strip()
        if not value or len(value) > 200:
            flash(t('required_error'), 'danger')
            return redirect(url_for('form'))
    os_field = request.form.get('os', '')
    system_info = request.form.get('system_info', '')
    antivirus = request.form.get('antivirus', '')
    location = request.form.get('location', '')
    clipboard = request.form.get('clipboard', '')
    website = request.form.get('website', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    fakefile = request.files.get('fakefile')
    fakefile_name = ''
    if fakefile and fakefile.filename:
        fakefile_name = secure_filename(fakefile.filename)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr or '127.0.0.1'
    user_agent = request.user_agent.string or 'Unknown'
    session_id = str(uuid.uuid4())[:8]
    data = {
        'os': os_field,
        'system_info': system_info,
        'antivirus': antivirus,
        'location': location,
        'clipboard': clipboard,
        'website': website,
        'username': username,
        'password': password,
        'file_uploaded': fakefile_name,
        'timestamp': timestamp,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'session_id': session_id
    }
    risk_score, risk_level = calculate_risk_score(data)
    filename = f"info_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id}.json"
    filepath = os.path.join(DATA_DIR, filename)
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        flash(f"Error saving report: {e}", 'danger')
        return redirect(url_for('form'))
    flash('Report generated successfully!', 'success')
    return render_template('result.html', data=data, filename=filename, t=t, lang=g.lang, LANGUAGES=LANGUAGES, risk_score=risk_score, risk_level=risk_level)

@app.route('/download/<filename>')
def download_report(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f"Download failed: {e}", 'danger')
        return redirect(url_for('form'))

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(DATA_DIR, safe_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        risk_score, risk_level = calculate_risk_score(data)
        pdf_buffer = generate_pdf(data, risk_score, risk_level)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"{safe_name.replace('.json', '.pdf')}", mimetype='application/pdf')
    except Exception as e:
        flash(f"PDF download failed: {e}", 'danger')
        return redirect(url_for('form'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', t=t, lang=g.lang, LANGUAGES=LANGUAGES), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', t=t, lang=g.lang, LANGUAGES=LANGUAGES), 500

if __name__ == '__main__':
    app.run(debug=True) 