import sqlite3
import os
from typing import Dict, List, Any

class PaymentDB:
    def __init__(self, db_name="payments.db"):
        # Configure database path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "data", db_name)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database tables
        self._init_db()

    def _init_db(self):
        ''' Create database tables if they don't exist '''
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # table 1
            # Persons table stores unique names
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
                ''')

            # table 2
            # Group table stores group id
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
                ''') 

            # table 3 
            # Payments table stores transaction history
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    time TEXT NOT NULL,
                    FOREIGN KEY(person_id) REFERENCES Persons(id) ON DELETE CASCADE,
                    FOREIGN KEY(group_id) REFERENCES Groups(id) ON DELETE CASCADE
                )
                ''')

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ----- GROUP CRUD ---------------------------------------
    def get_group_id(self, name: str) -> int:
        ''' use group name to find the group id '''
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM Groups WHERE name = ?",
                (name,)
            )
            row = cur.fetchone()
            if row:
                return row[0];
            raise RuntimeError(f"no group found with name {name!r}")

    def create_group(self, name: str) -> int:
        ''' returns the new group id '''
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Groups (name) VALUES (?)",
                (name, )
            )
            return cur.lastrowid

    def list_groups(self) -> List[Dict[str, Any]]:
        """
        Retrieve all groups from the database.

        Returns:
            A list of dictionaries, each containing:
                - 'id' (int): The unique ID of the group.
                - 'name' (str): The name of the group.
        Example:
            [
                {"id": 1, "name": "Friends"},
                {"id": 2, "name": "Family"}
            ]
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name FROM Groups"
            )
            return [{"id": r[0], "name": r[1]} for r in cur.fetchall()]

    def get_group(self, group_id: int) -> Dict[str, Any]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name FROM Groups WHERE id = ?",
                (group_id, )
            )
            row = cur.fetchone()
            if row:
                return {"id": row[0], "name": row[1]}
            raise RuntimeError(f"No group found with id {group_id}")
            
    def rename_group(self, group_id: int, new_name: str) -> Dict[str, Any]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE Groups SET name = ? WHERE id = ?",
                (new_name, group_id)
            )
            if cur.rowcount:
                return {"id": group_id, "name": new_name}
            raise RuntimeError(f"No group found with id {group_id}")

    def remove_group(self, group_id: int) -> None: 
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM Groups WHERE id = ?",
                (group_id,)
            )
            if cur.rowcount == 0:
                raise RuntimeError(f"No group found with id {group_id}")


    # --------- Payments CRUD ---------------------------------
    def insert(self, name: str, group: str, amount: float, time: str) -> int:
        """
        Store a new payment in the database, ensuring person and group exist.
        
        Args:
            name (str): Name of the payer.
            group (str): Name of the group.
            amount (float): Amount paid.
            time (str): Timestamp of the payment.
        
        Returns:
            int: The ID of the newly inserted payment record.
        """
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("INSERT OR IGNORE INTO Persons (name) VALUES (?)", (name,))
                cur.execute("INSERT OR IGNORE INTO Groups (name) VALUES (?)", (group,))
                # Get person_id
                cur.execute("SELECT id FROM Persons WHERE name = ?", (name,))
                person_id = cur.fetchone()[0]
                # Get group_id
                cur.execute("SELECT id FROM Groups WHERE name = ?", (group,))
                group_id = cur.fetchone()[0]
                # Insert payment
                cur.execute(
                    "INSERT INTO Payments (person_id, group_id, amount, time) VALUES (?, ?, ?, ?)",
                    (person_id, group_id, amount, time)
                )
                return cur.lastrowid
        except sqlite3.Error as e:
            raise RuntimeError(f"insert error: {e}")
             

    def remove_payment(self, payment_id: int) -> None:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM Payments WHERE id = ?", 
                (payment_id, )
            )
            if cur.rowcount == 0:
                raise RuntimeError(f"No group found with id {payment_id}")
            

    def get_all_payments(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieve all payments, grouped by group name.
        
        Returns:
            A dictionary where each key is a group name and the value is a list of
            payment records for that group. Each record contains:
                - 'person' (str): Payer's name.
                - 'amount' (float): Amount paid.
                - 'time' (str): Timestamp of the payment.
        """
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT g.name, p.name, pm.amount, pm.time
                    FROM Payments pm
                    JOIN Persons p ON pm.person_id = p.id
                    JOIN Groups g ON pm.group_id = g.id
                    ORDER BY g.name, pm.time
                """)
                rows = cur.fetchall()
                result: Dict[str, List[Dict[str, Any]]] = {}
                for group_name, person, amount, time in rows:
                    result.setdefault(group_name, []).append({
                        "person": person,
                        "amount": amount,
                        "time": time
                    })
                return result
        except sqlite3.Error as e:
            raise RuntimeError(f"Database query failed: {e}")
    
    

    
# test
# if __name__ == "__main__":
#     db = PaymentDB()

#     # Fetch all payments
#     all_payments = db.get_all_payments()

#     # Display groups and payment information
#     for group_name, records in all_payments.items():
#         print(f"Group: {group_name}")
#         total_amount = sum(record["amount"] for record in records)
#         print(f"  Total amount: {total_amount:.2f}")
        
#         # Calculate each person's total
#         person_totals = {}
#         for record in records:
#             person = record["person"]
#             person_totals[person] = person_totals.get(person, 0) + record["amount"]
        
#         for person, amount in person_totals.items():
#             print(f"    {person}: {amount:.2f}")
