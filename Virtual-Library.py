from database import *
from interactions.ext.get import get
import interactions
from discord.ext import commands
from requests.structures import CaseInsensitiveDict
import re

test_guild_id = 0
Role_employee_id = 0

bot = interactions.Client(token="😏")

@bot.command(
    name="book-registration",
    description="Registering a book in the library",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="isbn",
            description="ISBN book",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="bookcase",
            description="In which bookcase does the book lie",
            type=interactions.OptionType.STRING,
            required=True,
            focused = True,
            choices=[
                interactions.Choice(name="Bookcase №1", value="1"),
                interactions.Choice(name="Bookcase №2", value="2"),
                interactions.Choice(name="Bookcase №3", value="3"),
                interactions.Choice(name="Bookcase №4", value="4"),
                interactions.Choice(name="Bookcase №5", value="5"),
            ] 
        ),
        interactions.Option(
            name="bookshelf",
            description="Which bookshelf does the book lie on?",
            type=interactions.OptionType.STRING,
            required=True,
            focused = True,
            choices=[
                interactions.Choice(name="Bookshelf №1", value="1"),
                interactions.Choice(name="Bookshelf №2", value="2"),
                interactions.Choice(name="Bookshelf №3", value="3"),
                interactions.Choice(name="Bookshelf №4", value="4"),
                interactions.Choice(name="Bookshelf №5", value="5"),
                interactions.Choice(name="Bookshelf №6", value="6"),
                interactions.Choice(name="Bookshelf №7", value="7"),
                interactions.Choice(name="Bookshelf №8", value="8"),
            ] 
        ),

    ],
)
async def book_registration(ctx: interactions.CommandContext, isbn: str, bookcase: int, bookshelf: int):
    if Role_employee_id in ctx.author.roles:
        db_check = Library.get_or_skip(bookcase = bookcase, bookshelf=bookshelf )
        if db_check != None:
            await ctx.send(f"There is already a book on this shelf.", ephemeral=True)
            return
        db_check = Library.get_or_skip(ISBN = re.sub("[^0-9]", "", isbn))
        if db_check != None:
            await ctx.send(f"Such a book is already in the system.\nThe address of the book is: `Bookcase №{db_check.bookcase}, Bookshelf №{db_check.bookshelf}` ", ephemeral=True)
            return
        db_library = Library()
        db_library.ISBN = re.sub("[^0-9]", "", isbn)
        db_library.bookcase = bookcase
        db_library.bookshelf = bookshelf
        db_library.save()
        await ctx.send(f"The book has been added to the registration system. \nThe address of the book is: `Bookcase №{bookcase}, Bookshelf №{bookshelf}`", ephemeral=True)
    else:
        await ctx.send(f"You are not a library employee.", ephemeral=True)

@bot.command(
    name="book-search",
    description="Find a book by ISBN",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="isbn",
            description="ISBN book",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ],
)
async def book_registration(ctx: interactions.CommandContext, isbn: str):
    if Role_employee_id in ctx.author.roles:
        db_check = Library.get_or_skip(ISBN = re.sub("[^0-9]", "", isbn))
        if db_check != None:
            db_check_taken = TakenBooks.get_or_skip(ISBN = db_check.id, retrieved = False)
            if db_check_taken != None:
                await ctx.send(f"<@{db_check_taken.whotook}> has this book at the moment.", ephemeral=True)
                return
            await ctx.send(f"The book was found.\nThe address of the book is: `Bookcase №{db_check.bookcase}, Bookshelf №{db_check.bookshelf}` ", ephemeral=True)
            return
        await ctx.send(f"There is no book with this ISBN in the system", ephemeral=True)
    else:
        await ctx.send(f"You are not a library employee.", ephemeral=True)

@bot.command(
    name="issue-book",
    description="Issue a book to a person",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="isbn",
            description="ISBN book",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="whom",
            description="To whom do you give the book",
            type=interactions.OptionType.USER,
            required=True, ),
    ],
)
async def issue_book(ctx: interactions.CommandContext, isbn: str, whom: str):
    if Role_employee_id in ctx.author.roles:
        db_check = Library.get_or_skip(ISBN = re.sub("[^0-9]", "", isbn))
        if db_check == None:
            await ctx.send(f"There is no book with this ISBN in the system", ephemeral=True)
            return
        db_check_taken = TakenBooks.get_or_skip(ISBN = db_check.id, retrieved = False)
        if db_check_taken != None:
            await ctx.send(f"<@{db_check_taken.whotook}> has already taken this book", ephemeral=True)
            return
        db_takenbooks = TakenBooks()
        db_takenbooks.ISBN = db_check
        db_takenbooks.retrieved = False
        db_takenbooks.whotook = whom.id
        db_takenbooks.save()
        await ctx.send(f"The book was given to <@{db_takenbooks.whotook}>", ephemeral=True)
    else:
        await ctx.send(f"You are not a library employee.", ephemeral=True)

@bot.command(
    name="get-book",
    description="Get the book from the persona",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="isbn",
            description="ISBN book",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def get_book(ctx: interactions.CommandContext, isbn: str,):
    if Role_employee_id in ctx.author.roles:
        db_check = Library.get_or_skip(ISBN = re.sub("[^0-9]", "", isbn))
        if db_check == None:
            await ctx.send(f"There is no book with this ISBN in the system", ephemeral=True)
            return
        db_check_taken = TakenBooks.get_or_skip(ISBN = db_check.id, retrieved = False)
        if db_check_taken == None:
            await ctx.send(f"This book should be in the bookcase\nThe address of the book is: `Bookcase №{db_check.bookcase}, Bookshelf №{db_check.bookshelf}`", ephemeral=True)
            return
        db_check_taken.retrieved = True
        db_check_taken.save()
        await ctx.send(f"The book is back in the library. Please put it in the address: `Bookcase №{db_check.bookcase}, Bookshelf №{db_check.bookshelf}`", ephemeral=True)
    else:
        await ctx.send(f"You are not a library employee.", ephemeral=True)

bot.start()