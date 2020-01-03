# Public Transport Management System
## Abstract 
To provide excellent transportation to the citizens is the noble duty of government. To improve the situations of the current intercity bus transportation system, we did this project. There are several problems in the current system like the live location of the bus is not available to the control room, and passengers, live seat count, and fair collection is not known to the control room, etc. We tried to solve some issues through Technology.
## Prolems
- Live location of the bus is not available to control room and users.
- Live seat availability is not available to control room and users.
- Live fair collection is not known to the control room.
- Count the number of passangers travelling without ticket.
## Solution and other features 
- We created one web application for the control room, one mobile application for a conductor, and another mobile app for users.
- Control room can manage buses, routes, conductors(CRUD).
- Contol room can get the live location of each bus.
- To manage security and to reduce human error, QR code is used to pair conductor and bus at the starting of each trip.
- The control room can get a live fair collection of each trip and at the end of the trip.
- The control room can issue automatically generated pass with QR code for regular travelers.
- A Conductor starts the journey by scanning a unique QR code on each bus, with the scanning, the location of the conductor's mobile application starts sharing to the control room.
- A conductor can issue a ticket to the passenger from his/her mobile application.
- A conductor can scan the QR code of regular travelers.
- Passengers can see live location of the bus from their mobile application.
- Passengers can see the live seat availability on their targeted location.
- To detect the passengers traveling without a ticket, we use the image processing module fixed on the top of the door.
## Tools and Technologies
Google Firebase - database<br>
python Django - web-app<br>
android studio - mobile-app<br>
Adobe XD - prototype designing <br>
HTML, CSS, BOOTSTRAP, JavaScript, jQuery
