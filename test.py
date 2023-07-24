# import chat
# import os
# from flask import Flask, request, render_template,redirect, url_for, request , send_file
# from werkzeug.utils import secure_filename
# from flask import Flask
# from io import BytesIO
# from flask_wtf.file import FileField
# from wtforms import SubmitField
# from flask_wtf import Form
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config["SECRET_KEY"]="michelle"
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'pdfAI.db')
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "sqlite:///pdfAI.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class fileUser(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     filename = db.Column(db.String(255),unique = True,nullable = False)

#     def __init__(self,filename):
#          self.filename = filename

#     def __repr__(self):
#             return f'<filename {self.filename}>'
# # db.create_all()

# def serve_file(file_id):
#     file_data = fileUser.query.get(file_id)

#     if file_data:
#         file_path = os.path.join("uploads", file_data.filename)
#         return send_file(file_path, as_attachment=True)

#     return "File not found."

# @app.route("/", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             # Save the uploaded file to a secure location
#             file.save(os.path.join("uploads", file.filename))
#             newDB = fileUser(filename=file.filename)
#             db.session.add(newDB)
#             db.session.commit()
#             # return "File uploaded successfully!"
#             print(fileUser.query.all())
#         return render_template("success.html")
#     return render_template("upload.html")



# @app.route("/gpt4", methods=["GET", "POST"])
# def gpt4():
#     for files in fileUser.query.all():
#         print(files)
#     # serve_file(files)
#     return "d"

# @app.route("/delete", methods=["GET"])
# def deleteDB():
#     try:
#         db.session.query(fileUser).delete()
#         db.session.commit()
#         print(fileUser.query.all())
#         return "Success deleting" 
#     except Exception as e:
#         db.session.rollback()

# # def database():
# #     connection = sqlite3.connect("pdfChatbot.db")


# if __name__=="__main__":
#     with app.app_context():
#         db.create_all()
#         app.run(debug = True)