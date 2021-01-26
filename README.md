# Usage

This is a Vue web app which has an image repository which you can hopefully search

# Things I learned

- Never built a RESTFUL API before so this is my first time, this helped me a [lot](https://levelup.gitconnected.com/how-to-build-a-restful-api-using-node-js-express-mongodb-1882a966726c)
- Since this isn't Ruby on Rails, you have to configure a lot of things like establishing the connection to MongoDB, and then setting up the middleware so that Express doesn't stop working, then setting up the model which specifies the structure of how data will be indexed, and then the controller which deals with how requests are being handled
- AWS is a pain in the butt, my advice is to just skim over anything thats recommended, and if you have found out what your are looking for then focus on that. Otherwise you are going to tire yourself out. Thank the lord for this [guide](https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html)
- I just found out how to `this` in a callback. All you have to do is create a new variable for example `let self = this` and then use `self` from now on. Here's a [link](https://stackoverflow.com/questions/45743395/uncaught-in-promise-typeerror-cannot-set-property-of-undefined-with-axios) to my problem and here's an explanation of what's going [on](https://stackoverflow.com/questions/20279484/how-to-access-the-correct-this-inside-a-callback/20279485#20279485).
- For the love of god if you do any asychronous work like fetching from a resource do it don't try to wriggle out of it with synchronous code.
- (January 20, 2021) I just configured the backend with Flask which serves the data from the image classifier and have the Axios client request it, this is so damn cool.
- To add two git repositories together `git subtree add --prefix=[name of new folder] [child git rep url] [branch of git repo you want to be the parent]`, here's a [post](https://stackoverflow.com/questions/1425892/how-do-you-merge-two-git-repositories) about it
- CORS should always be configured when making cross domain requests, here's a great website of how to set up CORS in different [frameworks](https://enable-cors.org/index.html)
- Choose a folder name and stick with it lol but idea to change it later on, (especially if it's really bulky :( )
- THE CLIENT'S REQUEST SHOULD MATCH EXACTLY TO THE SERVER'S ROUTE, a backslash wasted so many hours of my life
- I've decided to enable bucket versionning since there's a higher chance that a user might be frustrated with finding out there image has been wiped out by someone else's image due to AWS S3 overwriting when two image names have the same name.

# To do

- ADD

  - In the event of a successful POST request to my Flask backend, index the data in the Elasticsearch database
  - How to add bulk images?

- SEARCH

  - When we send the search request we look for tags in the Elasticsearch database, then we return the scores which gives the filename
  - TinyEngine [MatchEngine API](https://services.tineye.com/developers/matchengine/api_reference/search) for searching images with images?

- AUTHENTICATION
  - Have ui perform some checks like if the email is valid

# Considerations

- Swagger.io
- JWT
