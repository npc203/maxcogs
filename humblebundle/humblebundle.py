import asyncio
import json

import aiohttp
import discord
from redbot.core import commands


class HumbleBundle(commands.Cog):
    """Responds with the currently available Humble Bundles, if any."""

    __author__ = "<@306810730055729152>, MAX"
    __version__ = "1.6.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.command(aliases=["humble"])
    @commands.cooldown(1, 700, commands.BucketType.guild)
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def humblebundle(self, ctx):
        """Responds with the currently available Humble Bundles."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.humblebundle.com/androidapp/v2/service_check"
                ) as response:
                    if response.status == 200:
                        data = json.loads(await response.read())
                    else:
                        return await ctx.send(
                            f"Something went wrong while trying to contact API."
                        )
        except asyncio.TimeoutError:
            return await ctx.send("Connection to Humble Bundle API timed out.")

        items = "".join(
            "**{}. {}:** <{}>\n".format(
                count + 1, bundles.get("bundle_name"), bundles.get("url")
            )
            for count, bundles in enumerate(data)
        )
        if not items:
            await ctx.send("There is currently no available humblebundle.")
            return
        await ctx.send(items)
