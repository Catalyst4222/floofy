from random import randint
from discord.ext import commands
from utilities.actions_config import text_actions


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["pat"])
    async def pet(self, ctx: commands.Context, *args):
        await self.__process_action(ctx, "pet", " ".join(args))

    @commands.command(pass_context=True)
    async def boop(self, ctx: commands.Context, *args):
        await self.__process_action(ctx, "boop", " ".join(args))

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
