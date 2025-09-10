# Diabetes Prediction Project

## Overview
This project aims to predict diabetes diagnosis using health indicators from the BRFSS 2015 dataset. The workflow includes data loading, preprocessing, model training, and evaluation.

## Dataset
The dataset used is `diabetes_binary_health_indicators_BRFSS2015.csv`, which contains various health-related features and a binary target column `Diabetes_binary` indicating diabetes diagnosis.

## Workflow
1. **Data Loading & Exploration**
	- Load the dataset using pandas.
	- Explore data shape, head, info, and check for null values.
	- Analyze unique values and class distribution in the target column.

2. **Feature Preparation**
	- Separate input features (`X`) and target (`Y`).
	- Split data into training and test sets (80/20 split).

3. **Data Preprocessing**
	- Standardize features using `StandardScaler` for better model performance.

4. **Model Training**
	- **Logistic Regression**: Train and predict using logistic regression.
	- **Random Forest Classifier**: Train and predict using a random forest classifier with 120 estimators.

5. **Evaluation Metrics**
	- Evaluate models using metrics such as accuracy, precision, recall, F1-score, ROC-AUC, log loss, and confusion matrix.
	- Generate classification reports for detailed performance analysis.

## Technologies Used
- Python
- pandas, numpy
- scikit-learn

## How to Run
Open the `diabetes_prediction.ipynb` notebook and run the cells sequentially. Ensure the dataset is available at the specified path.

## Results
The notebook provides predictions and performance metrics for both logistic regression and random forest models, allowing comparison and selection of the best model for diabetes prediction.

---
*For more details, see the code and outputs in `diabetes_prediction.ipynb`.*