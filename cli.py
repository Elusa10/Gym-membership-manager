import click
from database import get_session
from models import Member, Membership, Trainer, Transaction
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from database import (
    session, assign_membership, change_membership, cancel_membership, 
    view_active_members, view_expired_members, generate_revenue_report, 
    display_members_per_trainer, add_membership, assign_trainer_to_member, list_memberships, SessionLocal
)

engine = create_engine("sqlite:///gym.db")  # Adjust for your actual database
Session = sessionmaker(bind=engine)
session = Session()

def create_member(name, email, membership_id):
    session = get_session()
    member = Member(name=name, email=email, membership_id=membership_id)
    session.add(member)
    session.commit()
    session.close()
    click.echo(f"Member '{name}' added successfully!")

def list_members():
    session = get_session()
    members = session.query(Member).all()
    session.close()
    if members:
        for member in members:
            click.echo(f"ID: {member.id}, Name: {member.name}, Email: {member.email}, Membership ID: {member.membership_id}")
    else:
        click.echo("No members found.")

def delete_member(member_id):
    member = session.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        print("Member not found!")
        return

    
    default_member_id = 0
    session.query(Transaction).filter(Transaction.member_id == member_id).update({"member_id": default_member_id})

    session.delete(member)
    session.commit()
    print(f"Member {member_id} removed successfully!")


def create_trainer(name, specialty):
    session = get_session()
    trainer = Trainer(name=name, specialty=specialty)
    session.add(trainer)
    session.commit()
    session.close()
    click.echo(f"Trainer '{name}' added successfully!")

def list_trainers():
    session = get_session()
    trainers = session.query(Trainer).all()
    session.close()
    if trainers:
        for trainer in trainers:
            click.echo(f"ID: {trainer.id}, Name: {trainer.name}, Specialty: {trainer.specialty}")
    else:
        click.echo("No trainers found.")


@click.group()
def cli():
    """Gym Membership CLI"""
    pass

@cli.command(name="assign-membership")
@click.option("--member-id", prompt="Member ID", type=int, help="Enter the member's ID.")
@click.option("--membership-id", prompt="Membership ID", type=int, help="Enter the membership ID.")
def assign_membership_cli(member_id, membership_id):
    with Session() as session:
        # Fetch member and membership within the same session
        member = session.query(Member).filter_by(id=member_id).first()
        membership = session.query(Membership).filter_by(id=membership_id).first()

        if not member:
            click.echo(f"Member with ID {member_id} not found.")
            return
        
        if not membership:
            click.echo(f"Membership with ID {membership_id} not found.")
            return

        # Assign membership
        member.membership_id = membership.id
        session.commit()
        click.echo(f"Assigned membership {membership_id} to member {member_id}.")



@cli.command(name="change-membership")
def change_membership_cli():
    """Change a member's membership."""
    session = get_session()  
    change_membership(session) 

@cli.command(name="cancel-membership")
def cancel_membership_cli():
    """Cancel a member's membership."""
    session = get_session()
    cancel_membership(session)

@cli.command(name="view-active-members")
def view_active_members_cli():
    """View all active members."""
    session = get_session()
    view_active_members(session)

@cli.command(name="view-expired-members")
def view_expired_members_cli():
    """View all expired members."""
    session = get_session()
    view_expired_members(session)

@cli.command(name="generate-revenue-report")
def generate_revenue_report_cli():
    """Generate a revenue report."""
    session = get_session()
    generate_revenue_report(session)

@cli.command(name="view-members-per-trainer")
def display_members_per_trainer_cli():
    """Display the number of members assigned to each trainer."""
    session = get_session()
    display_members_per_trainer(session)

@cli.command(name="add-membership")
@click.option("--type", prompt="Membership Type (Basic, Standard, Premium)", help="Enter membership type.")
@click.option("--price", prompt="Price", type=float, help="Enter membership price.")
def add_membership_cli(type, price):
    """CLI command to add a membership."""
    valid_types = {"Basic", "Standard", "Premium"} 
    
    if type not in valid_types:
        click.echo(f"❌ Error: '{type}' is not a valid membership type. Choose from: Basic, Standard, Premium.")
        return  # Stop execution if invalid
    
    session = get_session()
    add_membership(session, type, price)
    session.close()
    click.echo(f"✅ Membership '{type}' added successfully!")
    click.echo(f"Price: ${price:.2f}")

@cli.command(name="assign-trainer")
@click.option("--member-id", prompt="Member ID", type=int, help="Enter the member's ID.")
@click.option("--trainer-id", prompt="Trainer ID", type=int, help="Enter the trainer's ID.")
def assign_trainer_cli(member_id, trainer_id):
    """Assign a trainer to a member."""
    session = get_session()
    member = session.query(Member).filter_by(id=member_id).first()
    trainer = session.query(Trainer).filter_by(id=trainer_id).first()

    if not member:
        click.echo(f"❌ Member with ID {member_id} not found.")
        return
    if not trainer:
        click.echo(f"❌ Trainer with ID {trainer_id} not found.")
        return

    assign_trainer_to_member(session, member_id, trainer_id)
    session.close()
    click.echo(f"✅ Trainer '{trainer.name}' assigned to Member '{member.name}'!")

@cli.command()
@click.option('--name', prompt='Member name', help='Name of the member')
@click.option('--email', prompt='Member email', help='Email of the member')
@click.option('--membership_id', type=int, prompt='Membership ID', help='ID of the membership')
def add_member(name, email, membership_id):
    """Add a new gym member."""
    create_member(name, email, membership_id)

@cli.command()
def view_members():
    """List all gym members."""
    list_members()

@cli.command()
@click.option('--member_id', type=int, prompt='Member ID', help='ID of the member to delete')
def remove_member(member_id):
    """Delete a gym member by ID."""
    delete_member(member_id)


@cli.command()
def view_memberships():
    """List all memberships."""
    session = SessionLocal()
    try:
        list_memberships(session)
    finally:
        session.close()

@cli.command()
@click.option('--name', prompt='Trainer name', help='Name of the trainer')
@click.option('--specialty', prompt='Trainer specialty', help='Trainer specialty (e.g., Cardio, Strength, Yoga)')
def add_trainer(name, specialty):
    """Add a new trainer."""
    create_trainer(name, specialty)

@cli.command()
def view_trainers():
    """List all trainers."""
    list_trainers()

if __name__ == '__main__':
    cli()
