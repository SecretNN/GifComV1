# GIFCOM
### platform for save yours GIF files and share them with other


# HOW TO LAUNCH?
| With Docker                                                                  | With out Docker                                                        |
|------------------------------------------------------------------------------|------------------------------------------------------------------------|
| Download [Docker Desktop](https://https://www.docker.com/)                   | Download [Python3.13](https://www.python.org/)                         |
| write in git bash: git clone https://github.com/SecretNN/GifComV1/tree/test2 | in Git bash: git clone https://github.com/SecretNN/GifComV1/tree/test2 |
| also in bash: cd GifComV1                                                    | also in bash: cd GifComV1                                              |
| bash: docker-compose up --build                                              | bash: python -m venv venv                                              |
| Write in browser: localhost:5000                                             | bash: venv\Scripts\activate                                            |
| For stop use CTRL+C in bash                                                  | bash: pip install -r requirements.txt                                  |
|                                                                              | In your idea terminal: python app.py                                   |
|                                                                              | In your idea terminal for stop: CTRL+C                                 |


# HOW TO DELETE GIFS?
## Delte gifs can only user which you choose. 
### You Need to change "Secret" For your nick which you creating by sign up
### first in home.html 22 
```
{% if current_user.is_authenticated and current_user.username == 'Secret'%}
```
### second in app.py 69
```
if current_user.username != 'Secret':
```

# WHERE I CAN FOUND DATABASE WITH GIFS AND USERS?
## U can find database on 
```
GifComV1/
└──instance/ 
```
## to open u need [DB BROWSER FOR SQLITE](https://sqlitebrowser.org/)