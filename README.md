# Reddit_Scorer

A data pipeline built using luigi package that helps to retrieve and scores posts from the top subreddits.

The score of the subreddit is calculated by the following formula:

![image](https://github.com/varunpusarla/Reddit_Scorer/assets/51925551/6d2c6b61-5f0a-48a9-abe9-bbda7d635160)



where the post score(PostRS) is calculated by:

![image](https://github.com/varunpusarla/Reddit_Scorer/assets/51925551/d5728249-2a53-482c-a232-ce7de59e4899)

In this project we score the top 50 subreddits by scoring them on the basis of top 5 comments of their top 10 posts.



Sample Output:

![image](https://github.com/varunpusarla/Reddit_Scorer/assets/51925551/167b562f-7b42-4ca2-addf-2be91d345b6b)

Schedule package of python has been used in order to run this pipeline twice a day.

## Environment Setup

1. Install the dependencies by running

```python
pip install -r requirements.txt
```

2. Add the following API credentials(you'll need to register for the reddit API) to an .env file
a) Client ID
b) Client Secret
c) Username
d) Password
e) User agent

3. Run the file:
```python
python app.py
```
