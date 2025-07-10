import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    # Run both queries concurrently using asyncio.gather
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return users, older_users

# Example usage
if __name__ == "__main__":
    try:
        # Run the concurrent fetch operation
        results = asyncio.run(fetch_concurrently())
        all_users, older_users = results
        print("All users:", all_users)
        print("Users older than 40:", older_users)
    except Exception as e:
        print(f"Error: {str(e)}")
