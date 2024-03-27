<div style="position: relative; padding-bottom: 64.98194945848375%; height: 0;"><iframe src="https://www.loom.com/embed/27fcf4dc6a1a4134adde7b86139bf66c?sid=a32ea522-a500-40b6-b6fe-ead1a25ab18f" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

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


### Note

I wanted to add some test cases but I ran out of time and energy for the day
