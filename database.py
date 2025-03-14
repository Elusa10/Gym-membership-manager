from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from models import Member, Membership, Trainer, MemberTrainer, Transaction


DATABASE_URL = 'sqlite:///gym.db'
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)

session = SessionLocal()


def get_session():
    """Returns a new database session."""
    return SessionLocal()


def assign_membership(session):
    """Assign a membership to an existing member."""
    member_id = input("Enter Member ID: ")
    membership_id = input("Enter Membership ID: ")
    
    member = session.query(Member).filter_by(id=member_id).first()
    membership = session.query(Membership).filter_by(id=membership_id).first()
    
    
    if not member:
        print("❌ Member not found!")
        return
    if not membership:
        print("❌ Membership not found!")
        return
    
    member.membership_id = membership.id
    session.commit()
    print(f"✅ Membership '{membership.type}' assigned to {member.name}!")

def list_memberships(session: Session):
    memberships = session.query(Membership).all()
    for membership in memberships:
        print(f"ID: {membership.id}, Type: {membership.type}, Price: {membership.price}")




def change_membership(session):
    """Upgrade or downgrade a member's membership."""
    member_id = input("Enter Member ID: ")
    member = session.query(Member).filter_by(id=member_id).first()

    if not member:
        print("❌ Member not found!")
        return
    
    if not member.membership:
        print("❌ This member has no active membership!")
        return
    
    membership_types = ["Basic", "Standard", "Premium"]
    current_type = member.membership.type

    print(f"Current Membership: {current_type}")
    action = input("Would you like to (U)pgrade or (D)owngrade? ").strip().lower()

    if action == "u":  # Upgrade
        if current_type == "Premium":
            print("❌ Already at the highest membership!")
        else:
            new_type = membership_types[membership_types.index(current_type) + 1]
            new_membership = session.query(Membership).filter_by(type=new_type).first()
            member.membership_id = new_membership.id
            session.commit()
            print(f"✅ Upgraded to {new_type}!")

    elif action == "d":  # Downgrade
        if current_type == "Basic":
            print("❌ Already at the lowest membership!")
        else:
            new_type = membership_types[membership_types.index(current_type) - 1]
            new_membership = session.query(Membership).filter_by(type=new_type).first()
            member.membership_id = new_membership.id
            session.commit()
            print(f"✅ Downgraded to {new_type}!")

    else:
        print("❌ Invalid input! Please enter 'U' for Upgrade or 'D' for Downgrade.")


def cancel_membership(session):
    """Cancel a member's active membership."""
    member_id = input("Enter Member ID: ")
    member = session.query(Member).filter_by(id=member_id).first()

    if not member:
        print("❌ Member not found!")
        return
    
    if not member.membership:
        print("❌ This member has no active membership to cancel!")
        return
    
    print(f"Current Membership: {member.membership.type}")
    confirm = input("Are you sure you want to cancel this membership? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        member.membership_id = None  # Remove membership assignment
        session.commit()
        print("✅ Membership has been canceled successfully!")
    else:
        print("❌ Action canceled.")

def view_active_members(session):
    """Display members with an active membership."""
    active_members = session.query(Member).filter(Member.membership_id.isnot(None)).all()

    if not active_members:
        print("❌ No active members found!")
        return
    
    print("\n🔹 Active Members 🔹")
    print("-" * 40)
    for member in active_members:
        print(f"ID: {member.id} | Name: {member.name} | Membership: {member.membership.type}")
    print("-" * 40)

def view_expired_members(session):
    """Display members without a membership (expired)."""
    expired_members = session.query(Member).filter(Member.membership_id.is_(None)).all()

    if not expired_members:
        print("✅ No expired memberships found! All members have an active membership.")
        return
    
    print("\n🔹 Expired Memberships 🔹")
    print("-" * 40)
    for member in expired_members:
        print(f"ID: {member.id} | Name: {member.name}")
    print("-" * 40)


def generate_revenue_report(session):
    """Generate and display total revenue from memberships."""
    # Get revenue breakdown by membership type
    revenue_data = (
        session.query(
            Membership.type,
            func.count(Member.id).label("member_count"),
            func.sum(Membership.price).label("total_revenue")
        )
        .join(Member, Membership.id == Member.membership_id)
        .group_by(Membership.type)
        .all()
    )

    if not revenue_data:
        print("❌ No active memberships found. No revenue generated!")
        return

    print("\n💰 Gym Revenue Report 💰")
    print("-" * 50)
    total_revenue = 0
    for membership_type, member_count, revenue in revenue_data:
        print(f"Membership: {membership_type}")
        print(f" - Members: {member_count}")
        print(f" - Revenue: ${revenue:.2f}\n")
        total_revenue += revenue

    print("=" * 50)
    print(f"🔥 Total Revenue: ${total_revenue:.2f}")
    print("=" * 50)


def display_members_per_trainer(session):
    """Show members assigned to each trainer based on trainer-member assignments."""
    trainers = session.query(Trainer).all()

    if not trainers:
        print("❌ No trainers found!")
        return

    print("\n👨‍🏫 Members Assigned to Trainers 👨‍🏫")
    print("-" * 50)

    for trainer in trainers:
        print(f"\n🔹 Trainer: {trainer.name} | Specialty: {trainer.specialty}")

        # Get members assigned to this trainer
        assigned_members = (
            session.query(Member)
            .join(MemberTrainer, Member.id == MemberTrainer.member_id)
            .filter(MemberTrainer.trainer_id == trainer.id)
            .all()
        )

        if not assigned_members:
            print("   ❌ No members assigned to this trainer.")
        else:
            for member in assigned_members:
                print(f"   - {member.name} (Email: {member.email})")

    print("-" * 50)

def add_membership(session, membership_type, price):
    """Adds a new membership with validation."""
    valid_membership_types = ["Basic", "Standard", "Premium"]

    if membership_type not in valid_membership_types:
        print(f"❌ Invalid membership type: {membership_type}. Choose from: {', '.join(valid_membership_types)}")
        return 

    new_membership = Membership(type=membership_type, price=price)
    session.add(new_membership)
    session.commit()
    print(f"✅ Membership '{membership_type}' added successfully!")

def assign_transaction(session):
    """Assign a transaction to an existing member."""
    member_id = input("Enter Member ID: ")
    amount = input("Enter Transaction Amount: ")
    
    member = session.query(Member).filter_by(id=member_id).first()
    
    if not member:
        print("❌ Member not found!")
        return
    
    transaction = Transaction(member_id=member.id, amount=amount)
    session.add(transaction)
    session.commit()
    
    print(f"✅ Transaction of ${amount} assigned to {member.name}!")



def assign_trainer_to_member(session, member_id, trainer_id):
    """Assign a trainer to a member after validation."""
    member = session.query(Member).filter_by(id=member_id).first()
    trainer = session.query(Trainer).filter_by(id=trainer_id).first()

    if not member:
        print("❌ Member not found! Please enter a valid member ID.")
        return

    if not trainer:
        print("❌ Trainer not found! Please enter a valid trainer ID.")
        return

    # Check if this trainer is already assigned to the member
    existing_assignment = (
        session.query(MemberTrainer)
        .filter_by(member_id=member_id, trainer_id=trainer_id)
        .first()
    )

    if existing_assignment:
        print("⚠️ This trainer is already assigned to this member!")
        return

    new_assignment = MemberTrainer(member_id=member_id, trainer_id=trainer_id)
    session.add(new_assignment)
    session.commit()
    print(f"✅ Successfully assigned Trainer {trainer.name} to Member {member.name}.")






