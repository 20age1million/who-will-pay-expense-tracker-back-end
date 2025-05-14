# WhoWillPay Expense Tracker — Back-end

> The server-side API for WhoWillPay: manages expense records, computes weights, and serves JSON data to the front-end.
> The front-end file can be found in [WhoWillPay Expense Tracker - Front-end](https://github.com/20age1million/who-will-pay-expense-tracker)

## Features
- **Record Payments**: Create, read, and list expense entries  
- **Compute Next Payer**: Return a weighted random “who pays next” decision  
- **Dashboard Data**: Aggregate totals, counts, and averages per person  

## Tech Stack
- Python 3.x & [Flask](https://flask.palletsprojects.com/)  
- SQLite for lightweight storage  
- Deployed via Nginx
