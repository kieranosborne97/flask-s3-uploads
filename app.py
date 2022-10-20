from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from database.db import create_db, create_user, get_all_users, set_user_profile_picture_file_names
from uploads.file_handler import is_file_type_allowed, upload_file_to_s3

app = Flask(__name__)
app.secret_key = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
create_db()


@app.route("/", methods=['GET'])
def home():    
    users = get_all_users()
    return render_template('home.html', users=users)


@app.route("/sign-up-new-user", methods=['POST'])
def sign_up_new_user():
    name = request.form['name']
    create_user(name)
    return redirect(url_for('home'))


@app.route("/upload-image/<user_id>", methods=['POST'])
def upload_image(user_id):
    if 'file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('home'))
    
    file_to_upload = request.files['file']

    if file_to_upload.filename == '':
        flash('No file uploaded', 'danger')
        return redirect(url_for('home'))
    
    if file_to_upload and is_file_type_allowed(file_to_upload.filename):
        provided_file_name = secure_filename(file_to_upload.filename)
        stored_file_name = upload_file_to_s3(file_to_upload, provided_file_name)
        set_user_profile_picture_file_names(user_id, stored_file_name, provided_file_name)
        flash(f'{provided_file_name} was successfully uploaded', 'success')
    
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)