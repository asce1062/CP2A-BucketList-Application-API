# CP2A - BucketList Application API

### Requirements

To complete this checkpoint you must have completed Modules 5, 6 and 7.

#

### Problem Description

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.
In this exercise you will be required to create an API for an online Bucket List service using Flask.
Specifications for the API are shown below. You may use any database you prefer for this assignment.


EndPoint    |   Functionality
-----------:|:---------------
`POST /auth/login`                          | Logs a user in
`POST /auth/register`                       | Register a user
`POST /bucketlists/`                        | Logs a user in
`GET /bucketlists/`                         | List all the created bucket lists
`GET /bucketlists/<id>`                     | Get single bucket list
`PUT /bucketlists/<id>`                     | Update this bucket list
`DELETE /bucketlists/<id>`                  | Delete this single bucket list
`POST /bucketlists/<id>/items/`             | Create a new item in bucket list
`PUT /bucketlists/<id>/items/<item_id>`     | Update a bucket list item
`DELETE /bucketlists/<id>/items/<item_id>`  | Delete an item in a bucket list

#

### Before you begin this checkpoint, ensure to review this material
[Best Practices for a pragmatic RESTful API](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)

#

### Task 0 - Create Data Models

For this task you will be creating the models for the data which your application will be manipulating. This should be done using SQLAlchemy.

#

### Task 1 -  Create Migration Script

For this task you will be creating scripts for handling migration of data when the data model changes. The script should contain the following tasks.

+ Create migrations
+ Apply migrations
+ Manually Create databases
+ Manually Drop databases

#

### Task 2 - Create Application Configurations

For this task you are required to create a flexible way for storing the application configurations. For this task, think about the different environments your application will be deployed to i.e Testing, Development and Production.

#

### Task 3 - Create the API endpoints

In this task you are required to create the API endpoints described above using any of [Flask](http://flask.pocoo.org/), [Flask-RESTful](http://flask-restful-cn.readthedocs.org/en/0.3.4/) or [Flask-RESTless](https://flask-restless.readthedocs.org/en/latest/index.html) as primary framework. Refer to the documentation on HTTP, APIs and Webservices for information on considerations and best practices.

The prefered JSON response for a single bucket list is shown below.

<pre>
{
	id: 1,
	name: “BucketList1”,
	items: [
		{
            id: 1,
            name: “I need to do X”,
            date_created: “2015-08-12 11:57:23”,
            date_modified: “2015-08-12 11:57:23”,
            done: False
        }
    ]
	date_created: “2015-08-12 11:57:23”,
	date_modified: “2015-08-12 11:57:23”
	created_by: “1113456”
}
</pre>

Ensure that your API is versioned as v1. See the material referenced above for more details on this.

#

### Task 4 - Implement Token Based Authentication

For this task, you are required to implement Token Based Authentication for the API such that some methods are not accessible via unauthenticated users. Access control mapping is listed below.

EndPoint    |   Public Access
-----------:|:---------------
`POST /auth/login`                          |   `TRUE`
`POST /auth/register`                       |    `TRUE`
`POST /bucketlists/`                        |   `FALSE`
`GET /bucketlists/`                         |   `FALSE`
`GET /bucketlists/<id>`                     |   `FALSE`
`PUT /bucketlists/<id>`                     |   `FALSE`
`DELETE /bucketlists/<id>`                  |   `FALSE`
`POST /bucketlists/<id>/items/`             |   `FALSE`
`PUT /bucketlists/<id>/items/<item_id>`     |   `FALSE`
`DELETE /bucketlists/<id>/items/<item_id>`  |   `FALSE`

#

### Task 5 - Implement Pagination on your API

For this task, you are required to implement pagination on your API such that users can specify the number of results they would like to have via a GET parameter `limit`. The default number of results is 20 and the maximum number of results is 100.

###### Request

`GET http://localhost:5555/bucketlists?limit=20`

###### Response

20 bucket list records belonging to the logged in user.

#

### Task 6 - Implement Searching by name
For this task, you are required to implement searching for bucket lists based on the name using a `GET` parameter `q`. The result set should also be paginated.

###### Request

`GET http://localhost:5555/bucketlists?q=bucket1`

###### Response

Bucket lists with the string “bucket1” in their name.

#

### Just for Fun

+ Stretch your API to see how it performs for multiple requests using [Apache AB](https://www.digitalocean.com/community/tutorials/how-to-use-apachebench-to-do-load-testing-on-an-ubuntu-13-10-vps).
+ Build a mobile front-end for your application using Ionic.
+ Read more about best practices for API design.