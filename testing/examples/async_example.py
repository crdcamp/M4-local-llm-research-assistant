import asyncio

async def fetch_user(user_id):
    await asyncio.sleep(1)  # simulates I/O (DB call, HTTP request, etc.)
    return f"User {user_id}"

async def fetch_orders(user_id):
    await asyncio.sleep(2)
    return f"Orders for user {user_id}"

async def fetch_recommendations(user_id):
    await asyncio.sleep(1.5)
    return f"Recommendations for user {user_id}"

async def main():
    results = await asyncio.gather(
        fetch_user(42),
        fetch_orders(42),
        fetch_recommendations(42),
    )
    print(results)

asyncio.run(main())
