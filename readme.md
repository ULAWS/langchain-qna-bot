# Welcome to QnA builder

The project is divided into **client** and **server** sections

## Server

To run->

1. `cd server`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`

## Client

To run->

1. `cd client`
2. `npm start`

## How it works?

- The client will launch on port 3000 and server on 8000 by default.
- The UX will ask for the doc first, which can a JSON or a PDF file. If it's a JSON make sure there is a `content` field which is an array of the content which will be ingested
- You will then be required to add the questions JSON file, which needs to have the questions as an array in the `questions` field
- You can choose the test files from the _testDoc_ folder. I'd recommend using the tennisRules.pdf and then questions.json
- You'll see a raw json string as the result in the UI, which can be prettified later
