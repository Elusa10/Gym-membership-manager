**Gym Management CLI**

This is a Command Line Interface (CLI) application for managing gym memberships, trainers, and transactions using Python and SQLAlchemy.

**Features**

. Add new members, trainers, and memberships.

. Update or delete existing records.

. Change member memberships (upgrade/downgrade).

. Assign trainers to members.

. Record transactions for membership payments.

**Technologies Used**

. *Python* (CLI implementation)

. *Click* (Command-line interaction)

. *SQLAlchemy* (Database ORM)

. *SQLite* (Database storage)


**Installation**

1. *Clone the Repository*

git clone https://github.com/Elusa10/Gym-membership-manager.git
cd gym-management-cli

2. *Create and Activate a Virtual Environment*

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

3. *Install Dependencies*

pip install -r requirements.txt

4. *Set Up the Database*

python setup_db.py

This initializes the database and creates the necessary tables.


**Usage**

Run the CLI using:

python cli.py <command>

**Available Commands**

1. *Add a Member*

python cli.py add-member

2. *Add a Trainer*

python cli.py add-trainer

3. *Assign a Trainer to a Member*

python cli.py assign-trainer

4. *Change Membership (Upgrade/Downgrade)*

python cli.py change-membership

5. *Record a Transaction*

python cli.py record-transaction

6. *View All Members*

python cli.py view-members


**Troubleshooting**

ValueError: 'Basic' is not in list

This error occurs if the membership type is missing from the predefined list. Ensure that membership_types contains all expected membership levels:

membership_types = ["Basic", "Silver", "Gold", "Platinum"]

**Database Errors**

If you encounter database errors, reset the database:

python setup_db.py

**Contributing**

Fork the repository.

Create a new branch (git checkout -b feature-name).

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature-name).

Open a Pull Request.

**License**

This project is licensed under the MIT License.

