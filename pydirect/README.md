To run the program:
```
python3 main.py
```

Still redoing some work initially done in JS.

to-do:
- write output of getting all accounts to files for my followed artists and my friend's followed artists
- get shared artists
- get all playlists I follow
- get all playlists my friends follow
- get shared playlists
- track when a friend listens to an artist I follow or a playlist I follow

## Data Models
May want to use a graph database.
- artists
    - uri - string
    - name - string
    - is_following? (maybe)
- accounts
    - uri
    - name
- playlists
- songs