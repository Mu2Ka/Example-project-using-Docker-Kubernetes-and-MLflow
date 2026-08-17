from flask import Flask, request, jsonify
import joblib
import numpy as np
app = Flask(__name__)
model = joblib.load('iris_model.joblib') #later need to load from mlflow

@app.route('/',methods=['GET'])
def health_check():
        return jsonify({'status': 'ok'})
@app.route('/predict',methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}),400
        features = np.array([data.get('sepal_length',0),
                              data.get('sepal_width',0),
                              data.get('petal_length',0),
                              data.get('petal_width',0)
                              ]).reshape(1,-1)
        prediction = model.predict(features)
        probability = model.predict_proba(features)

        classes=['setosa','versicolor','virgin']
        predicted_classs = classes[prediction[0]]
        return jsonify({
            'prediction': predicted_classs,
            'class_id': int(prediction[0]),
            'probabilities': {
                classes[i]: float(probability[0][i])
                for i in range(len(classes))
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)