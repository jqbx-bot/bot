# JQBX Bot

## Commands

| Command | Description | Example |
| --- | --- | --- |
| /welcome | Sets the welcome message. If no welcome message provided, displays the current message. (Note: "Welcome [user(s)]!" automatically gets prefixed into the welcome message, so you only need to provide the extra context to include with the welcome.) | `/welcome Today's theme is beans!` |
| /unwelcome | Clears the current welcome message. New users will not be greeted by the bot until a new message is set via `/welcome` | |
| /dadjoke | Tells a random dad joke. | |

## TODO:
* Implement commands: `/relink`, `/ro`, `/urban`, `/inspiration`
* deploy to cheap AWS ECS cluster