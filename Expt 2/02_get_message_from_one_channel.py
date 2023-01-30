import discord
import os
import json
import time

intents = discord.Intents.all()

client = discord.Client(intents=intents)

TOKEN = 'DISCORD_API_TOKEN'

GUILD_ID = ''

f = open('SERVER_DATA/02_Channel_List_WWG.json')
CHANNEL_ID_ARRAY = json.load(f)

final_channel_data = []

@client.event
async def on_ready():
    # Replace 'guild_id' with the ID of the guild you want to get channels from
    guild = client.get_guild(GUILD_ID)
    
    # Get a list of all channels in the guild
    # channel = client.get_channel(742798380870271169)

    # TODO: Get all messages in batches with sleep function
    async def get_messages(final_channel_data):
        for index in range(0, len(CHANNEL_ID_ARRAY)):
            # try:
                channel = client.get_channel(CHANNEL_ID_ARRAY[index]['id'])

                await client.wait_until_ready()
                async for message in channel.history(limit=15000):
                    # Storing messages in the file CHANNEL_ID.json in MESSAGES folder
                    FILENAME = 'MESSAGES/' + str(CHANNEL_ID_ARRAY[index]['id'])+'-'+CHANNEL_ID_ARRAY[index]['name'] + '.json'

                    # Check whether the specified path exists or not
                    isExist = os.path.exists(FILENAME)

                    if isExist:
                        saved_msgs = open(FILENAME)
                        final_channel_data = json.load(saved_msgs) 

                    if message.embeds:
                        # Extract the text from the embed
                            text = message.content + "\n"
                            for embed in message.embeds:
                                for field in embed.fields:
                                    text += f"{field.name}: {field.value}\n"
                                message_dict = {}
                                message_dict['id']=message.id
                                message_dict['channel']=message.channel
                                message_dict['mentions']=message.mentions
                                message_dict['role_mentions']=message.role_mentions
                                message_dict['author']=message.author
                                message_dict['content']=text
                                message_dict['embeds']=1
                                message_dict['embed_title']=embed.title
                                message_dict['embed_description']=embed.description
                                message_dict['attachments']=message.attachments
                                message_dict['created_at']=message.created_at
                                message_dict['edited_at']=message.edited_at

                    else:
                        message_dict = {}
                        message_dict['id']=message.id
                        message_dict['channel']=message.channel
                        message_dict['mentions']=message.mentions
                        message_dict['role_mentions']=message.role_mentions
                        message_dict['author']=message.author
                        message_dict['content']=message.content
                        message_dict['embeds']=0
                        message_dict['attachments']=message.attachments
                        message_dict['created_at']=message.created_at
                        message_dict['edited_at']=message.edited_at

                    final_channel_data.append(message_dict)

                    if isExist:
                        with open(FILENAME, mode='w') as json_file:
                            json_file.write(
                            json.dumps(final_channel_data, indent=4, sort_keys=True, default=str))
                    else:
                        open(FILENAME, "x")
                        with open(FILENAME, mode='w') as json_file:
                            json_file.write(
                            json.dumps(final_channel_data, indent=4, sort_keys=True, default=str))
                    
                    print("Data updated for:",CHANNEL_ID_ARRAY[index]['id'],CHANNEL_ID_ARRAY[index]['name'])
                    time.sleep(0.1)
            # except:
            #     print("Error Channel:",CHANNEL_ID_ARRAY[index]['id'],CHANNEL_ID_ARRAY[index]['name'])


    client.loop.create_task(get_messages(final_channel_data))
    
client.run(TOKEN)
