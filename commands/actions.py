from random import randint
from discord.ext import commands
from utilities.actions_config import text_actions


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def pet(self, ctx: commands.Context):
        await self.__process_action(ctx, "pet")

    @commands.command(pass_context=True)
    async def boop(self, ctx: commands.Context):
        await self.__process_action(ctx, "boop")

    @staticmethod
    async def __process_action(ctx: commands.Context, action_name: str):
        mentions = ctx.message.mentions
        author_name = ctx.author.nick or ctx.author.name

        if len(mentions) == 0:
            await ctx.send(f"**{author_name}** {action_name}s themselves!")
        else:
            action_list = text_actions[action_name]
            ran = randint(0, len(action_list) - 1)

            mention_string = ""
            for (idx, men) in enumerate(mentions):
                men_name = men.nick or men.name

                if idx == 0:
                    mention_string += f"**{men_name}**"
                elif idx == len(mentions) - 1:
                    mention_string += f" and **{men_name}**"
                else:
                    mention_string += f", **{men_name}**"

            current_action = action_list[ran]
            main_action = current_action.replace("{{receivers}}", mention_string)

            response = f"**{author_name}** {main_action}"
            await ctx.send(response)


def setup(bot):
    bot.add_cog(Actions(bot))
