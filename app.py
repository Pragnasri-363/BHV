from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request
from flask_migrate import Migrate
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:PASSWORD@localhost:5432/bhv_db'
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class Entries(db.Model):
    __tablename__="entries"
    id=db.Column(db.Integer,primary_key=True)
    #This serves as index to retrieve the required data
    patient_name=db.Column(db.String(100), nullable=False, index=True)

    image_name = db.Column(db.String(255), nullable=False)
    narrative = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template('index.html') 



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get form data
        patient_name = request.form.get('patient_name')
        narrative = request.form.get('narrative')
        file = request.files.get('patient_image')

        if file and patient_name:
            # Secure the file name
            filename = secure_filename(file.filename)
            
            UPLOAD_FOLDER = os.path.join('static', 'uploads')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            new_entry = Entries(
                patient_name=patient_name,
                image_name=filename,
                narrative=narrative
            )
            db.session.add(new_entry)
            db.session.commit()

            return "Upload successful! File saved and entry recorded in the database."

        else:
            return "Please provide a name and select a file."

    return render_template('upload.html')


@app.route('/gallery/<search_term>')
def gallery(search_term):
    user_entries = Entries.query.filter_by(patient_name=search_term).all()
    
    return render_template('gallery.html', entries=user_entries, patient=search_term)
    

if __name__ == '__main__':
    app.run(debug=True)