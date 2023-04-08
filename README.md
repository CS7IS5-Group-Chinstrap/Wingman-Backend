# Wingman-Backend

This is the backend code for the Wingman Dating app.<br/>
Install all the required libraries using the command inside the project directory


`pip install -r requirements.txt`

To run the flask app, use either 

`python app.py`

or

`flask run`

## API's 

- */all-users* - Returns the data for all the users.<br/>

- */get-similar-users/{userID}* - Returns the data for the users similar to a given user (passed as userID in api eg: */get-similar-users/19* ) using K-means clustering

- */get-ice-breakers/{userID}* - Returns icebreakers from topics extracted from a given user's bio (user passed as userID in api eg: */get-ice-breakers/19*) using Latent Dirichlet Allocation (LDA) in gensim.

