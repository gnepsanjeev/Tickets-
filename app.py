from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'  # Replace with a secure key

# Mock database for simplicity
users = {"admin": "password"}  # Replace with a real database
tickets = []

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', tickets=tickets)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/create-ticket', methods=['POST'])
def create_ticket():
    if 'user' in session:
        issue = request.form['issue']
        tickets.append({'id': len(tickets) + 1, 'issue': issue, 'status': 'Open'})
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
