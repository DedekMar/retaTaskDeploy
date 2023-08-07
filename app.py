from flask import Flask, render_template
from data_processor import DataProcessor
import argparse
from waitress import serve
import logging
from loader import download_and_extract_zip

# simple flask app that uses the DataProcessor class to route the requsts and pass results to the templates

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/item_count')
def show_item_count():
    try:
        item_count = data_processor.count_all_items()
        return render_template('item_count.html', item_count = item_count)
    except Exception as e:
        return render_template("error.html")


@app.route('/item_list')
def show_item_list():
    try:
        items = data_processor.get_all_item_names()
        return render_template('item_list.html', items = items)
    except Exception as e:
        return render_template("error.html")

@app.route('/item_spares')
def show_item_spares():
    try:    
        items_with_spares = data_processor.get_items_with_category_parts(1)
        return render_template('item_spares.html', items_with_spares = items_with_spares)
    except Exception as e:
        return render_template("error.html")

if __name__ == '__main__':
    # Add command-line argument for  target directory
    parser = argparse.ArgumentParser(description="Specify the path of the xml file and launch the web Flask app")
    parser.add_argument("-fp", default = "./xml_data/export_full.xml", help="Path to the xml file")  
    args = parser.parse_args()  
    file_path = args.fp
    url = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"
    download_and_extract_zip(url, file_path)

    data_processor = DataProcessor(file_path= file_path)
    serve(app, host='0.0.0.0', port=5000)
    #app.run(host="0.0.0.0")