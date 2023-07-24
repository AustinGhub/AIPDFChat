import chat
import os
from flask import Flask, request, render_template,redirect, url_for, request , send_file,jsonify
from werkzeug.utils import secure_filename
from flask import Flask
from io import BytesIO
from flask_wtf.file import FileField
import random
from wtforms import SubmitField
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"]="michelle"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pdfAI.db')
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "sqlite:///pdfAI.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)


class fileUser(db.Model):
    __tablename__ = "file_user"
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(255),unique = True,nullable = False)
    content = db.Column(db.Text, nullable=False)  # Add this field to store the PDF content
    # size = db.Column(db.Integer,unique = True,nullable = False)
    def __init__(self,filename,content):
        self.filename = filename
        self.content = content
        # self.size = size


def serve_file(file_id):
    file_data = fileUser.query.get(file_id)

    if file_data:
        file_path = os.path.join("uploads", file_data.filename)
        print(file_path)
        return send_file(file_path, as_attachment=True)

    return "File not found."

@app.route("/", methods=["GET", "POST"])
def upload_file():

    # db.session.query(fileUser).delete()
    # db.session.commit()
  
    gotFile = False
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # Save the uploaded file to a secure location
            file_path = os.path.join("uploads",file.filename)
            file.save(os.path.join("uploads", file.filename))

            #read pdf
            with open(file_path,"rb") as pdf_file:
                #get stuff from pdf
                pdfContent = chat.getpdf_text(pdf_file)

            newDB = fileUser(filename=file.filename,content = pdfContent)
            db.session.add(newDB)
            db.session.commit()
            gotFile = True
    # print(fileUser.query.all())

    return render_template("upload.html")

# @app.route("/", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         files = request.files.getlist("file")  # Get multiple files as a list

#         # Combine the content of all PDFs
#         pdf_content = ""
#         for file in files:
#             file_path = os.path.join("uploads", file.filename)
#             file.save(file_path)

#             with open(file_path, "rb") as pdf_file:
#                 pdf_content += chat.getpdf_text(pdf_file)

#             # os.remove(file_path)  # Delete individual file after reading its content

#         newDB = fileUser(filename="combined.pdf", content=pdf_content)
#         db.session.add(newDB)
#         db.session.commit()
#         file.save(os.path.join("uploads", "combined.pdf"))

#     return render_template("upload.html")



 
@app.route("/search", methods=["GET","POST"])
def search():
    all_content = fileUser.query.with_entities(fileUser.content).all()
    content_list = [content[0] for content in all_content]
    texts = ""

    fileList = []
    filenames = fileUser.query.with_entities(fileUser.filename).all()
    realFiles = [file[0] for file in filenames]


    #ADD FILE PATH TO LIST AND USE SIMPLE DIRECTORY READERA
    for file in realFiles:
        # name =str(file)
        # newfile = name.strip(',()')
        file_path = os.path.join("uploads", file)
        # newname = newfile.strip("'")
        fileList.append(file_path)
    
    print(fileList)

    index = chat.pdfIndex(fileList)
    if request.method == "POST":
        prompt = request.form["prompt"]
        print(prompt)
        response = chat.generateAnswerGPT(prompt,index)
        res ={}
        res['answer'] = response
        return jsonify(res),200
    return render_template("upload.html")



if __name__=="__main__":
    with app.app_context():
        # fileUser.__table__.drop()
        # db.session.expire_all()
        # db.drop_all()
        db.create_all()
        # print(fileUser.query.all())
        app.run(debug = True)

