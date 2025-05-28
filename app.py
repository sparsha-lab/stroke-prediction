from flask import Flask,render_template,request
import pickle
app=Flask(__name__)

with open ("stroke.svc-model.pkl","rb")as file:
    stroke_model=pickle.load(file)

with open ("lb-smoking.pkl","rb")as file:
    lb_smoke=pickle.load(file)

def predict_stroke(gender="Male", age=67.0, hypertension="Yes", heart_disease="Yes", avg_glucose_level=234.46, bmi=67.34, smoking_status="smokes", Residence_type="Urban"):
    lst = []

    # Gender handling
    if gender == 'Male':
        lst = lst + [1]
    elif gender == 'Female':
        lst = lst + [0]
    elif gender == 'Other':
        lst = lst + [2]

    # Age handling
    lst = lst + [age]

    # Hypertension handling
    if hypertension == 'Yes':
        lst = lst + [1]
    elif hypertension == 'No':
        lst = lst + [0]

    # Heart disease handling
    if heart_disease == 'Yes':
        lst = lst + [1]
    elif heart_disease == 'No':
        lst = lst + [0]

    # Other features
    lst = lst + [avg_glucose_level, bmi]

    # Handle smoking status with error handling for unseen labels
    try:
        smoking_status = lb_smoke.transform([smoking_status])[0]
    except ValueError:
        # In case of an unseen label, set a default value or handle the error
        print(f"Warning: Unseen smoking status '{smoking_status}'. Using default 'never smoked'.")
        smoking_status = lb_smoke.transform(['never smoked'])[0]

    lst = lst + [smoking_status]

    # Residence type handling
    if Residence_type == 'Urban':
        lst = lst + [0, 1]
    elif Residence_type == 'Rural':
        lst = lst + [1, 0]

    print(lst)
    result = stroke_model.predict([lst])
    print(result)

    # Final prediction result
    if result == [1]:
        return "Person is having a stroke"
    else:
        return "Person is not having a stroke"


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contact",methods=["GET"])
def contact():
    name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        # Add logic to handle the form (e.g., store in DB or send email)
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        gender = request.form.get("gender")
        age = float(request.form.get("age"))
        hypertension = request.form.get("hypertension")
        heart_disease = request.form.get("heart_disease")
        avg_glucose_level = float(request.form.get("avg_glucose_level"))
        bmi = float(request.form.get("bmi"))
        smoking_status = request.form.get("smoking_status")
        Residence_type = request.form.get("residence")

        result = predict_stroke(
            gender=gender,
            age=age,
            hypertension=hypertension,
            heart_disease=heart_disease,
            avg_glucose_level=avg_glucose_level,
            bmi=bmi,
            smoking_status=smoking_status,
            Residence_type=Residence_type,
        )

        return render_template("predict.html", prediction=result)

    return render_template("predict.html")


@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)
