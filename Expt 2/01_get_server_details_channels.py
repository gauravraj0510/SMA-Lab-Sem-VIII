import discord
import os
import json

intents = discord.Intents.all()

client = discord.Client(intents=intents)

TOKEN = 'DISCORD_API_TOKEN'

GUILD_ID = ''

final_server_data = {}
CHANNEL_ID_ARRAY = []

@client.event
async def on_ready():
    # Replace 'guild_id' with the ID of the guild you want to get channels from
    guild = client.get_guild(GUILD_ID)
    
    # Get a list of all channels in the guild
    channels = guild.text_channels

    final_server_data['id'] = guild.id
    final_server_data['name']=guild.name
    final_server_data['created_at']=guild.created_at
    final_server_data['owner']=guild.owner
    final_server_data['member_count']=guild.member_count
    final_server_data['total_channel_count']=len(guild.channels)
    final_server_data['text_channel_count']=len(guild.text_channels)
    final_server_data['voice_channel_count']=len(guild.voice_channels)
    final_server_data['each_role_member_count']={}

    for role in guild.roles:
        # Get the members with this role
        members = [m for m in guild.members if role in m.roles]
        final_server_data['each_role_member_count'][role.name]=len(members)


    # Iterate over the channels
    for channel_obj in channels:
        channel = client.get_channel(channel_obj.id)
        channel_name = channel_obj.name
        channel_id = channel_obj.id
        print(channel_name, channel_id)
        CHANNEL_ID_ARRAY.append({"id":channel_id, "name":channel_name})

    final_server_data['channel_details'] = CHANNEL_ID_ARRAY
      

    if (os.path.exists('SERVER_DATA/01_WWG_Server_Details.json')):
      with open('SERVER_DATA/01_WWG_Server_Details.json', mode='w') as json_file:
        json_file.write(json.dumps(final_server_data, indent=4, sort_keys=True, default=str))
    else:
      f = open('SERVER_DATA/01_WWG_Server_Details.json', "x")
      with open('SERVER_DATA/01_WWG_Server_Details.json', mode='w') as json_file:
        json_file.write(json.dumps(final_server_data, indent=4, sort_keys=True, default=str))

    if (os.path.exists('SERVER_DATA/02_Channel_List_WWG.json')):
      with open('SERVER_DATA/02_Channel_List_WWG.json', mode='w') as json_file:
        json_file.write(json.dumps(CHANNEL_ID_ARRAY, indent=4, sort_keys=True, default=str))
    else:
      f = open('SERVER_DATA/02_Channel_List_WWG.json', "x")
      with open('SERVER_DATA/02_Channel_List_WWG.json', mode='w') as json_file:
        json_file.write(json.dumps(CHANNEL_ID_ARRAY, indent=4, sort_keys=True, default=str))

client.run(TOKEN)
