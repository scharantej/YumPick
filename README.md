# Flask Application Design

## HTML Files

- **index.html**:
 - Homepage of the website.
 - Contains a description of the website, introduces the concept of the Dish of the Week, and provides links to:
   - The poll to vote for the dish of the week.
   - The menu page to order the dish of the week.
   - The sign-in / up page.

- **poll.html**:
 - Page where users can vote for their favorite dish from a list of options.
 - Contains a form with a list of dishes as radio buttons.
 - When a user selects a dish and submits the form, the selection is recorded in the database.

- **menu.html**:
 - Page displaying the dish of the week and its details.
 - Includes the dish name, description, delivery information, and cost.
 - Provides a form for users to enter their order details and submit the order.

- **order_confirmation.html**:
 - Page displayed after a user successfully places an order.
 - Confirms the order details and provides a unique order ID.

## Routes

- **@app.route('/')**:
 - Route for the homepage (`index.html`).

- **@app.route('/poll')**:
 - Route for the polling page (`poll.html`).

- **@app.route('/menu')**:
 - Route for the menu page (`menu.html`).

- **@app.route('/order', methods=['POST'])**:
 - Route for handling the order form submission.
 - Validates the order details and saves them in the database.
 - Redirects to the order confirmation page (`order_confirmation.html`).

- **@app.route('/order_confirmation')**:
 - Route for the order confirmation page (`order_confirmation.html`).

- **@app.route('/login')**:
 - Route for displaying the login page.

- **@app.route('/signup')**:
 - Route for displaying the signup page.

- **@app.route('/authenticate', methods=['POST'])**:
 - Route for handling login and signup requests.
 - Authenticates the user and creates a session.
 - Redirects to the homepage (`index.html`).

- **@app.route('/logout')**:
 - Route for handling logout requests.
 - Invalidates the session and redirects to the homepage (`index.html`).