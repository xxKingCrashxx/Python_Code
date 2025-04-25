from pymongo import MongoClient
from bson.codec_options import CodecOptions
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os
import tzdata

MONGO_STRING = os.getenv("MONGO_STRING")

client = MongoClient(MONGO_STRING)
db = client["Peters-Minecraft-Server"]

player_events_timeseries_new = db.create_collection(
    name="player_events",
    codec_options=CodecOptions(
        tz_aware=True,
    ),
    timeseries={
        "timeField": "timestamp",
        "metaField": "event_info",
        "granularity": "minutes",
    }
)


player_sessions_timeseries_new = db.create_collection(
    name="player_sessions",
    codec_options=CodecOptions(
        tz_aware=True,
    ),
    timeseries={
        "timeField": "join_timestamp",
        "metaField": "session_info",
        "granularity": "minutes",
    }

)

old_events_collection = db.get_collection("player_events_timeseries")
old_session_collection = db.get_collection("player_sessions_timeseries")

old_events_documents = list(old_events_collection.find())
old_session_documents = list(old_session_collection.find())

for doc in old_events_documents:
    
    player_events_timeseries_new.insert_one({

        "timestamp": doc["timestamp"]
            .replace(tzinfo=ZoneInfo("America/New_York"))
            .astimezone(timezone.utc),
        "event_info": {
            "player_id":  doc["event_info"]["player_id"],
            "player_name": doc["event_info"]["player_name"],
        },
        "event_type": doc["event_info"]["event_type"]
    })

for doc in old_session_documents:
    player_sessions_timeseries_new.insert_one({
        "join_timestamp": doc["join_timestamp"]
            .replace(tzinfo=ZoneInfo("America/New_York"))
            .astimezone(timezone.utc),
        "left_timestamp": doc["session_info"]["left_timestamp"]
            .replace(tzinfo=ZoneInfo("America/New_York"))
            .astimezone(timezone.utc),
        "play_time": doc["session_info"]["play_time"],
        "session_info": {
            "player_id": doc["session_info"]["player"]["player_id"],
            "player_name": doc["session_info"]["player"]["player_name"]
        } 
    })

players_collection = db.get_collection("Players")
players_list = list(players_collection.find())

for player in players_list:
    players_collection.update_one(
        {
            "_id": str(player["_id"])
        },
        {
            "$set": {
                "first_joined": datetime \
                    .fromisoformat(player["first_joined"]) \
                    .replace(tzinfo=ZoneInfo("America/New_York")) \
                    .astimezone(timezone.utc),
                "last_seen": player["last_seen"] \
                    .replace(tzinfo=ZoneInfo("America/New_York")) \
                    .astimezone(timezone.utc)
            }
        }
    )



