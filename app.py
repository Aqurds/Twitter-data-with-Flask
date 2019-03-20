from flask import Flask, render_template, request
#from nocache import nocache
import ast,requests,boto3,os
from datetime import datetime
import csv
# import plots,copy,random,string
# access_key_id = 'ASIA37PBWIRNEDGEMZO2'
# secret_access_key = "+QT0v4mCGOxm7"
# session_token = '+dP/EIgDIcZgOUcuzlLHRY9glf+sqJexnhFY6I6s5Vjv6AtT66gUKo4t3PkdkTGtYr/SYI6CBvnEYPOtumiuqdCgHJZLUrYjZx0AsENG9BMgodHcFk8u/cSppfhzjYwWbGKzyBuNiWvpQrpNwVrpO+O+J3ORApG0/jnIv8ibN8oxqLa4QU='
#
app = Flask(__name__)
app.config['SECRET_KEY'] = '0f9dc56d2288afa6e10b8d97577fe25b'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#
#
# types = {"Government" : 0, "Education" : 0, "Invalid URL" : 0, "Social Media" : 0,
#   "News" : 0, "Blog" : 0, "Commercial Health" : 0, "Fake News" : 0, "Scientific" : 0,
#   "Videos" : 0, "Commercial" : 0, "HealthMagazines" : 0, "HealthInsurance" : 0,
#   "NMPSocieties" : 0, "None Found" : 0}
#
# table_dict = {"vaccine" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "abortion" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "weed" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "ecig" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types)),
#             "aids" : (copy.deepcopy(types),copy.deepcopy(types),copy.deepcopy(types))}
#
# region = 'us-east-2'
# session = boto3.session.Session()
# aws_secret = 'aXL3ndaT/'
# aws_pub = 'AKIAIFL3OJZQZDFSJOQQ'
# db = boto3.resource('dynamodb',aws_access_key_id=aws_pub,aws_secret_access_key=aws_secret)
# img_folder = '/home/trevorm4/mysite/static/img/'

# No caching at all for API endpoints.
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response
#
# """
# Uses Twitter oEmbed api to fetch the html code for embedding the tweet.
# Uses fix_twitter_html_response because the api escapes '/', even though its not necessary,which
# messes up the code
#
# @param tweet_url : url of the tweet to fetch html code for
# @return html code to embed passed tweet
# """
# def get_embed_html(tweet_url):
#   r = requests.get('https://publish.twitter.com/oembed?url='+tweet_url)
#   r = fix_malformed_dict_string(r.text)
#   return fix_twitter_html_response((ast.literal_eval(r)['html']))
#
# def fix_twitter_html_response(html):
#   new_string = ""
#   for i in range(len(html)):
#     if not (html[i] == "\\" and html[i:i+2] == '\\/'):
#       new_string += html[i]
#   return new_string
#
# """
# Some of the JSONs have false/true/null instead of False/True/None
# So this method just replaces all of false/true/null with False/True/None so ast.literal_eval can
# parse it extremely easily
# """
# def fix_malformed_dict_string(dict_string):
#   no_null = dict_string.replace('null','None')
#   no_false = no_null.replace('false','False')
#   no_true = no_false.replace('true','True')
#   return no_true
#
# def get_latest_tweets(table_name,num_tweets,topic):
#   table = db.Table(table_name)
#   response = table.scan()
#   tweets = []
#
#   for item in response['Items']:
#     if item['topic'] == topic.lower():
#         tweets.append(get_embed_html(item['TweetID']))
#   return tweets[:num_tweets]
#
# def update_counts(table_name,dictionary):
#   table = db.Table(table_name)
#
#   response = table.scan()
#
#   for item in response["Items"]:
#     category = item['topic']
#     url_type = item['type']
#     dictionary[category][0][url_type] += 1 #overall count
#     if item['user_type'] == 'Bot':
#       dictionary[category][2][url_type] += 1
#     else:
#       dictionary[category][1][url_type] += 1
#
# def update_plots(category):
#   update_counts('URLsTable',table_dict)
#   cat = category
#   plots.type_histogram_overall(table_dict[cat][0],True, category + '_PLOT_'+ generate_random_string(10) + '.png')
#   plots.type_histogram_overall(table_dict[cat][2],True, category + '_PLOT_'+ generate_random_string(10) + '_human_' +'.png')
#   plots.type_histogram_overall(table_dict[cat][2],True, category + '_PLOT_'+ generate_random_string(10) + '_bot_'+ '.png')
#
# def generate_random_string(n):
#   return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
#
# def get_plot_html(category):
#   existing_files = [file for file in os.listdir(img_folder) if file.find(category + '_PLOT_') == 0]
#
#   for file in existing_files:
#     os.remove(os.path.join(img_folder,file))
#   update_plots(category)
#
#   files = os.listdir(img_folder)
#   files = [file for file in files if file.find(category + '_PLOT_') == 0]
#   html_blocks = []
#
#   for file in files:
#     print('<img src=\"' + img_folder + file + '\" alt=\"' + file[:file.find('.png')] + '\">')
#     html_blocks.append('<img src=\"' + '/static/img/' + file + '\" alt=\"' + file[:file.find('.png')] + '\">')
#   return html_blocks


#app route

@app.route('/', methods=['POST', 'GET'])
def dash():
    data_list = []
    result_list = []
    positive = 0
    negative = 0
    neutral =0
    with open('AllTweet.csv', encoding="utf8") as f:
        rd = csv.reader(f)
        for row in rd:
            data_list.append(row)

    search_topic = ''
    if request.method == 'POST':
        search_topic = request.form['topic']

        for item in data_list:
            if item[14] == search_topic:
                result_list.append(item)
    for item in result_list:
        if item[11] == "Neutral":
            neutral += 1
        if item[11] == "Negative":
            negative += 1
        if item[11] == "Positive":
            positive += 1
    return render_template('dashboard.html', result_list=result_list, positive=positive, negative=negative, neutral=neutral)


@app.route('/analyze')
def analyze():
    return render_template('dashboard.html',tweets=get_latest_tweets('AllTweet',15,'aids'))


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/graph/')
def graph():
    return render_template('graph.html')



#
# @app.route('/vaccines')
# def vaccines():
#   #tweetss = get_latest_tweets('tweets_by_ID',15)
#   graphs = get_plot_html("vaccine")
#   return render_template('vaccines.html',charts=graphs)
#
# @app.route('/abortion')
# def abortion():
#     #tweetss = get_latest_tweets('abortion_tweets_by_ID',15)
#     graphs = get_plot_html("abortion")
#     return render_template('abortion.html',charts=graphs)
# @app.route('/marijuana')
# def weed():
#     #tweetss = get_latest_tweets('weed_tweets_by_ID',15)
#     graphs = get_plot_html('weed')
#     return render_template('weed.html', charts = graphs)
# @app.route('/aids')
# def aids():
#     #tweetss = get_latest_tweets('aids_tweets_by_ID',15)
#     graphs = get_plot_html('aids')
#     return render_template('aids.html', charts = graphs)
# @app.route('/ecigs')
# def ecigs():
#     #tweetss = get_latest_tweets('ecig_tweets_by_ID',15)
#     graphs = get_plot_html('ecig')
#     return render_template('ecigs.html', charts = graphs)


if __name__ == "__main__":
    app.run(debug=True)
