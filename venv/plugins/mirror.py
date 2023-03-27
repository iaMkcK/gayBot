import discord
import asyncio
import re
import settings

userToken = settings.PERSONAL_TOKE
botToken = settings.DICKSWORD_TOKE

sourceChannelID = "1059128851898306560"
targetChannelID = "1087808106790125699"

intents = discord.Intents.default()
botClient = discord.Intents.default()
userClient = discord.Intents.default()

@userClient.event
async def on_ready():
    print("User account connected")
    print(userClient.user.name)
    print(userClient.user.id)
    print("-------")

@botClient.event
async def on_ready():
    print("Bot account connected")
    print(botClient.user.name)
    print(botClient.user.id)
    print("-------")

# Return a string with the url contained in a given string.
def find_url(string):
    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", string)
    return url

# Returns a discord.Embed ready to be sent.
def build_embed(authorName, authorPicture, embedDesc, embedColor, embedImage):
    emb = discord.Embed()
    emb.set_author(name=authorName, url="", icon_url=authorPicture)
    emb.description = embedDesc
    emb.color = embedColor
    messageUrls = find_url(embedDesc)
    if embedImage != "":
        emb.set_image(url=embedImage)
        print(authorName + " uploaded an image")
    elif len(messageUrls) > 0:
        emb.set_image(url=messageUrls[0])
        print(authorName + " linked an image")
    else:
        print(authorName + ": " + embedDesc)
    return emb

@botClient.event
async def send_message(messageEmbed):
    channel = botClient.get_channel(int(targetChannelID))
    await channel.send(embed=messageEmbed)

@userClient.event
async def on_message(message):
    if message.channel.id == int(sourceChannelID):
        authorName = message.author.name + "#" + message.author.discriminator
        if len(message.attachments) > 0:
            imageURL = message.attachments[0].url
        else:
            imageURL = ""
        await send_message(build_embed(authorName, message.author.avatar_url_as(format=None,static_format='png',size=1024), message.clean_content, message.author.color, imageURL))

# Async loop allows both clients to run simultaneously.
loop = asyncio.get_event_loop()
task1 = loop.create_task(userClient.start(userToken))
task2 = loop.create_task(botClient.start(botToken))
gathered = asyncio.gather(task1, task2)
loop.run_until_complete(gathered)


if __name__ == "__main__":
    run()