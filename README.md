# Car_rental_system
This is the first assessment for COMP639, a simple car rental system. Using python Flask and HTML, showing on pythonanywhere.

## Contents
- [Structure] (#Structure)
- [Usage] (#Usage)
- [Shortage] (#Shortage)

## Structure
car_rental_system/
├── car_rental_system/     
│   ├── templates/     
│   ├── static/         
│   ├── views/                   
│   └── __init__.py             
├── run.py              
├── requirements.txt    
└── README.md           

In this project I use blueprint.
In folder views, there are "auth.py" and "routes.py". The routes related to login and registration are located in the "auth.py" file. The others in "routes.py".

## Usage
All the users' password is "123456"
The administrator's username is: admin, password is: 123456
The customer's username is: c2, password is: 123456
The staff's username is: s1

In the navbar:
"CAR": all functionalities related to cars 
"CUSTOMER": all functionalities related to customers
"STAFF": all functionalities related to staffs

You can update your profile when you click the username.

You can find all the customers and staffs when you login with administrator.

In my webpage, I set some functions but no use, like "Search", "Book now".

## Shortage

In this project, I have learned some knowledge, like blueprint, bootstrap. However, there are many shortages in this project and so many things I need to improve.
1. Page design is not good, like the "Add car" button, "Add customer" button and "Add staff" button. 
2. Some functions still need improvement, like "Search" and "Book", at least when user click these, should be give something back.
3. About edit or add car, my idea is administrator or staff can upload picture for car, but now I just use same picture.
