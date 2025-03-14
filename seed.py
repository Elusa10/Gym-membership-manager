from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from database import engine, Member, Trainer, Membership, MemberTrainer, Transaction


fake = Faker()

Session = sessionmaker(bind=engine)
session = Session()


session.query(MemberTrainer).delete()
session.query(Transaction).delete()
session.query(Member).delete()
session.query(Trainer).delete()
session.query(Membership).delete()
session.commit()


membership_types = [
    {"type": "Basic", "price": 2000},
    {"type": "Standard", "price": 3500},
    {"type": "Premium", "price": 5000}
]


memberships = []
for m in membership_types:
    membership = Membership(type=m["type"], price=m["price"])
    session.add(membership)
    memberships.append(membership)

session.commit()


trainer_specialties = ["Strength Training", "Cardio", "Yoga", "CrossFit", "Bodybuilding"]
trainers = []
for _ in range(5):
    trainer = Trainer(name=fake.name(), specialty=random.choice(trainer_specialties))
    session.add(trainer)
    trainers.append(trainer)

session.commit()


members = []
for _ in range(15):  
    member = Member(
        name=fake.name(),
        email=fake.email(),
        membership_id=random.choice(memberships).id
    )
    session.add(member)
    members.append(member)

session.commit()


for member in members:
    assigned_trainer = random.choice(trainers)
    member_trainer = MemberTrainer(member_id=member.id, trainer_id=assigned_trainer.id)
    session.add(member_trainer)

session.commit()

# Generate transactions for revenue tracking
for _ in range(20):
    transaction = Transaction(
        member_id=random.choice(members).id,
        amount=random.choice([2000, 3500, 5000]),  # Membership prices
        date=fake.date_this_year()
    )
    session.add(transaction)

session.commit()

print("Database successfully seeded with memberships, members, trainers, assignments, and transactions!")
session.close()
