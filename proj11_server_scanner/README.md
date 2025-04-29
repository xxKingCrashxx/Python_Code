# Minecraft Server Scanner
This simple application utilizes the fact that one can query any minecraft server for basic metadata such as the player count and sample of the list of players online. Assuming the server does not have any plugins to scramble this metadata, one can gather metrics about who typically plays on the server, at what time, and for how long. This information can then later be transformed to find patterns about each individual player or the player population as a whole on the server.

## Libraries Used
- mcstatus
- pymongo
- python-dotenv
- tzdata

mcstatus and pymongo are the primary libraries used for querying and storing the data.

## How It Works
By default, a vanilla minecraft server allows basic pinging to see the players online / total supported players on the server. It also includes a sample, typically a max of 15, of players currently online. Every minute the script pings the server and keeps track of a dictionary of players and set of currently retrieved players. This way we can determine players who left and who joined by comparing the difference between the two.