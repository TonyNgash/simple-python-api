from flask import Flask, jsonify, render_template, redirect,request
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
application = app
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/img')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload")
def upload():
    if request.args.get("msg") != "":
        msg = request.args.get("msg")
        return render_template("upload.html",msg = msg)
    else:
        return render_template("upload.html",msg = "")


connect = pymysql.connect(host="127.0.0.1",user="your-username",password="your-pass",database="your-db")
@app.route("/receive-product",methods=['GET','POST'])
def receive():
    cur = connect.cursor()
    sql = "INSERT INTO products(product_name,product_price,product_description,image_filename)VALUES(%s,%s,%s,%s)"
    if request.method == "POST":
        prodName = request.form['product_name']
        prodPrice = request.form['product_price']
        prodDescription = request.form['product_description']
        prodImage = request.files['product_image']
        myFilename = secure_filename(prodImage.filename)#
        cur.execute(sql,(prodName, prodPrice, prodDescription, request.base_url+"/../static/img/"+myFilename))
        connect.commit()
        prodImage.save(os.path.join(app.config['UPLOAD_FOLDER'],myFilename))
        msg = "Products Added Successfully"
        return  redirect(f"/your-application-url/upload?msg={msg}")
    else:
        msg = "Error! Method was not POST."
        return redirect(f"/your-application-url/upload?msg={msg}")


@app.route("/show-products")
def products():
    cur = connect.cursor()
    sql = "SELECT * FROM products"
    cur.execute(sql)
    if cur.rowcount > 0:
        data = cur.fetchall()
        response = jsonify(data)
        response.status_code = 200
        return response
    else:
        data = {'msg':"No data found"}
        response = jsonify(data)
        response.status_code = 200
        return response

    



#tle last block of code
if __name__ == "__main__":
    app.run(debug=True)
#don't add code beyond this point

