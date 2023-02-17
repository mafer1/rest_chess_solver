# REST Chess solver

Project of web application based on Python(3.8), Flask and Docker. The main purpose of the application is creating and validating available moves of chess pieces.

## Requirements:
* Docker
* Docker-compose
* Docker Desktop (MacOS and Windows users)

## Installation:
* in folder: src/
```
   docker-compose up
```
Program is exposed on localhost(0.0.0.0) on port 8000:
All functions are available in route /api/v1/:
* Greetings:
```
    curl http://0.0.0.0:8000/api/v1/
```
* List of moves for defined chess pieces on chess board
  * types of chess pieces:
    * pawn
    * knight
    * rook
    * queen
    * king
  * This endpoint receives 2 parameters:
    * chess_figure - one from a list from above
    * current_field - string combination representing staring point on chess board ie. "A2", "b2" etc.

### Schema:
```
    /api/v1/<string:chess_figure>/<string:current_field>
```

### Example:
```
    curl http://0.0.0.0:8000/api/v1/pawn/b1
```
* Move validator which verifying correctness of starting and ending points combinations
  * This endpoint receives 2 parameters:
    * chess_figure - one from a list from above
    * current_field - string combination representing staring point on chess board ie. "A2", "b2" etc.
    * dest_point - string combination representing destination point on chess board
### Schema:
```
    /api/v1/<string:chess_figure>/<string:current_field>/<string:dest_field>
```

### Example:
```
    curl http://0.0.0.0:8000/api/v1/pawn/b1/c6
```


### Stack:
* Python 3.8.16
* [Flask 2.2.2](https://flask.palletsprojects.com/en/2.2.x/)
* Black
* Pytest
* Docker
