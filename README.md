
<h1>WEBSTACK PORTFOLIO PROJECT</h1>
This is an E-commerce api

RESTful HTTP API using Python Flask that allows users to manage their ecommerce platform.

### Signin User
- Create a user 
- users can login
- user can logout
- Create an order

### Admin Priviledges
Add New Product
Update a product
See all users
Create a user
Delete a user

<br></br>
Ability to create, read, update, and delete products, categories. A category can have multiple subcategor.
Products can belong to multiple categories and subcategories.
<br></br>
Fetching a product fetches the details of categories.
<br><br> 

### Usage

## Installation

Create a project folder and a flask folder within:

````
mkdir flask
cd flask
py -3 -m venv flaskApp

````
## How to run

````
git clone https://github.com/GODSPE1/GADGETGO.git

pip install requirements.txt

set FLASK_ENV=development

set DEBUG_MODE=1

flask run

````

Start the server:

`python run.py` (Starts the server on 127.0.0.1:5000)

This project is preloaded with a dummy `sqlite` database located in the `instance` directory. To start from a scratch db, delete the `instance` directory and start the server.

To test the API using Postman, install postman agent in your OS and call the API using Postman.

### Endpoints

#### Fetch users
- [GET] `/user>` - Retrieve a list of customers

- [GET] `/user/<id: int>` - Retrieve a specific customer by their ID.

- [POST] `/user/<id: int>` - Update customer information.

- [DELETE] `/user/<id: int>` - Delete a customer account.

#### Product

- [GET] `/products` - Get all products

- [GET] `/product/(int: product_id)` - Get product with product_id

- [DELETE] `/product/(int: product_id)` - Delete product with product_id

- [POST] `/product/create` - Create a new product

```
{
  "title": "name",
  "description": "description",
  "categories"s //optional
  "price" = "price of product"
  "image" = "image of product"
}
```

- [PUT] `/product/(int: product_id)/update` - Update product with product_id
```
{
  "title": "name",
  "description": "description",
  "categories"s //optional
  "price" = "price of product"
  "image" = "image of product"
}
```

#### Categories
- [GET] `/categorie` - Retrieve a list of categories.

- [GET] `/categories/<id: int>` - Retrieve a specific category by its ID.

- [POST] `/categories` - Create a new category.

- [PUT] `/categories/{id}: Update an existing category.

- [DELETE] `TE /categories/{id}: Delete a category. 

#### Orders
- [GET] `/user>` - Retrieve a list of customers orders

- [GET] `/user>` - Retrieve a list of customers

- [GET] `/orders/<id: int>` -  Retrieve a specific order by its ID for a customer.

- [POST] `/orders` - Create a new order.

- [PUT] `/orders/<id: int>` - Update an existing order (e.g., change shipping address).  

- [DELETE] `/orders/<id: int>` - Cancel an order.