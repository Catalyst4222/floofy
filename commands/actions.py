import re
from random import choice, randint
from typing import Optional

from discord import Guild, Member, Message
from discord.ext import commands

from static.action_texts import actions

MENTION_REGEX = re.compile(r"(<@!?(\d{17,19})>)")


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: Message):

        if not msg.content.lower().startswith("f!"):
            return

        command, *args = msg.content.split()
        action = command[2:]
        if actions.get(action) is None:
            return

        user = msg.author.display_name
        receivers = self._get_receivers(msg, " ".join(args))

        if receivers is None:
            return await msg.channel.send(f"**{user}** {action}s themself!")

        reply = choice(actions[action])
        await msg.channel.send(reply.format(user=user, receivers=receivers))

    @staticmethod
    def _get_receivers(msg: Message, phrase: str) -> Optional[str]:
        # made in a way to easily convert to snek
        if not phrase:
            if msg.reference and isinstance(msg.reference.resolved, Message):
                return f"**{msg.reference.resolved.author.display_name}**"
            else:
                return None

        mentions = re.findall(MENTION_REGEX, phrase)

        if not mentions:
            return phrase

        # transform to Member objects
        mentions: list[Member] = [msg.guild.get_member(int(id)) for _, id in mentions]

        mention_string = ""
        for (idx, men) in enumerate(mentions):
            men_name = men.display_name

            if idx == 0:
                mention_string += f"**{men_name}**"
            elif idx == len(mentions) - 1:
                mention_string += f" and **{men_name}**"
            else:
                mention_string += f", **{men_name}**"

        return mention_string

    @staticmethod
    async def __process_action(ctx: commands.Context, action_name: str, args):
        mentions = ctx.message.mentions
        author_name = ctx.author.nick or ctx.author.name
        main_action = ""

        if len(mentions) == 0:
            if len(args) == 0:
                main_action = f"{action_name}s themselves!"
            else:
                receivers = f"**{args}**"
                main_action = get_main_action(action_name, receivers)
        else:
            mention_string = ""
            for (idx, men) in enumerate(mentions):
                men_name = men.nick or men.name

                if idx == 0:
                    mention_string += f"**{men_name}**"
                elif idx == len(mentions) - 1:
                    mention_string += f" and **{men_name}**"
                else:
                    mention_string += f", **{men_name}**"

            main_action = get_main_action(action_name, mention_string)

        response = f"**{author_name}** {main_action}"
        await ctx.send(response)


def get_main_action(action_name, receivers):
    action_list = text_actions[action_name]
    ran = randint(0, len(action_list) - 1)
    current_action = action_list[ran]
    return current_action.replace("{{receivers}}", receivers)


def setup(bot):
    bot.add_cog(Actions(bot))
