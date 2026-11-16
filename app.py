
import os
import joblib
import xgboost as xgb
import pandas as pd
import numpy as np

from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------------
# MODEL DIRECTORY
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# -----------------------------------
# LOAD SAVED PREPROCESSING OBJECTS
# -----------------------------------

print("Loading preprocessing files...")

preprocessor = joblib.load(
    os.path.join(MODEL_DIR, "preprocessor.pkl")
)

label_encoder = joblib.load(
    os.path.join(MODEL_DIR, "label_encoder.pkl")
)

# -----------------------------------
# LOAD XGBOOST MODELS FROM JSON
# -----------------------------------

print("Loading Binary Model...")

model1 = xgb.XGBClassifier()
model1.load_model(
    os.path.join(MODEL_DIR, "xgboost_tuned_model.json")
)

print("Binary Model loaded successfully!")

print("Loading Multiclass Model...")

model2 = xgb.XGBClassifier()
model2.load_model(
    os.path.join(MODEL_DIR, "xgboost_multiclass_tuned_model.json")
)

print("Multiclass Model loaded successfully!")

# -----------------------------------
# FEATURE INFORMATION
# -----------------------------------

selected_features = preprocessor["selected_features"]
numerical_features = preprocessor["numerical_features"]
categorical_features = preprocessor["categorical_features"]

encoder = preprocessor["encoder"]
scaler = preprocessor["scaler"]

print("\nAll model files loaded successfully!")
print("Total selected features:", len(selected_features))


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/dataset")
def dataset():

    return render_template(
        "dataset.html",
        feature_count=len(selected_features),
        numerical_count=len(numerical_features),
        categorical_count=len(categorical_features),
        attack_labels=label_encoder.classes_
    )


# -----------------------------------
# PREDICTION
# -----------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        input_data = {}

        # Collect all 17 input features
        for feature in selected_features:

            value = request.form.get(feature)

            if value is None or value.strip() == "":
                return "Missing input: " + feature, 400

            if feature in numerical_features:
                input_data[feature] = float(value)
            else:
                input_data[feature] = value

        # Create DataFrame in original training order
        input_df = pd.DataFrame(
            [input_data],
            columns=selected_features
        )

        # Apply numerical preprocessing
        numerical_data = scaler.transform(
            input_df[numerical_features]
        )

        # Apply categorical preprocessing
        categorical_data = encoder.transform(
            input_df[categorical_features]
        ).toarray()

        # Combine features in training order
        processed_data = np.hstack([
            numerical_data,
            categorical_data
        ])

        # -----------------------------------
        # MODEL 1: BINARY CLASSIFICATION
        # -----------------------------------

        binary_prediction = int(
            model1.predict(processed_data)[0]
        )

        if binary_prediction == 0:

            result = "Normal Traffic"
            attack_category = "No Attack"

        else:

            result = "Attack Detected"

            # -----------------------------------
            # MODEL 2: MULTICLASS CLASSIFICATION
            # -----------------------------------

            multiclass_prediction = model2.predict(
                processed_data
            ).astype(int)

            attack_category = label_encoder.inverse_transform(
                multiclass_prediction
            )[0]

        # -----------------------------------
        # DISPLAY RESULT
        # -----------------------------------

        return render_template(
            "result.html",
            result=result,
            attack_category=attack_category
        )

    except ValueError as e:

        return f"Invalid input: {str(e)}", 400

    except Exception as e:

        app.logger.exception("Prediction error")

        return f"Prediction failed: {str(e)}", 500


# -----------------------------------
# RUN FLASK APPLICATION
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True, port=int(os.environ.get("PORT", "5000")))
