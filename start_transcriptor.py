#!/usr/bin/env python

import os
import uuid
import logging
import base64
import uvicorn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from faster_whisper import WhisperModel, decode_audio
import shutil

app = FastAPI()

logger = logging.getLogger("uvicorn")
model = WhisperModel("tiny")

def uuid2slug(uuidstring):
    return base64.urlsafe_b64encode(uuidstring.bytes).decode("utf-8").strip('=')

@app.get("/")
async def root():
    """
    Just a REST test
    """
    return {"message": "Transcript", "intent": "World"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):

    myuuid = uuid.uuid4()
    filename = "speech-" + uuid2slug(myuuid)
    logger.info("file name: '{}'".format(filename))

    try:
        with open(file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"error": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    shutil.move(file.filename, "/tmp/" + filename)
    return {"transcript_id": filename}

@app.get("/transcript/{transcript_id}")
async def transcript(transcript_id):
    segments, info = model.transcribe("/tmp/" + transcript_id, word_timestamps=True)
    segments = list(segments)
    if len(segments) == 0:
        return {"error": "no segments found!"}
    
    segment = segments[0]
    return {"transcript_id": transcript_id, "text": segment.text}


if __name__ == "__main__":
    uvicorn.run("start_transcriptor:app", host='0.0.0.0', port=8006, log_level="info")
