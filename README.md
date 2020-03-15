
# Bmat

Software engineer test for BMAT.

## Installation

Clone the repository

    git clone https://github.com/xyvs/bmat
  
Enter the app folder

	cd bmat

Build the docker image with [Docker](https://www.docker.com) installed:

    docker-compose build

Start the docker service

    docker-compose up -d

Run the initial migrations

    docker-compose exec web pipenv run -- python bmat/manage.py migrate
   

## Usage / Testing

There were a couple of things I have to change in order to make the test.py file work, for example to assert the response code I have to return the reponse and not the content in the get_response method, that way I could access the response code and the response data, and have both test passed, I also include a few print statements just to make it look pretty displaying on the console. Along side with that, I decided to make my own unit tests with the help of the django test suite, this tests can be found at bmat/core/test.py, I even added some songs I like there. :) (Blink-182 Included). That way I covered a bit more on the unit tests since test.py covers functional tests pretty well.

Run functional tests (test.py)

    docker-compose exec web pipenv run -- python test.py
   
Run unit tests (bmat/core/test.py)

    docker-compose exec web pipenv run -- python bmat/manage.py test core

## Questions

### Tell us about your design choices, and why you made them.

> There were a few design choices I had to make when making the app, for example, the views in which an element is created I decided to inherit from CreateAPIView, so it becomes easier to use and takes all the validations of the model, aside to that, I overwritten a few methods in the serializer to make the view idempotent, also create a special class to make the slug field work idempotently, this helps to make the response more error-proof, for example when trying to send a duplicate value, just return the one that already exists and not a response code of 400 saying that the value already exists, as for the other views I added some validators to be able to handle errors in the values sent to the view, in the case of the GetTopAPIView view, I make a class to help code legibility since the view does several things. On the database decision, I chose PostgreSQL, besides being a very mature and completely open source solution, it contains some special integrations with django like ArrayField or JSONField, which makes it an ideal Django companion. Many validations work at the database level and in many cases the creation of objects are wrapped to avoid any errors in them. To handle packages and virtual environments I decided to use pipenv I think it offers a lot of utility and speed up some processes, the project also includes some dev dependencies like isort to order imports and flake8 for linting that way the code follows the PEP8 style guide, also to make the project run I opt for docker.

### What you provided is a prototype and therefore not production ready software. But, of course, the marketing team doesn't know about that and already sold the finished product to three different customers. What do you think needs to be improved in your software in order for it to be used in production?

> Authentication and cache, would be essential. Better documentation like docstring will make it more easy to work with multiple developers, also docker is more likely configured to work in dev environments, some fixes like serve static files with Nginx and and run on Gunicorn will make it more production ready, maybe a more flexible environment variable handler like django-environ and a  DevOps pipeline.

### How do you think your program would behave if the fingerprinting team went crazy, inserted ten million songs and started monitoring two thousand channels

> Slow, cache would help in a lot of transactions, and I think infrastructure has a lot of weight in this cases since the most heavy task here is insertion, deploying the app on multiple server and adding a load balancer will make the responses better, faster also less prone to errors.
