Run ```parseprofile.py``` with the command ```python parseprofile.py [leetify_profile_link or just steamID]```. This will pull all recent matches from that specific player and then save all of their game files in a directory named after their steamID. Once all files have been pulled, an SQL database will be created and the name of that SQL database will be added to ```databases.json```. 

If you run ```mergeDB.py``` all of the SQL database files listed in ```databases.json``` will be merged into one whole SQL database.

To run ```toggleIsCheat.py``` run the command ```python toggleIsCheat.py [SQL database filename]```. This will turn the ```isCheat``` variable to ```1``` instead of ```0``` and will drop all matches where the suspected cheater has lost.
