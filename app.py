from flask import Flask, render_template, request, redirect, url_for
from prediction import tomatoLeafDiseasePrediction
import pandas as pd


app = Flask(__name__)
app.secret_key = "leaves"


@app.route('/home')
def home():
    return render_template("prediction.html")


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img = request.files['file_']
        img_path = "static/user_upload/ui" + img.filename
        img.save(img_path)
        result = tomatoLeafDiseasePrediction(img_path)
        prediction = result[0]
        p_score = result[1]
        pred_data = result[2]
        # print("pred_data : ", pred_data)

        # print("p_score : ", p_score)
        formatted_score = "{:.2f}%".format(p_score * 100)
        # print(formatted_score)

        if prediction == "Health":
            sug_title = "Protect Healthy tomato leaves from disease and minimize the need for Pesticides"
        else: 
            sug_title = "About Disease and Pesticides List"

        return render_template("prediction.html", prediction=prediction, img_path=img_path, p_score=formatted_score, s_t=sug_title, p_d=pred_data)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pwd"]

        users_df = pd.read_excel('user.xlsx')

        for index, row in users_df.iterrows():
            if row["email"] == email and row["password"] == pwd:

                return redirect(url_for('home'))

        error_message = 'Invalid email or password. Please try again.'
        return render_template('login.html', msg=error_message)

    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            email = request.form['email']
            pwd = request.form['pwd']
            repwd = request.form['repwd']
            if pwd == repwd:  # Fix the comparison operator
                col_list = ["email", "password"]
                try:
                    # Try reading the existing file, if it exists
                    r1 = pd.read_excel('user.xlsx', usecols=col_list)
                except FileNotFoundError:
                    # If the file doesn't exist, create an empty DataFrame
                    r1 = pd.DataFrame(columns=col_list)

                new_row = {'email': email, 'password': pwd}
                r1 = r1.append(new_row, ignore_index=True)
                r1.to_excel('user.xlsx', index=False)
                print("Records created successfully")
                msg = 'Registration Successful. You can log in here.'
                return render_template('login.html', msg=msg)
            else:
                msg = 'Password and Re-enter password do not match.'
                return render_template('register.html', msg=msg)
        return render_template('register.html')
    except:
        return render_template('register.html', msg="Please Enter valid mail pattern like xyz@gmail.com")


@app.route('/password', methods=['POST', 'GET'])
def password():
    try:
        if request.method == 'POST':
            current_pass = request.form['current']
            new_pass = request.form['new']
            verify_pass = request.form['varify']
            r1 = pd.read_excel('user.xlsx')
            for index, row in r1.iterrows():
                if row["password"] == str(current_pass):
                    if new_pass == verify_pass:
                        r1.loc[index, "password"] = verify_pass
                        r1.to_excel("user.xlsx", index=False)
                        msg1 = 'Password changed successfully'
                        return render_template('password.html', msg=msg1)
                    else:
                        msg = 'Re-entered password is not matched'
                        return render_template('password.html', msg=msg)
            else:
                msg3 = 'Incorrect Password'
                return render_template('password.html', msg=msg3)
        return render_template('password.html')
    except Exception as e:
        return render_template('password.html', msg=e)
    

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    try:
        if request.method == 'POST':
            graph_name = request.form['text']
            graph = ''
            name = ''
            if graph_name == "c_ac":
                model_name = "Convolutional Neural Network"
                name = "Accuracy Plot Graph "
                graph = "static/graphs/c_ac.png"
            elif graph_name == 'c_ls':
                model_name = "Convolutional Neural Network"
                name = "Loss Plor Graph"
                graph = "static/graphs/c_ls.png"
            elif graph_name == 'c_cr':
                model_name = "Convolutional Neural Network"
                name = "Classification Report"
                graph = "static/graphs/c_cr.png"
            elif graph_name == 'c_cm':
                model_name = "Convolutional Neural Network"
                name = "Confusion Matrix"
                graph = "static/graphs/c_cm.png"
            elif graph_name == "d_ac":            
                model_name = "DenseNet 201"
                name = "Accuracy Plot Graph "
                graph = "static/graphs/d_ac.png"
            elif graph_name == 'd_ls':
                model_name = "DenseNet 201"
                name = "Loss Plor Graph"
                graph = "static/graphs/d_ls.png"
            elif graph_name == 'd_cr':
                model_name = "DenseNet 201"
                name = "Classification Report"
                graph = "static/graphs/d_cr.png"
            elif graph_name == 'd_cm':
                model_name = "DenseNet 201"
                name = "Confusion Matrix"
                graph = "static/graphs/d_cm.png"

            return render_template('graphs.html', mn=model_name, name=name, graph=graph)
    except Exception as e:
         msg = "Select the Graph."
         return render_template('graphs.html', msg=msg)
    
@app.route('/graphs', methods=['POST', 'GET'])
def graphs():
    return render_template('graphs.html')


@app.route('/logout')
def logout():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(port=2890, debug=True)
