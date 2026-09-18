"""
THEARA COLOR — Transactional Credit Management Service
Founder: Krai Theara | "Create Your Look"
"""

import uuid
from typing import Tuple, Optional, List, Dict, Any
from app.db.database import get_db
from app.core.config import settings


class CreditService:
    """
    Handles atomic deduction, refunding, and tracking of generation credits.
    Guarantees concurrency safety using database transactions.
    """

    @classmethod
    def get_balance(cls, user_id: str) -> Dict[str, Any]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT balance, lifetime_used FROM credits WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            # Create starting balance
            cursor.execute(
                "INSERT INTO credits (user_id, balance, lifetime_used) VALUES (?, ?, ?)",
                (user_id, settings.PLAN_CREDITS["free"], 0)
            )
            conn.commit()
            balance, used = settings.PLAN_CREDITS["free"], 0
        else:
            balance, used = row["balance"], row["lifetime_used"]
        conn.close()
        return {"balance": balance, "lifetime_used": used}

    @classmethod
    def deduct_credits(
        cls,
        user_id: str,
        amount: int,
        action: str,
        reference_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Atomically checks balance and deducts credits.
        Returns (success, message).
        """
        if amount <= 0:
            return True, "No charge"

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("SELECT balance, lifetime_used FROM credits WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if not row or row["balance"] < amount:
                conn.rollback()
                return False, "Insufficient credits for this operation"

            new_balance = row["balance"] - amount
            new_used = row["lifetime_used"] + amount
            cursor.execute(
                "UPDATE credits SET balance = ?, lifetime_used = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (new_balance, new_used, user_id)
            )

            tx_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO credit_transactions (id, user_id, amount, action, reference_id, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tx_id, user_id, -amount, action, reference_id, description or f"Consumed {amount} credits for {action}"))

            conn.commit()
            return True, "Credits deducted successfully"
        except Exception as e:
            conn.rollback()
            return False, f"Credit deduction error: {str(e)}"
        finally:
            conn.close()

    @classmethod
    def refund_credits(
        cls,
        user_id: str,
        amount: int,
        reference_id: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> bool:
        """
        Refunds credits if generation fails downstream.
        """
        if amount <= 0:
            return True

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("SELECT balance, lifetime_used FROM credits WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                new_balance = row["balance"] + amount
                new_used = max(0, row["lifetime_used"] - amount)
                cursor.execute(
                    "UPDATE credits SET balance = ?, lifetime_used = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (new_balance, new_used, user_id)
                )

                tx_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO credit_transactions (id, user_id, amount, action, reference_id, description)
                    VALUES (?, ?, ?, 'refund', ?, ?)
                """, (tx_id, user_id, amount, reference_id, reason or "Refund for failed generation"))

                conn.commit()
                return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()
        return False

    @classmethod
    def get_transactions(cls, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM credit_transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        result = [dict(r) for r in rows]
        conn.close()
        return result

