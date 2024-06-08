### Team Draft Web App

This project is a Flask-based web application for conducting team drafts. It allows users to input a list of players, select team captains, and then either manually or randomly draft players onto two teams.

#### How to Use

1. Access the [Team Draft Web App](https://draftmaster-5a8f04263e9a.herokuapp.com/).
2. Enter the 10 players' names.
3. Select team captains.
4. Choose to either randomly draft all players or manually pick players for each team.
5. Once all players have been picked, teams will be displayed, and you can reset the draft if needed.

#### Technologies Used

- **Flask**: A micro web framework written in Python.
- **Flask-SocketIO**: A Flask extension that adds WebSocket support to your application.
- **HTML/CSS/JavaScript**: Front-end technologies for user interface and interaction.
- **Heroku**: Platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

#### File Structure

- **app.py**: Python file containing the Flask application logic.
- **index.html**: HTML file for the front-end interface.
- **SocketIO script**: JavaScript for real-time updates using SocketIO.

#### Project Overview

- **index.html**: Contains the front-end structure and forms for user input.
- **app.py**: Implements the backend logic for handling user requests, managing player data, and updating teams.
- **SocketIO**: Facilitates real-time updates of team rosters without the need for page refresh.

#### Deployment

The application is deployed on Heroku and can be accessed [here](https://draftmaster-5a8f04263e9a.herokuapp.com/).

#### Conclusion
The Team Draft Web App was created to solve a common problem: deciding team captains for game nights with friends. Now, with just a few clicks, you can input player names, select captains, and draft teams effortlessly. Powered by Flask and Flask-SocketIO, along with HTML, CSS, and JavaScript, the app offers a seamless user experience. Whether you're manually picking teams or opting for a random draft, the process is quick and fair. Deployed on Heroku, the app is easily accessible to anyone with an internet connection. It's a simple solution to a common problem, making game nights more enjoyable for all.
