from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Complaint {self.id} - {self.title}>'

@app.route('/')
def index():
    complaints = Complaint.query.all()
    return render_template('index.html', complaints=complaints)

@app.route('/add', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']

        new_complaint = Complaint(title=title, description=description, status=status)
        db.session.add(new_complaint)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    if request.method == 'POST':
        complaint.title = request.form['title']
        complaint.description = request.form['description']
        complaint.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', complaint=complaint)

@app.route('/delete/<int:id>')
def delete_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    return redirect(url_for('index'))

with app.app_context(): 
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
