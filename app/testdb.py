from models import storage
from models.user import User

# Reload the database and get session ready
storage.reload()

# Create sample users
user1 = User(
    email="alice@example.com",
    phone="0700123456",
    password_hash="hashed_password_1",
    first_name="Alice",
    last_name="Mwangi",
    location="Nairobi",
    role="user"
)

user2 = User(
    email="bob@example.com",
    phone="0711223344",
    password_hash="hashed_password_2",
    first_name="Bob",
    last_name="Omondi",
    location="Kisumu",
    role="admin"
)

# Add to session and save to DB
storage.new(user1)
storage.new(user2)
storage.save()

# Optional: print to confirm
print("Users added:")
for user in [user1, user2]:
    print(user.to_dict())
