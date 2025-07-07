import asyncio
import aiosqlite
import time

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database
    """
    print("Starting async_fetch_users...")
    start_time = time.time()
    
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
    
    end_time = time.time()
    print(f"async_fetch_users completed in {end_time - start_time:.2f} seconds")
    print(f"Found {len(results)} users")
    
    return results

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database
    """
    print("Starting async_fetch_older_users...")
    start_time = time.time()
    
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
    
    end_time = time.time()
    print(f"async_fetch_older_users completed in {end_time - start_time:.2f} seconds")
    print(f"Found {len(results)} users older than 40")
    
    return results

async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather()
    """
    print("=== Starting concurrent database queries ===")
    start_time = time.time()
    
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    end_time = time.time()
    print(f"\n=== Concurrent execution completed in {end_time - start_time:.2f} seconds ===")
    
    # Display results
    print("\nAll Users:")
    for user in all_users:
        print(f"  {user}")
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(f"  {user}")
    
    return all_users, older_users

# Additional function to demonstrate the performance difference
async def fetch_sequentially():
    """
    Execute queries sequentially for comparison
    """
    print("\n=== Starting sequential database queries ===")
    start_time = time.time()
    
    # Execute queries one after another
    all_users = await async_fetch_users()
    older_users = await async_fetch_older_users()
    
    end_time = time.time()
    print(f"=== Sequential execution completed in {end_time - start_time:.2f} seconds ===")
    
    return all_users, older_users

async def main():
    """
    Main function to demonstrate both concurrent and sequential execution
    """
    print("Demonstrating concurrent vs sequential database queries\n")
    
    # Run concurrent queries
    await fetch_concurrently()
    
    # Run sequential queries for comparison
    await fetch_sequentially()

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())