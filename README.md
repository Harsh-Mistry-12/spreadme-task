# spreadme-task

# Add employees

curl --location 'http://127.0.0.1:8000/employees' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Jimil Patel",
    "email": "jimilpatel009@gmail.com",
    "designation": "Senior Data Administrator",
    "salary": 65300
}'


# Fetch employees

curl --location 'http://127.0.0.1:8000/employees/3' ---> Fetch specific employee
curl --location 'http://127.0.0.1:8000/employees/' ---> Fetch all employees


# Edit employees

curl --location --request PUT 'http://127.0.0.1:8000/employees/1' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Harsh G Mistry",
    "salary": 37000.0
}'


# Delete employee

curl --location --request DELETE 'http://127.0.0.1:8000/employees/2'


Note:
I am not able to attach Postman Collection as I was not using Signed In Account.


