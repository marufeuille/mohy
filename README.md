# Usage
## List Questions
```
curl localhost/questions
```

## Get Question Describe
```
curl localhost/question/QUESTION_ID
```

## Create Question
```
curl -X POST -H "Content-Type: application/json" -d '{"question":"Hello?", "question_type": "FREE_TEXT", "user_name":"UserA"}' localhost/question
```

## Answer Question
curl -X POST -H "Content-Type: application/json" -d '{"question_id":"HTRcwNxsdWjb1lnlRatF", "answer": "hi!", "user_name":"UserB"}' localhost/execution