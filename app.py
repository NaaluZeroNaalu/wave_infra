import streamlit as st
import requests
import json


#credentials

api_key = "3Vj-0udUsnRjiJwBKNGAEcHNpiS-xi6VX-5tU2VZWHij"
url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
project_id = "4152f31e-6a49-40aa-9b62-0ecf629aae42"
model_id = "meta-llama/llama-3-2-90b-vision-instruct"
auth_url = "https://iam.cloud.ibm.com/identity/token"


st.session_state.transcript = "Upload to get transcript"
st.session_state.insights = "Upload to get insights"
st.session_state.callquality = "Upload to get call quality"
st.session_state.separate = "Upload to get call transcript"
transcript = "upload"
quality = "upload"
insights = "upload"

t = f"""

Hello. Hi, may I speak to Anessa Roberts? This is श्री. Good morning Anessa, this is Candus from कृष्ण Telecom. The reason for my call today is about the form you filled out on our website for our fiber plans. Have I caught you at a good time? 
For now it's fine, but I might be busy soon, but we can talk about it now. 
Perfect, first I'd like to quickly confirm your address and see if it's part of our serviceable locations. What we have here is one one three four five Keyast Bruce Way, San Antonio, Florida three three five seven six. Is this correct? 
That's correct. 
Perfect. So this address is eligible for a fiber connection. We can provide you with the service. Would you like to know more about our available plans? 
Actually, I was just curious if my location is serviceable for fiber, but I am not really actively looking to switch right now. I am kind of happy with my current provider, so... 
I understand. This is just going to be a discovery call to see if there are areas we might be able to help you out with. If I could just ask you real quick, how much is the average speed you're getting from your current provider? 
I'm not sure. I haven't really checked. 
And what is your current provider? 
B CNC. 
And what do you usually use your connection for? Browsing, gaming, streaming? 
All sorts of things, but mainly just browsing, FaceTime, and streaming most of all. 
And are you totally happy with how this performs for each of these activities, or do you think it could be better in some aspects? 
I would say totally happy, but mostly it's acceptable. When watching videos at 4K, there's definitely some lagging. It doesn't matter which device, on our phones or on our TV, it freezes for a few seconds and then resumes. I guess it's the connection because it's definitely not the device. We just bought this 4K TV last month, and it's happening like clockwork every time we watch 4K. Other than that, it's fine.

"""

st.set_page_config(layout="wide", page_title="Wave Infra Call Insights")
st.markdown("<h1 style='text-align:center'>Wave Infra Call Insights</h1>", unsafe_allow_html=True)
st.markdown("<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH' crossorigin='anonymous'>", unsafe_allow_html=True)

top1, top2 = st.columns(2)
bottom1, bottom2 = st.columns(2)

def access_token():
    print("generating access token")
    auth_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to get access token: {response.text}")
    else:
        token_info = response.json()
        # st.write(token_info)
        return token_info['access_token']


def Getcallquality(trans):
    body = {

    "input":f"""
    Below is a transcription of a conversation between two people. need call qualtiy ananalysis for given transcription
    

    The output should look like this:

    Add-on Request by Customer: customer request...........

    Action Taken for the request: action taken by ........

    call rating: rating out of 10

    Reason: reason for the rating

Transcription:
    {trans}

""",
    "parameters":{
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 30,
        "stop_sequences": [";"],
        "repetition_penalty": 1.05,
        "temperature": 0.5
    },
    "model_id": model_id,
    "project_id": project_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token()}"
        }
    response = requests.post(url, headers=headers, json=body)
    st.session_state.callquality = response.json()['results'][0]['generated_text']
    # st.write(st.session_state.insights)

def Separatespeakers(trans):
    body = {

    "input":f"""
Below is a transcription of a conversation between two people but it is in parah not seprately. Your task is to separate the conversation into two distinct parts, where one part is for Person1 and the other is for Person2. Each part should contain the dialogue for each speaker. Label the dialogues as follows speaker one and speaker two

Ensure the dialogues are clearly separated and labeled, maintaining the correct order for each speaker one by one. Separate the conversation based on the order of speech by person one and person two without any explanantion.

The output should look like this:

person1: hi

person2: hi, your name?
...

person1 and person2 will be bold

Transcription:
{trans}
""",
    "parameters":{
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 30,
        "stop_sequences": [";"],
        "repetition_penalty": 1.05,
        "temperature": 0.5
    },
    "model_id": model_id,
    "project_id": project_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token()}"
        }
    response = requests.post(url, headers=headers, json=body)
    st.session_state.transcript = ""
    transcript_data = json.dumps(response.json()['results'][0]['generated_text'])
    st.session_state.separate = json.loads(transcript_data)


def Getinsights(trans):
    body = {

    "input":f"""
Below is a transcription of a conversation between two people. need insight summary from the given transcription

The output should look like this:

Insights Summary: insight summary of the conversation.....

Sentiment: sentiment of the conversation.....

i need Insights Summary and Sentiment only

this is the Transcription:
{trans}
""",
    "parameters":{
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 30,
        "stop_sequences": [";"],
        "repetition_penalty": 1.05,
        "temperature": 0.5
    },
    "model_id": model_id,
    "project_id": project_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token()}"
        }
    response = requests.post(url, headers=headers, json=body)
    st.session_state.insights = response.json()['results'][0]['generated_text']
    # st.write(st.session_state.insights)

def Gettranscript():
    
    try:
        st.write("Uploaded file:", uploaded_file.name)
        url = "https://dev.assisto.tech/workflow_apis/process_file"
        
        payload = {}
        headers = {}
        files = [('file', (uploaded_file.name, uploaded_file, 'audio/mp3'))]
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            # st.success("Request sent successfully!")
                # st.write(response.json()) 
            st.session_state.transcript = response.json()['result'][0]['message'] 
 

            Getinsights(st.session_state.transcript)
            Getcallquality(st.session_state.transcript)
            Separatespeakers(st.session_state.transcript)

        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            st.session_state.transcript = response.text
        
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.session_state.transcript = e

with top1:
    st.subheader("Upload Audio")
    # st.button("Choose File",type="primary",use_container_width=True)
    uploaded_file = st.file_uploader("Choose File")
    # if uploaded_file:
    if st.button("Upload",type="primary",use_container_width=True):
        Gettranscript()
        # Getinsights(st.session_state.transcript)
        # Getcallquality(st.session_state.transcript)
        # Separatespeakers(st.session_state.transcript)

with top2:
    #TRANSCRIPT
    st.subheader("Call Transcript using Watsonx Speech-To-text")
    # st.text_area("",value=st.session_state.transcript,height=300, disabled=True)
    with st.container(height=200, key=1):
        st.write(st.session_state.separate)
    st.markdown("<br>", unsafe_allow_html=True)
    # st.button("Convert to Text")



with bottom1:
    st.subheader("Call Insights by watsonx.ai")
    # st.write(st.session_state.insights)
    with st.container(height=300, key=2):
        st.write(st.session_state.insights)
    # if st.button("Generate Insights" ,use_container_width=True):
    #     Getinsights(st.session_state.transcript)
        

with bottom2:
    st.subheader("Call quality analysis by watsonx.ai")
    # st.write(st.session_state.callquality)
    with st.container(height=300, key=3):
        st.write(st.session_state.callquality)
    # st.button("Call quality analysis",use_container_width=True)


