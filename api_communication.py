import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time


# upload
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size = 5242880):
        with open(filename,"rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    
    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data = read_file(filename=filename))

    #print(upload_response.json())

    audio_url = upload_response.json()['upload_url']
    return audio_url


# transcribe
def transcribe(audio_url):
    transcribe_request = {"audio_url": audio_url}
    transcribe_response = requests.post(transcript_endpoint, json=transcribe_request, headers=headers)
    #print(transcribe_response.json())
    job_id = transcribe_response.json()['id']
    return job_id



# pull
def pull(transcript_id):
    pulling_endpoint = transcript_endpoint + '/' + transcript_id
    pulling_response = requests.get(pulling_endpoint, headers=headers)
    return pulling_response.json()

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = pull(transcript_id)
        if data['status'] == 'completed':
            return data,None
        elif data['status'] == 'error':
            return data,data["error"]
        print('Waiting 30 seconds....')
        time.sleep(30)


# save transcript
def save_transcript(audio_url,filename):
    data, error = get_transcription_result_url(audio_url)
    if not error:
        text_filename = filename.rstrip(".wav")+".txt"
        with open(text_filename,"w") as f:
            f.write(data["text"])
        print("Transcription Saved!")
        return len(data["text"].split(" "))
    elif error:
        print("Error!!", error)
        return 0
