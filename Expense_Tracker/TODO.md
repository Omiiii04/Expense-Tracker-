# TODO: Fix Expense Tracker Issues

- [x] Add Flask session import and secret key in app.py
- [x] Update login route to set session['user_id'] after successful login
- [x] Update home route to check if user is logged in and filter expenses by session user_id
- [x] Update add_expense route to use session user_id and include date_added in insert
- [x] Update stats route to filter data by session user_id
- [x] Add logout route to clear session and redirect to login
- [x] Add logout link to home.html template
- [x] Add login checks to protected routes (home, add_expense, stats)
