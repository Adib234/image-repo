# Usage

This is a Vue web app which has an image repository which you can hopefully search

Here are some commands to run to get this up and running (all of these are performed from the root directory).

```bash
cd frontend && npm run serve # to get the frontend running, has hot reload enabled
```

```bash
cd backend && FLASK_APP=main.py flask run # to get the backend running, has a lot of logging to help debugging
```

```bash
elasticsearch # to start the elsaticsearch instance for searching
```

# Architecture diagram

![](res/2021-02-17-17-47-36.png)

# Features

**SEARCH function**

- [x] from characteristics of images
  > I have the user choose to describe their image when they add it or if they choose not to my route that handles adding images has an image classifier called ImageAI that uses a DenseNet model by Facebook AI research. This also gets stored in my Elasticsearch database so when users use my search bar, the query is searched upon in my Elasticsearch database.
- [x] from text
  > I have a search bar on my client that accepts queries, once the search button is clicked on the client sends the query as a request to my Flask backend and in there I have an Elasticsearch database. The full-text search engine then returns the top 5 images that match the description
- [] from an image (search for similar images)
  > This is not supported as I don't know how based on my architecture to create a service or use an API

**ADD function**

- [] one / bulk / enormous amount of images
  > Adding only one image is currently supported
- [x] private or public (permissions)
  > I enabled permissions through authentication, so when you first sign up a folder is in the bucket. The user has the choice to either upload to the public repo which means the toggled 'Public' in their option. If they toggled 'Private' then that means that it will be in a folder that they have selected from the dropdown.
- [x] secure uploading and stored images
  > I use Amazon S3 to upload and store images since upon creation only the users have access to the resources available in Amazon S3. Also, default server-side encryption is enabled to add an additional layer of security.

**DELETE function**

- [x] one / bulk / selected / all images
  > One/bulk/selected/all images is supported using `s3.deleteObject`!
- [x] Prevent a user deleting images from another user (access control)
  > Authentication of users handles this since each user is given an object directory to store their images or more folders and they only have access to this since their email is the unique identifier that has to match with the name of the object directory
- [x] secure deletion of images
  > I'm using Amazon S3 which is known for secure deletion

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
- Passwords should never be stored in a database, do some hashing to it and then discard it immediately after
- If you're using environment variables you gotta export in the session of the shell you are working on in the terminal, having a .env sometimes doesn't do everthing
- Enabling CORS solves CORS issues with the server but not the client, when you send a request back, you must have `Access-Control-Allow-Origin:*` in your response header. Otherwise you're going to have server saying 200 but client throwing a bad error.
- Why hash passwords instead of encrypt? what happens when two hashes are the same
- To prevent the data from being sent in real text, secure requests using HTTP basic authentication so your hash isn't in vain
- To change the state of the parent component, pass an event down the child and on the event the child will `$emit(event)`, used this to logout from my component
- Usually the two key advantages of client side caching are:
  - Data is available with a very small latency.
  - The database system receives less queries, allowing to serve the same dataset with a smaller number of nodes.
- Used Redis to decrease time required to send a response from my backend my 6x! REDIS IS WOW :)
- Users can now search in public and private repos
- When you first try to connect to an EC2 instance, don't use `https` but `http`, when use `https` it tries to establish a HTTPS/SSL connection and not an unencrypted HTTP connection to your server.
- This [tutorial](https://hackernoon.com/tutorial-creating-and-managing-a-node-js-server-on-aws-part-1-d67367ac5171) helps get started with an EC2 instance
- Deploying the [frontend](https://jgefroh.medium.com/a-guide-to-using-nginx-for-static-websites-d96a9d034940) need to register a domain name, most of them cost money :(, my frontend is on EC2 instance but I just couldn't get the backend there. For some reason too many missing modules in my requirements.txt.
- Find out ways to register domain name, maybe use [Amazon](https://aws.amazon.com/getting-started/hands-on/get-a-domain/) in the future?
- Other links that I found helpful were this [fullstack deplyoment tutorial](https://www.freecodecamp.org/news/lessons-learned-from-deploying-my-first-full-stack-web-application-34f94ec0a286/), using [pm2](https://medium.com/hackernoon/tutorial-creating-and-managing-a-node-js-server-on-aws-part-2-5fbdea95f8a1#.mnlkymeti), [nginx and flask](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18), [reducing build size in production](https://medium.com/js-dojo/how-to-reduce-your-vue-js-bundle-size-with-webpack-3145bf5019b7)
- use `flex-wrap: wrap` to make content dynamically be on the next line or row

# To do

- lighthouse labs
- show a demo of your app
- ask for feedback on vuejs, flask, and a bunch of other places! create a section of it

# Technologies used

### Backend

- Flask as server
- Passlib to hash passwords
- MongoDB as database
- ImageAI to classify images
- Elasticsearch as full-text search engine

### Frontend

- Vue.js for frontend framework
- Axios for making calls to server
- Bulma as CSS framework
- AWS-SDK to connect to AWS-S3 for using their buckets to store images for public and private repositories

# Some things I look to do in the future/ improvements that could be made

- I didn't quite understand how to modularize my routes with Flask which I should do in the future because having a lot of code in one file makes it hard to debug. The thing that prevented me was that Flask's factory application was confusing
- How do I make methods in one child component be available in another child component with the same parent? This would allow code to be reused and not violate the DRY principle
- Perform some validation when users enter a name for their private albums since the name of their private album is the bucket name
- Because of bad planning, when the user creates a new account for some reason the home page and signup page have the same route
- I tried refactoring with Flask but it didn't work, from now on I will keep routes skinny and middlewares fat instead of having code that connects to the database or does some processing on the request be in the same file as the routes.
- Verify that user is not bot and send verification email?
- Support for adding bulk images
- Make access to MongoDB more secure

# Twelve factor app

| Factor              | Description                                                      | Did we do it       | How did we do it/not do it?                                                                                                                                                                                                                                                                                                  |
| ------------------- | ---------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Codebase            | One codebase tracked in revision control, deploys                | :heavy_check_mark: | My app uses Git as the version control system and this repo is the copy of the revision tracking database                                                                                                                                                                                                                    |
| Dependencies        | Explicity declare and isolate dependencies                       | :heavy_check_mark: | I sort of did this because I do have explicity dependency declaration which is just the `npm install` and the commands for starting up the backend and frontend which are like the builds. I'm confused though if my frontend offers any dependency isolation, however I know my backend does because I'm using `virtualenv` |
| Config              | Store config in the environment                                  | :heavy_check_mark: | Strict separation of config variables from code in `.env`                                                                                                                                                                                                                                                                    |
| Backing services    | Treat backing services as attached services                      |                    | We have backing services but I don't think we have backups of any of the backing services                                                                                                                                                                                                                                    |
| Build, release, run | Strictly separate build and run stages                           |                    | Haven't even looked into releasing yet, so this is not done : (                                                                                                                                                                                                                                                              |
| Processes           | Execute the app as one or more stateless processes               | :heavy_check_mark: | No sticky sessions, anything that needs to persist is on a backing service that's either third-party (i.e. AWS) or a database (MongoDB)                                                                                                                                                                                      |
| Port binding        | Export services via port binding                                 | :heavy_check_mark: | On development services are exposed via port binding for example backend is `localhost:5000` and frontend is `localhost:8080`                                                                                                                                                                                                |
| Concurrency         | Scale out via the process model                                  |                    | Didn't understand this, I will look into this the next time I develop something similar. I have no tasks running in the background but I think if I had them, it would be better since the wait time to fetch for example images would be less.                                                                              |
| Disposability       | Maximize robustness with fast startup and graceful shutdown      |                    | Fast startup because not many things need to be run but no graceful shutdown other than killing each individual process that is required to keep the app up                                                                                                                                                                  |
| Dev/prod parity     | Keep development, staging, and production as similar as possible | :heavy_check_mark: | pretty much identical, you can check the production branch, the only difference is that i deleted all comments to minify javascript                                                                                                                                                                                          |
| Logs                | Treat logs as event streams                                      |                    | I didn't do this since I didn't deploy my project but in the future if I do then I will look into using Splunk for analyzing logs to find specific event in the past, gain insights of my backend such as requests per minute and monitoring                                                                                 |
| Admin processes     | Run admin/management tasks as one-off processes                  |                    | I have no admin environment                                                                                                                                                                                                                                                                                                  |
