# Wingman-Backend

This is the backend code for the Wingman Dating app.
Install all the required libraries using the command inside the project directory


`pip install -r requirements.txt`

To run the flask app, use either 

`python app.py`

or

`flask run`

## API's 

*/usersdata* - Returns the data for all the users.
*/getSimilarUsers?userID={userID}* - Returns the data for the users similar to a given user (passed as userID in api query parameter) using K-means clustering
