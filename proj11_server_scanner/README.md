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

### Database Setup
Since there are primarily two main things we can collect: players joining and leaving, we have two main events: PLAYER_JOIN and PLAYER_LEAVE that stores the players name and uuid aswell as the timestamp of when the event was initiated. There is also one more event that we can add called NEW_PLAYER. We can keep track of the number of unique players seen on the server in a different collection. This event would only trigger if the player hasn't been added to the collection of distinct players. 

A join and leave event are typically associated with each other. The span of time between the join and leave can be called a session and this script also logs sessions after a player leaves.

So in total we have 3 primary collections:
- Players
- Player_Events
- Player_Sessions

The Schema for each is the following:

```javascript
//Players Schema:

{
    _id: String (mcuuid)
    player_name: String (username of player),
    total_playtime: Int,
    first_joined: Date,
    last_seen: Date,
}

//Player_Events:
{
    timestamp: Date,
    event_type: String ["PLAYER_JOIN" | "PLAYER_LEAVE" |"NEW_PLAYER"],
    event_info: {
        player_id: String (mcuuid),
        player_name: String,
    }
}

//Player_Sessions

{
    join_timestamp: Date,
    leave_timestamp: Date,
    play_time: Int,
    session_info: {
        player_id: String
        player_name: String
    }
}
```

### Implications
From the corresponding collections, one can get a pretty accurate understanding of the activity of the server as well as the individual activity of specific players. Keep in mind, that this script can gather all the above information without the need for admin access. Unless active effort is done by the admins, like spoofing the list of currently online players, and limititing or turning off the sample player list, this information is free for the taking.