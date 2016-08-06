"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests
import json


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.0c018794-e403-4cd7-8cda-6f83a1462054"):
    	raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    print (session)

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print("intent name: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "GetDirector":
        return get_director(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Filmi. " \
                    "Please ask me about the director of your favorite movie"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please repeat your question."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_director(intent, session):
    session_attributes = {}
    reprompt_text = None

    if "Movie" in intent["slots"]:
        movie = intent["slots"]["Movie"]["value"]#session['attributes']['Movie']
        print("Movie: " + movie) 
        '''
        query movie here
        '''
        try:
        	director = get_director_for_movie(movie)
        	print ("Director: " + director)
        	speech_output = "The director of " + movie + \
                        " is " + director + "."
        	should_end_session = True
        except:
        	speech_output = "I could not fetch the director for that movie"
        	should_end_session = True
    else:
        speech_output = "I'm not sure what the movie is. " \
                        "You can say, Who directed A Few Good Men"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_director_for_movie(movie):
	#movie: https://api.themoviedb.org/3/search/movie?query=titanic&api_key=c35494259ebd7299960cebd8ebaef471
	r = requests.get(("https://api.themoviedb.org/3/search/movie?query=%s&api_key=c35494259ebd7299960cebd8ebaef471") % (movie))
	output = json.loads(r.text)
	movie_id = output["results"][0]["id"]
	
	credits_request = requests.get(("https://api.themoviedb.org/3/movie/%s/credits?api_key=c35494259ebd7299960cebd8ebaef471") % (movie_id))
	credits_output = json.loads(credits_request.text)
	for crew_member in credits_output["crew"]:
		if crew_member["job"] == "Director":
			return crew_member["name"]
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
    
if __name__=="__main__":
    print(get_director_for_movie("Good Will Hunting"))