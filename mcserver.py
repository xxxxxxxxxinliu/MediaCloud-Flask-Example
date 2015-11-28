import ConfigParser, logging, datetime, os, collections

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)
now = datetime.datetime.now()

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startday = request.form['startday']
    endday = request.form['endday']

    startday_y,startday_m,startday_d = startday.split("-")
    endday_y,endday_m,endday_d = endday.split("-")
    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( datetime.date( int(startday_y), int(startday_m), int(startday_d)), 
                                            datetime.date( int(endday_y), int(endday_m), int(endday_d)) ),
                     'media_sets_id:1' ], split = True, split_start_date = startday, split_end_date = endday)
    count = results['count']
    data = results['split']
    data_sorted = collections.OrderedDict(sorted(data.items()))
    dates = [key[:10] for key in data_sorted.keys()[:-3]]
    values = data_sorted.values()[:-3]

    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['count'], startday=startday, endday=endday, dates = dates, values= values)

if __name__ == "__main__":
    app.debug = True
    app.run()

logging.info("hello")