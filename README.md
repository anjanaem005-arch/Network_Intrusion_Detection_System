# Network Intrusion Detection System (NIDS)

A machine-learning-based Network Intrusion Detection System built with
**Python, Flask and XGBoost**, using the **UNSW-NB15** dataset.

The application accepts network-traffic feature values, predicts whether
the traffic is **Normal** or an **Attack**, and, if an attack is
detected, predicts its attack category.

## Project Overview

The system uses a two-stage classification approach:

1.  **Binary classification:** Identifies traffic as Normal or Attack.
2.  **Multiclass classification:** If an attack is detected, predicts
    its category.

The nine attack categories are Analysis, Backdoor, DoS, Exploits,
Fuzzers, Generic, Reconnaissance, Shellcode and Worms.

## Dataset

-   **Dataset:** UNSW-NB15
-   **Training file:** `UNSW_NB15_training-set.csv` (an Excel version
    was also used during development).
-   **Original training-set size:** 175,341 records and 45 columns.
-   The `id` column was removed before modelling.
-   `label` was used for binary classification and `attack_cat` for
    multiclass classification.

## Selected Features

XGBoost feature importance was used to select 17 features.

### Numerical features (14)

`sttl`, `ct_srv_dst`, `sbytes`, `ct_dst_sport_ltm`, `smean`, `sloss`,
`dpkts`, `ct_dst_src_ltm`, `dmean`, `swin`, `synack`, `ct_srv_src`,
`dbytes`, `ct_state_ttl`.

### Categorical features (3)

`proto`, `service`, `state`.

## Preprocessing

-   **MinMaxScaler** is applied to numerical features.
-   **OneHotEncoder** is applied to categorical features.
-   The transformed numerical and categorical features are combined
    before prediction.
-   The fitted preprocessing objects are stored in `preprocessor.pkl`.
-   The multiclass category encoder is stored in `label_encoder.pkl`.

## Models

  ---------------------------------------------------------------------------------------
  Model                   Purpose                 File
  ----------------------- ----------------------- ---------------------------------------
  Binary XGBoost          Normal vs Attack        `xgboost_tuned_model.json`
  classifier                                      

  Multiclass XGBoost      Predict attack category `xgboost_multiclass_tuned_model.json`
  classifier                                      
  ---------------------------------------------------------------------------------------

The XGBoost models are saved in native JSON format. Preprocessing
objects are loaded using Joblib.

## Model Evaluation

### Binary classification

  Metric        Result
  ----------- --------
  Accuracy      95.12%
  Precision     98.01%
  Recall        94.76%
  F1-score      96.36%
  ROC-AUC       99.37%

### Multiclass classification

  Metric                   Result
  ---------------------- --------
  Accuracy                 75.55%
  Precision (weighted)     85.76%
  Recall (weighted)        75.55%
  F1-score (weighted)      78.80%
  F1-score (macro)         57.77%

The difference between weighted F1 and macro F1 indicates variation in
performance across classes. Macro F1 gives each class equal importance
and can reveal weaker performance on underrepresented attack categories.

## Technology Stack

-   Python
-   XGBoost and scikit-learn
-   Pandas and NumPy
-   Joblib
-   Flask
-   HTML and CSS

## Project Structure

``` text
Network_Intrusion_Detection/
├── app.py
├── requirements.txt
├── models/
│   ├── preprocessor.pkl
│   ├── label_encoder.pkl
│   ├── xgboost_tuned_model.json
│   └── xgboost_multiclass_tuned_model.json
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── css/
│       └── style.css
└── .venv/
```

The `.venv` folder is created locally and should generally not be
committed to Git.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd Network_Intrusion_Detection
```

Or open your existing project folder in VS Code.

### 2. Create a virtual environment

On Windows:

``` bash
py -3.13 -m venv .venv
```

### 3. Activate the environment

Command Prompt:

``` cmd
.venv\Scripts\activate
```

PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The project was developed with Python 3.13.7, XGBoost 3.4.1 and
scikit-learn 1.6.1. Use compatible package versions if your environment
differs.

### 5. Check model files

Ensure these files are inside the `models/` folder:

-   `preprocessor.pkl`
-   `label_encoder.pkl`
-   `xgboost_tuned_model.json`
-   `xgboost_multiclass_tuned_model.json`

### 6. Run the application

``` bash
python app.py
```

Open the local URL printed by Flask. By default:

``` text
http://127.0.0.1:5000/
```

## How to Use

1.  Open the application in a browser.
2.  Enter values for the 17 selected network-traffic features.
3.  Submit the form.
4.  The binary model predicts Normal or Attack.
5.  If an attack is detected, the multiclass model predicts its
    category.
6.  View the result on the results page.

Use feature values and categorical options compatible with the training
data. Unknown categorical values may be ignored by the encoder and can
reduce prediction reliability.

## Current Scope and Limitations

-   The application predicts from user-provided feature values.
-   **Live packet capture and continuous real-time network monitoring
    are not implemented.**
-   Live detection would require packet capture, network-flow
    construction and extraction of the same 17 features in a manner
    consistent with the UNSW-NB15 feature definitions.
-   The reported metrics come from evaluation on the dataset; real-world
    network performance has not been established.
-   Class imbalance affects performance across attack categories, as
    reflected by the macro F1-score.

## Future Enhancements

-   Live packet capture and network-flow generation.
-   Compatible feature extraction from live traffic.
-   Real-time attack alerts and warning indicators.
-   Alert history and traffic visualizations.
-   Improved detection of minority attack categories.
-   Validation using additional real-world network traffic.

## Disclaimer

This is an academic machine-learning prototype. Its predictions are not
a replacement for production-grade network security monitoring or
professional security controls.
