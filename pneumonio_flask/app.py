import base64
import time
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        file = request.files['image']
        image_data = base64.b64encode(file.read()).decode('utf-8')
        
        headers = {
            'Authorization' : 'rpa_H8ZXGGKERTJARPZGKZ8LFG9TMT3SSRI09SWVULG51e9m3s'
            
        }
        
        res = requests.post('https://api.runpod.ai/v2/v1j88xdmb8tquv/run',
                            json = {'input':{'image': image_data}},
                            headers = headers
                            )
        res_id = res.json()['id']
        prediction = None
        for _ in range(50):
            status_res = requests.post(f'https://api.runpod.ai/v2/v1j88xdmb8tquv/status/{res_id}', headers=headers)
            status = status_res.json()
            print(f'aqui llegamos {status}')
            
            if status.get('status','').lower() == 'completed':
                prediction = status['output']['prediction']
                print('aqui llegamos')
                break
            time.sleep(4)
            
        if prediction is None:
            prediction = "Error: No se obtuvo una predicción."
            
        return render_template('index.html', original_image = f'data:image/jpeg;base64, {image_data}', 
                               prediction = prediction)
        
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)