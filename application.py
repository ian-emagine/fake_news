### import numpy as np
import helper
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
from flask import Flask, request, Response, render_template, redirect


app = Flask(__name__)
application = app


def train_model():

    #Read the data
    items = helper.get_classified_items()
    df = pd.DataFrame(items['items'], columns =['id', 'title', 'body', 'result', 'news_category_id','created'])
    
    #Get shape and head
    df.shape
    df.head()

    

    #DataFlair - Get the labels
    results=df.result
    results.head()

    #DataFlair - Split the dataset
    x_train,x_test,y_train,y_test=train_test_split(df['body'], results, test_size=0.2, random_state=7)

    #DataFlair - Initialize a TfidfVectorizer
    tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)

    #DataFlair - Fit and transform train set, transform test set
    tfidf_train=tfidf_vectorizer.fit_transform(x_train) 

    # print(x_test)

    tfidf_test=tfidf_vectorizer.transform(x_test)

    # print(tfidf_test.shape)

    #DataFlair - Initialize a PassiveAggressiveClassifier
    pac=PassiveAggressiveClassifier(max_iter=50)
    pac.fit(tfidf_train,y_train)

    #DataFlair - Predict on the test set and calculate accuracy
    # y_pred=loaded_model.predict(tfidf_test)
    # print(y_pred)
    #score=accuracy_score(y_test,y_pred)
    #print(f'Accuracy: {round(score*100,2)}%')

    #DataFlair - Build confusion matrix
    #confusion_matrix(y_test,y_pred, labels=['FAKE','REAL'])


    model_filename = 'fake_news_model.sav'
    joblib.dump(pac, open(model_filename, 'wb'))

    vectorizer_filename = 'fake_news_vectorizer.sav'
    joblib.dump(tfidf_vectorizer, open(vectorizer_filename, 'wb'))

    return

def predict_data(test_data_frame):
    model_filename = 'fake_news_model.sav'
    loaded_model = joblib.load(model_filename)

    vectorizer_filename = 'fake_news_vectorizer.sav'
    loaded_vectorizer = joblib.load(vectorizer_filename)

    vec_newtest=loaded_vectorizer.transform(test_data_frame['body'])
    t_pred=loaded_model.predict(vec_newtest)
    t_pred.shape
    # print(t_pred)
    return t_pred


def get_single_item():
    res_data1 = helper.get_unclassified_item()
    # print(res_data1['items'])
    return pd.DataFrame(res_data1['items'], columns =['id', 'title', 'body', 'result', 'news_category_id','created'])

# predict_data(get_single_item())

def test_add_item():
    # Get item from the POST body
    # req_data = request.get_json()
    test_body = """
    Daniel Greenfield, a Shillman Journalism Fellow at the Freedom Center, is a New York writer focusing on radical Islam. 
    In the final stretch of the election, Hillary Rodham Clinton has gone to war with the FBI. 
    The word “unprecedented” has been thrown around so often this election that it ought to be retired. But it’s still unprecedented for the nominee of a major political party to go war with the FBI. 
    But that’s exactly what Hillary and her people have done. Coma patients just waking up now and watching an hour of CNN from their hospital beds would assume that FBI Director James Comey is Hillary’s opponent in this election. 
    The FBI is under attack by everyone from Obama to CNN. Hillary’s people have circulated a letter attacking Comey. There are currently more media hit pieces lambasting him than targeting Trump. It wouldn’t be too surprising if the Clintons or their allies were to start running attack ads against the FBI. 
    The FBI’s leadership is being warned that the entire left-wing establishment will form a lynch mob if they continue going after Hillary. And the FBI’s credibility is being attacked by the media and the Democrats to preemptively head off the results of the investigation of the Clinton Foundation and Hillary Clinton. 
    The covert struggle between FBI agents and Obama’s DOJ people has gone explosively public. 
    The New York Times has compared Comey to J. Edgar Hoover. Its bizarre headline, “James Comey Role Recalls Hoover’s FBI, Fairly or Not” practically admits up front that it’s spouting nonsense. The Boston Globe has published a column calling for Comey’s resignation. Not to be outdone, Time has an editorial claiming that the scandal is really an attack on all women. 
    James Carville appeared on MSNBC to remind everyone that he was still alive and insane. He accused Comey of coordinating with House Republicans and the KGB. And you thought the “vast right wing conspiracy” was a stretch. 
    Countless media stories charge Comey with violating procedure. Do you know what’s a procedural violation? Emailing classified information stored on your bathroom server. 
    Senator Harry Reid has sent Comey a letter accusing him of violating the Hatch Act. The Hatch Act is a nice idea that has as much relevance in the age of Obama as the Tenth Amendment. But the cable news spectrum quickly filled with media hacks glancing at the Wikipedia article on the Hatch Act under the table while accusing the FBI director of one of the most awkward conspiracies against Hillary ever. 
    If James Comey is really out to hurt Hillary, he picked one hell of a strange way to do it. 
    Not too long ago Democrats were breathing a sigh of relief when he gave Hillary Clinton a pass in a prominent public statement. If he really were out to elect Trump by keeping the email scandal going, why did he trash the investigation? Was he on the payroll of House Republicans and the KGB back then and playing it coy or was it a sudden development where Vladimir Putin and Paul Ryan talked him into taking a look at Anthony Weiner’s computer? 
    Either Comey is the most cunning FBI director that ever lived or he’s just awkwardly trying to navigate a political mess that has trapped him between a DOJ leadership whose political futures are tied to Hillary’s victory and his own bureau whose apolitical agents just want to be allowed to do their jobs. 
    The only truly mysterious thing is why Hillary and her associates decided to go to war with a respected Federal agency. Most Americans like the FBI while Hillary Clinton enjoys a 60% unfavorable rating. 
    And it’s an interesting question. 
    Hillary’s old strategy was to lie and deny that the FBI even had a criminal investigation underway. Instead her associates insisted that it was a security review. The FBI corrected her and she shrugged it off. But the old breezy denial approach has given way to a savage assault on the FBI. 
    Pretending that nothing was wrong was a bad strategy, but it was a better one that picking a fight with the FBI while lunatic Clinton associates try to claim that the FBI is really the KGB. 
    There are two possible explanations. 
    Hillary Clinton might be arrogant enough to lash out at the FBI now that she believes that victory is near. The same kind of hubris that led her to plan her victory fireworks display could lead her to declare a war on the FBI for irritating her during the final miles of her campaign. 
    But the other explanation is that her people panicked. 
    Going to war with the FBI is not the behavior of a smart and focused presidential campaign. It’s an act of desperation. When a presidential candidate decides that her only option is to try and destroy the credibility of the FBI, that’s not hubris, it’s fear of what the FBI might be about to reveal about her. 
    During the original FBI investigation, Hillary Clinton was confident that she could ride it out. And she had good reason for believing that. But that Hillary Clinton is gone. In her place is a paranoid wreck. Within a short space of time the “positive” Clinton campaign promising to unite the country has been replaced by a desperate and flailing operation that has focused all its energy on fighting the FBI. 
    There’s only one reason for such bizarre behavior. 
    The Clinton campaign has decided that an FBI investigation of the latest batch of emails poses a threat to its survival. And so it’s gone all in on fighting the FBI. It’s an unprecedented step born of fear. It’s hard to know whether that fear is justified. But the existence of that fear already tells us a whole lot. 
    Clinton loyalists rigged the old investigation. They knew the outcome ahead of time as well as they knew the debate questions. Now suddenly they are no longer in control. And they are afraid. 
    You can smell the fear. 
    The FBI has wiretaps from the investigation of the Clinton Foundation. It’s finding new emails all the time. And Clintonworld panicked. The spinmeisters of Clintonworld have claimed that the email scandal is just so much smoke without fire. All that’s here is the appearance of impropriety without any of the substance. But this isn’t how you react to smoke. It’s how you respond to a fire. 
    The misguided assault on the FBI tells us that Hillary Clinton and her allies are afraid of a revelation bigger than the fundamental illegality of her email setup. The email setup was a preemptive cover up. The Clinton campaign has panicked badly out of the belief, right or wrong, that whatever crime the illegal setup was meant to cover up is at risk of being exposed. 
    The Clintons have weathered countless scandals over the years. Whatever they are protecting this time around is bigger than the usual corruption, bribery, sexual assaults and abuses of power that have followed them around throughout the years. This is bigger and more damaging than any of the allegations that have already come out. And they don’t want FBI investigators anywhere near it. 
    The campaign against Comey is pure intimidation. It’s also a warning. Any senior FBI people who value their careers are being warned to stay away. The Democrats are closing ranks around their nominee against the FBI. It’s an ugly and unprecedented scene. It may also be their last stand. 
    Hillary Clinton has awkwardly wound her way through numerous scandals in just this election cycle. But she’s never shown fear or desperation before. Now that has changed. Whatever she is afraid of, it lies buried in her emails with Huma Abedin. And it can bring her down like nothing else has.  

    """
    req_data = {"title": "You Can Smell Hillary’s Fear", "body": test_body, "news_category_id": "1"}
    # req_data = [[999999,"You Can Smell Hillary’s Fear", test_body, "UNDETERMINED","1","2021-09-11 12:12:00"]]
    
    if  'result' not in req_data or req_data['result'] not in ('REAL', 'FAKE'):
        # modified_req_data = req_data.to_dict()
        modified_req_data = req_data
        modified_req_data['result'] = 'UNDETERMINED'
    else:
        modified_req_data = req_data
    # print(modified_req_data)
    # Add item to the list
    res_data = helper.add_to_list(modified_req_data)

    # Return error if item not added
    if res_data is None:
        return render_template('add.html', the_title = "Could not save article. Please try again.", title = modified_req_data['title'], body = modified_req_data['body'])
        # response = Response("{'error': 'Item not added - " + req_data['title'] + "'}", status=400 , mimetype='application/json')
        # return response
    
    # Transform to Dataframe
    test_data_frame = pd.DataFrame(res_data, columns =['id', 'title', 'body', 'result', 'news_category_id','created'])
    # print(test_data_frame.head())
    result = predict_data(test_data_frame)
    # result = test_data_frame
    print(result)

# test_add_item()


@app.route('/')
def add_form():
    return render_template('add.html', the_title="Check if a news article is real of fake")

@app.route('/analyze', methods=['POST'])
def add_item():
    # Get item from the POST body
    # req_data = request.get_json()
    req_data = request.form
    
    if  'result' not in req_data or req_data['result'] not in ('REAL', 'FAKE'):
        modified_req_data = req_data.to_dict()
        modified_req_data['result'] = 'UNDETERMINED'
    else:
        modified_req_data = req_data

    # Add item to the list
    res_data = helper.add_to_list(modified_req_data)

    # Return error if item not added
    if res_data is None:
        return render_template('add.html', the_title = "Could not save article. Please try again.", title = modified_req_data['title'], body = modified_req_data['body'])
    
    # Transform to Dataframe
    test_data_frame = pd.DataFrame(res_data, columns =['id', 'title', 'body', 'result', 'news_category_id','created'])
    # print(test_data_frame.head())
    result = predict_data(test_data_frame)
    
    return render_template('result.html', the_title = "Result of your article", result = result, title = modified_req_data['title'])