# Email Service API
This is a simple application for sending scheduled emails, using two different email service providers to ensure reliability  (SendGrid and Mailgun).
>The solution focuses on the back-end aspect of the problem.

This application is written in python using Flask micro-framework. Flask is known with being simple to learn and use and it's minimalist core functions.

The application consists of one main routing function `send_email` that routes to the index page and two helping functions `use_sendgrid` and `use_mailgun` to build requests sending emails using SendGrid and Mailgun services respectively.
## Trade offs:
Due to the time constraint I left bare except clauses.

Up and running at: https://emailservice-api-heroku.herokuapp.com/
