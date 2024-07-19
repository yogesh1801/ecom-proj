# Project Setup

This guide will walk you through setting up the development environment for the project using Docker and a virtual environment. The project consists of three Django applications: `auth`, `order`, and `product`, which need to be run on different ports.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.x installed

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yogesh1801/ecom-proj.git
cd ecom-proj
```

### 2. Run Docker using Docker Compose

```bash
docker-compose up
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Run Django Projects
```bash
# For auth Project
cd auth
python manage.py runserver 8002

# For order project
cd order
python manage.py runserver 8001

# For product project
cd product
python manage.py runserver 8000
```
### 6. Start a Celery worker

```bash
cd order
celery -A order worker --loglevel=info -P eventlet
```

# Authentication Service API Documentation

This document outlines the API endpoints for user authentication services.

## Base URL

`api/auth/`

## Endpoints

### 1. Register

Create a new user account.

- **URL:** `/register/`
- **Method:** POST
- **Request Body:**
  - `username`: String
  - `password`: String
  - Other fields as required by the UserRegisterForm
- **Responses:**
  - 201 Created: Account successfully created
    ```json
    {
      "message": "Account Created for {username}"
    }
    ```
  - 400 Bad Request: Invalid input
    ```json
    {
      "message": "Please Fill all the required fields correctly",
      "error": {
        // Form validation errors
      }
    }
    ```
  - 405 Method Not Allowed: If not a POST request

### 2. Login

Authenticate a user and create a session.

- **URL:** `/login/`
- **Method:** POST
- **Request Body:**
  - `username`: String
  - `password`: String
- **Responses:**
  - 200 OK: Successfully logged in
    ```json
    {
      "message": "User Logged in Successfully"
    }
    ```
  - 400 Bad Request: Invalid credentials or input
    ```json
    {
      "message": "The user does not exist or credentials are wrong"
    }
    ```
    or
    ```json
    {
      "message": "Please Fill all the required fields correctly",
      "error": {
        // Form validation errors
      }
    }
    ```
  - 405 Method Not Allowed: If not a POST request

### 3. Logout

End the user's session.

- **URL:** `/logout/`
- **Method:** GET
- **Responses:**
  - 200 OK: Successfully logged out
    ```json
    {
      "message": "Logged out Successfully"
    }
    ```
  - 405 Method Not Allowed: If not a GET request

### 4. Change Password

Allow an authenticated user to change their password.

- **URL:** `/changepassword/`
- **Method:** POST
- **Authentication:** Required
- **Request Body:**
  - Fields required by Django's PasswordChangeForm
- **Responses:**
  - 200 OK: Password successfully changed
    ```json
    {
      "message": "Password Changed Successfully"
    }
    ```
  - 400 Bad Request: User not authenticated or invalid input
    ```json
    {
      "message": "User is not Logged In please log in"
    }
    ```
    or
    ```json
    {
      "message": "Please Fill all the required fields correctly",
      "error": {
        // Form validation errors
      }
    }
    ```
  - 405 Method Not Allowed: If not a POST request



# Order Service API Documentation

This document outlines the API endpoints for the order management service.

## Base URL

`api/order/`

## Endpoints

### 1. Create Order

Create a new order for the authenticated user.

- **URL:** `/create_order/`
- **Method:** POST
- **Authentication:** Required
- **Request Body:**
  - Fields as required by the OrderForm
- **Responses:**
  - 200 OK: Order created successfully
    ```json
    {
      "message": "Order created Successfully with id {order_id}"
    }
    ```
  - 400 Bad Request: User not authenticated or invalid input
    ```json
    {
      "message": "User is not Logged In please log in"
    }
    ```
    or
    ```json
    {
      "message": "Please Fill all the required fields correctly",
      "error": {
        // Form validation errors
      }
    }
    ```
  - 405 Method Not Allowed: If not a POST request

### 2. Get Orders

Retrieve a paginated list of orders for the authenticated user.

- **URL:** `/get_orders/`
- **Method:** GET
- **Authentication:** Required
- **Query Parameters:**
  - `page`: Integer (optional, default: 1)
- **Responses:**
  - 200 OK: List of orders
    ```json
    {
      "orders": [
        {
          "id": 1,
          "status": "PENDING",
          "created_at": "2023-07-20T12:00:00Z",
          "total_price": 100.00,
          "items_count": 2
        },
        // More orders...
      ],
      "total_pages": 5,
      "current_page": 1
    }
    ```
  - 400 Bad Request: User not authenticated
  - 405 Method Not Allowed: If not a GET request

### 3. Get Order Detail

Retrieve details of a specific order.

- **URL:** `/<int:order_id>/`
- **Method:** GET
- **Authentication:** Required
- **Responses:**
  - 200 OK: Order details
    ```json
    {
      "id": 1,
      "status": "PENDING",
      "created_at": "2023-07-20T12:00:00Z",
      "updated_at": "2023-07-20T12:00:00Z",
      "total_price": 100.00,
      "items": [
        {
          "item_id": 1,
          "product_id": "PROD123",
          "quantity": 2,
          "status": "PROCESSING",
          "price": 50.00
        },
        // More items...
      ]
    }
    ```
  - 400 Bad Request: User not authenticated
  - 404 Not Found: Order not found
  - 405 Method Not Allowed: If not a GET request

### 4. Get Order Total

Retrieve the total price and item count for a specific order.

- **URL:** `/<int:order_id>/total/`
- **Method:** GET
- **Authentication:** Required
- **Responses:**
  - 200 OK: Order total
    ```json
    {
      "order_id": 1,
      "total_price": 100.00,
      "item_count": 2
    }
    ```
  - 400 Bad Request: User not authenticated
  - 404 Not Found: Order not found
  - 405 Method Not Allowed: If not a GET request

### 5. Add Order Item

Add a new item to an existing order.

- **URL:** `/<int:order_id>/add_item/`
- **Method:** POST
- **Authentication:** Required
- **Request Body:**
  - Fields as required by the OrderedItemForm
- **Responses:**
  - 200 OK: Item added successfully
    ```json
    {
      "message": "Item added Successfully to order {order_id}",
      "item_id": 1,
      "product_id": "PROD123",
      "quantity": 2,
      "status": "PROCESSING",
      "price": 50.00
    }
    ```
  - 400 Bad Request: User not authenticated, order not found, or invalid input
  - 405 Method Not Allowed: If not a POST request

### 6. Update Order Item

Update an existing item in an order.

- **URL:** `/item/<int:item_id>/update/`
- **Method:** PUT
- **Authentication:** Required
- **Request Body:**
  - Fields as required by the OrderedItemForm
- **Responses:**
  - 200 OK: Item updated successfully
    ```json
    {
      "message": "Item updated Successfully",
      "item_id": 1,
      "product_id": "PROD123",
      "quantity": 3,
      "status": "PROCESSING",
      "price": 75.00
    }
    ```
  - 400 Bad Request: User not authenticated or invalid input
  - 404 Not Found: Item not found
  - 405 Method Not Allowed: If not a PUT request

# Product Management API Documentation

This document outlines the API endpoints for the product management service.

## Base URL

`api/product/`

## Endpoints

### 1. Create Product

Create a new product for the authenticated user.

- **URL:** `/create/`
- **Method:** POST
- **Authentication:** Required
- **Request Body:**
  - Fields as required by the ProductForm
- **Responses:**
  - 200 OK: Product created successfully
    ```json
    {
      "message": "product created with id: {product_id}"
    }
    ```
  - 400 Bad Request: User not authenticated or invalid input
  - 405 Method Not Allowed: If not a POST request

### 2. Edit Product

Edit an existing product owned by the authenticated user.

- **URL:** `/edit/<int:pk>/`
- **Method:** POST
- **Authentication:** Required
- **Request Body:**
  - Fields as required by the ProductForm
- **Responses:**
  - 201 Created: Product updated successfully
    ```json
    {
      "message": "Product details updated successfully."
    }
    ```
  - 400 Bad Request: User not authenticated, product not found, or invalid input
  - 405 Method Not Allowed: If not a POST request

### 3. Product Details

Retrieve details of a specific product.

- **URL:** `/details/<int:pk>/`
- **Method:** GET
- **Responses:**
  - 200 OK: Product details
    ```json
    {
      "id": 1,
      "name": "Product Name",
      "description": "Product Description",
      "category": "Category",
      "stock": 100,
      "created_on": "2023-07-20T12:00:00Z",
      "price": 1000,
      "is_active": true
    }
    ```
  - 404 Not Found: Product not found
  - 405 Method Not Allowed: If not a GET request

### 4. User Products

Retrieve a paginated list of products created by the authenticated user.

- **URL:** `/user_products/<int:page>/`
- **Method:** GET
- **Authentication:** Required
- **Responses:**
  - 200 OK: List of user's products
    ```json
    {
      "products": [
        {
          "id": 1,
          "name": "Product Name",
          "description": "Product Description",
          "category": "Category",
          "stock": 100,
          "price": 1000,
          "is_active": true,
          "created_on": "2023-07-20T12:00:00Z"
        },
        // More products...
      ],
      "page": {
        "current": 1,
        "has_next": true,
        "has_previous": false,
        "total_pages": 5,
        "total_items": 50
      }
    }
    ```
  - 400 Bad Request: User not authenticated
  - 405 Method Not Allowed: If not a GET request

### 5. All Products

Retrieve a paginated list of all active products.

- **URL:** `/all_products/<int:page>/`
- **Method:** GET
- **Responses:**
  - 200 OK: List of all active products
    ```json
    {
      "products": [
        {
          "id": 1,
          "name": "Product Name",
          "description": "Product Description",
          "category": "Category",
          "stock": 100,
          "price": 1000,
          "is_active": true,
          "created_on": "2023-07-20T12:00:00Z"
        },
        // More products...
      ],
      "page": {
        "current": 1,
        "has_next": true,
        "has_previous": false,
        "total_pages": 5,
        "total_items": 50
      }
    }
    ```
  - 405 Method Not Allowed: If not a GET request

### 6. Delete Product

Delete a product owned by the authenticated user.

- **URL:** `/delete_product/<int:pk>/`
- **Method:** POST
- **Authentication:** Required
- **Responses:**
  - 200 OK: Product deleted successfully
    ```json
    {
      "message": "Product Deleted Successfully"
    }
    ```
  - 400 Bad Request: User not authenticated or product not found
  - 405 Method Not Allowed: If not a POST request

### 7. Toggle Product Status

Toggle the active status of a product owned by the authenticated user.

- **URL:** `/product_status/<int:pk>/`
- **Method:** POST
- **Authentication:** Required
- **Responses:**
  - 200 OK: Product status updated successfully
    ```json
    {
      "message": "Active status Successfully set to {status}"
    }
    ```
  - 400 Bad Request: User not authenticated or product not found
  - 405 Method Not Allowed: If not a POST request

### 8. Get Product Price

Retrieve the price of a specific product.

- **URL:** `/price/<int:product_id>/`
- **Method:** GET
- **Responses:**
  - 200 OK: Product price
    ```json
    {
      "price": "1000"
    }
    ```
  - 404 Not Found: Product not found

## Notes

- Most endpoints require user authentication.
- The API returns JSON responses for all endpoints.
- Error messages and status codes are provided for easier debugging and error handling on the client side.
- Pagination is implemented for listing products, with 10 items per page.