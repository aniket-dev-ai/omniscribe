import asyncio
import os
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_dir = current_dir.parent  # backend/src/db

if str(db_dir) not in sys.path:
    sys.path.insert(0, str(db_dir)) 
    
from connection import get_supabase_client

# CREATE
async def insert_user(email, name, role):
    supabase = get_supabase_client()
    payload = {"email": email, "name": name, "role": role}
    try:
        res = supabase.table("users").insert(payload).execute()
        if getattr(res, "error", None):
            print(f"Failed to insert user {name}")
            return False
        if res.data:
            print(f"User {name} inserted successfully.")
            return True
        print(f"Failed to insert user {name}.")
        return False
    except Exception as e:
        print(f"Error inserting user {name}: {e}")
        return False


# READ ALL
async def get_all_users():
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").select("*").execute()
        if getattr(res, "error", None):
            print("Failed to fetch users.")
            return None
        return res.data
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None


# READ ONE
async def get_user_by_email(email):
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").select("*").eq("email", email).execute()
        if getattr(res, "error", None):
            print(f"Failed to fetch user {email}.")
            return None
        if res.data:
            return res.data[0]
        print(f"No user found with email {email}.")
        return None
    except Exception as e:
        print(f"Error fetching user {email}: {e}")
        return None


# UPDATE
async def update_user(email, updates: dict):
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").update(updates).eq("email", email).execute()
        if getattr(res, "error", None):
            print(f"Failed to update user {email}.")
            return False
        if res.data:
            print(f"User {email} updated successfully.")
            return True
        print(f"No user found with email {email} to update.")
        return False
    except Exception as e:
        print(f"Error updating user {email}: {e}")
        return False


# DELETE
async def delete_user(email):
    supabase = get_supabase_client()
    try:
        res = supabase.table("users").delete().eq("email", email).execute()
        if getattr(res, "error", None):
            print(f"Failed to delete user {email}.")
            return False
        if res.data:
            print(f"User {email} deleted successfully.")
            return True
        print(f"No user found with email {email} to delete.")
        return False
    except Exception as e:
        print(f"Error deleting user {email}: {e}")
        return False
    
    
async def main():
    # Create
    await insert_user("alice@example.com", "Alice", "admin")

    # Read all
    users = await get_all_users()

    # # Read one
    # user = await get_user_by_email("alice@example.com")

    # # Update
    # await update_user("alice@example.com", {"role": "editor", "name": "Alice B."})

    # # Delete
    # await delete_user("alice@example.com")
    
    print(users)
if __name__ == "__main__":
    asyncio.run(main())