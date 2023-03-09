# ShoppinglyX_e-commerce
Built e-commerce website using Django

#### Demo of:
ShoppinglyX  
- Home
- products
- product-details overview without login 

https://user-images.githubusercontent.com/91488051/223941108-87bf0d69-e2e9-4503-8533-d70278555a17.mp4


Item can not be added to cart or bought if not looged in 

https://user-images.githubusercontent.com/91488051/223940311-97d4e272-2fda-4ae2-acb1-a275cb325ca3.mp4


User Registration

https://user-images.githubusercontent.com/91488051/223940348-bcaebe00-cc99-4471-810c-64d7111083e1.mp4


Search Functionality

https://user-images.githubusercontent.com/91488051/223942411-5b6e9bbc-2ef5-4d87-a407-a0d419a356ce.mp4


complete process of login to buying 

https://user-images.githubusercontent.com/91488051/223939024-f3f6aab1-57a8-4118-8d1a-06d03854c8d1.mp4


Change password Page

![ShoppingX _ Buy Now - Google Chrome 09-03-2023 11_46_37](https://user-images.githubusercontent.com/91488051/223940934-01f983fb-01b4-425e-b17a-768f1b6817ae.png)


Forgot Password Page (Reset Password)

![Screenshot 2023-03-09 114837](https://user-images.githubusercontent.com/91488051/223941285-c58adb84-697e-45e6-9878-f4b1bca79003.jpg)


- Link for reseting Password will be sent to Email after Entering Email address

![Screenshot 2023-03-09 114919](https://user-images.githubusercontent.com/91488051/223941325-fd144732-5189-48b3-b850-481bae868d20.jpg)



## E-Commerce App using Django

This is an e-commerce web application built using the Django web framework. The application allows users to browse, search, and purchase products from the website.
Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

   - Python 3.6 or higher
   - Django 3.0 or higher
   - Sqlite3 database

### Clone the repository:

   In bash type:

    git clone https://github.com/HaardPatel5620/ShoppinglyX_e-commerce.git


## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with


   pip install virtualenv


Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project


      virtualenv env


That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:


      source env/bin/active


Then install the project dependencies with


      pip install -r requirements.txt


Now you can run the project with this command


      python manage.py runserver


## Features

The following features are available in the application:

 - User authentication: users can create an account and log in to the website
 - Product browsing: users can browse products by category or search for products by name or description
 - Product details: users can view detailed information about a product, including images, description, and price
 - Cart management: users can add products to their cart, view the cart, and checkout to place an order
 - Order history: users can view their order history and the status of their orders

## Architecture

The application is built using the Django web framework, which follows the Model-View-Controller (MVC) architecture pattern. The database is implemented using Sqlite3, and the front-end is implemented using HTML, CSS, Bootstrap, JavaScript and Ajax.

The ShoppinglyX directory contains the main settings file and URL configuration. The app directory contains the application for managing products, users and authentication. The templates directory contains the HTML templates, the static directory contains the CSS and JavaScript files, and the media directory contains the uploaded images.
