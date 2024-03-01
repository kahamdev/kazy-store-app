'''
 this file is called app.py
 used to run our main app
'''

# this section used to import some dependencies
from flask import Flask, render_template ,jsonify,request
import requests
from api import API_PATH
from constants import watchesdisc,tvsdisc,phonesdisc

app=Flask(__name__,
          template_folder="myapp/templates",
          static_url_path="/myapp/static/style",
          static_folder='myapp/static/style',
        
          )

# this section used to call routes function
@app.route('/', methods=['GET'])
def home_view():
    search_query = request.args.get('search')
    resp = requests.get(API_PATH)
    if resp.status_code == 200:
        data = resp.json()

        smart_watches = data.get('products', {}).get('smart-watches', [])
        smart_tvs = data.get('products', {}).get('smart-tvs', [])
        smart_phones = data.get('products', {}).get('smart-phones', [])
   
        filtered_watches = []
        filtered_tvs = []
        filtered_phones = []

        if search_query:
            filtered_watches = [watch for watch in smart_watches if search_query.lower() in watch.get('name', '').lower()]
            filtered_tvs = [tv for tv in smart_tvs if search_query.lower() in tv.get('name', '').lower()]
            filtered_phones = [phone for phone in smart_phones if search_query.lower() in phone.get('name', '').lower()]
        
       

        else:
            filtered_watches = smart_watches
            filtered_tvs = smart_tvs
            filtered_phones = smart_phones
        
       

        return render_template('home.html', 
        watches=filtered_watches,
        tvs=filtered_tvs,
        phones=filtered_phones,
        watchesdisc=watchesdisc,
        tvsdisc=tvsdisc,
        phonesdisc=phonesdisc,
        search_query=search_query)
    else:
        return jsonify({'error': 'Failed to fetch data from API'})
    
  

@app.route("/gadgets")
def gadgets_info():
    resp = requests.get(API_PATH)
    if resp.status_code == 200:
       data = resp.json()
       return jsonify(data)
    
    else:
        return None

# this section used to run our app by allowing debug to true
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
