i want to make a telegram bot which i can do something like a slash command "/reminder" and if i use this reminder command the bot will send me in a week from there a message and asks me if i am still into this idea and reminds me about the idea i had.
if i dont use the reminder command the bot will respond as helpful assistant with around 100k context tokens

- make a slash command /reminder and if this slash command is getting triggered the llm sends me a reminder about this 
- if no reminder is set the conversation is just a normal chatgpt convo


action checks every day in database if a reminder is ready if so reminder message is send 

- make basic bot with which i can chat on telegram
    - best way to host bot?
- implement reminder function together with github actions
- make the bot pretty and finish

i can just do serverless functions with webhooks - will figure this out on the way