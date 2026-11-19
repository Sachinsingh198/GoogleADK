import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from google.adk.tools import ToolContext

# Path to the SQLite database
DB_PATH = Path(__file__).resolve().parent / "campusx.db"


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_refund_policy() -> dict[str, Any]:
    """Get the common refund policy terms and eligibility rules for CampusX courses.

    Returns:
        A dictionary containing the refund window, completion threshold,
        and other policy details.
    """
    return {
        "policy_summary": "CampusX Course Refund Policy",
        "refund_window_days": 7,
        "max_completion_percent": 20.0,
        "eligible_statuses": ["active"],
        "terms": [
            "Refund requests must be made within 7 days of course purchase.",
            "Course completion must be 20% or less.",
            "The enrollment must be active (not already requested for refund or refunded).",
            "Eligible refunds receive a 100% full refund of the amount paid.",
            "Refund requests require student confirmation and will be marked as 'refund_requested' pending processing.",
        ],
    }


def identify_student(email: str, tool_context: ToolContext) -> dict[str, Any]:
    """Look up a student by their registered email address.

    Args:
        email: The email address used to purchase the CampusX course.

    Returns:
        Student information if found, or an error status if not found.
    """
    email_clean = email.strip()
    with _get_connection() as conn:
        cursor = conn.execute(
            "SELECT student_id, name, email FROM students WHERE email = ? COLLATE NOCASE",
            (email_clean,),
        )
        student = cursor.fetchone()

    if not student:
        return {
            "status": "not_found",
            "message": f"No student found with email '{email}'. Please check the email address.",
        }

    # Store in session state for subsequent turns
    tool_context.state["student_email"] = student["email"]
    tool_context.state["student_id"] = student["student_id"]
    tool_context.state["student_name"] = student["name"]

    return {
        "status": "found",
        "student_id": student["student_id"],
        "name": student["name"],
        "email": student["email"],
    }


def get_my_enrollments(
    tool_context: ToolContext,
    student_id: Optional[str] = None,
) -> dict[str, Any]:
    """Get all course enrollments for the currently identified student.

    Args:
        student_id: Optional student ID. If omitted, uses the student identified in the conversation.

    Returns:
        A dictionary containing the list of enrollments with course details.
    """
    sid = student_id or tool_context.state.get("student_id")
    if not sid:
        email = tool_context.state.get("student_email")
        if email:
            with _get_connection() as conn:
                row = conn.execute(
                    "SELECT student_id FROM students WHERE email = ? COLLATE NOCASE",
                    (email,),
                ).fetchone()
                if row:
                    sid = row["student_id"]
                    tool_context.state["student_id"] = sid

    if not sid:
        return {
            "status": "error",
            "message": (
                "No student has been identified yet. Please identify the student "
                "using their registered email address before querying enrollments."
            ),
        }

    with _get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                e.enrollment_id,
                e.student_id,
                e.course_id,
                c.course_name,
                c.price as course_price,
                e.purchased_at,
                e.amount_paid,
                e.completion_percent,
                e.status,
                e.refund_reason
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = ?
            ORDER BY e.purchased_at DESC
            """,
            (sid,),
        )
        rows = cursor.fetchall()

    enrollments = [dict(row) for row in rows]
    return {
        "status": "success",
        "student_id": sid,
        "count": len(enrollments),
        "enrollments": enrollments,
    }


def check_refund_eligibility(enrollment_id: str) -> dict[str, Any]:
    """Check whether a course enrollment is eligible for a refund according to CampusX policy.

    Eligibility requirements:
    - Enrollment must be in 'active' status (not already requested or refunded).
    - Purchased within the last 7 days.
    - Course completion must be 20% or less.

    Args:
        enrollment_id: The ID of the enrollment to check (e.g. 'ENR001').

    Returns:
        A dictionary detailing eligibility, full refund amount, and reasons if ineligible.
    """
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                e.enrollment_id,
                e.student_id,
                e.course_id,
                c.course_name,
                e.purchased_at,
                e.amount_paid,
                e.completion_percent,
                e.status,
                e.refund_reason
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.enrollment_id = ?
            """,
            (enrollment_id.strip(),),
        )
        row = cursor.fetchone()

    if not row:
        return {
            "eligible": False,
            "status": "not_found",
            "reasons": [f"Enrollment with ID '{enrollment_id}' was not found."],
        }

    enrollment = dict(row)
    now = datetime.now(timezone.utc)
    purchased_at = datetime.fromisoformat(enrollment["purchased_at"])
    if purchased_at.tzinfo is None:
        purchased_at = purchased_at.replace(tzinfo=timezone.utc)

    days_since_purchase = (now - purchased_at).total_seconds() / 86400.0
    completion_percent = float(enrollment["completion_percent"])
    status = enrollment["status"]

    ineligible_reasons = []

    # 1. Status check
    if status == "refund_requested":
        ineligible_reasons.append("A refund has already been requested for this enrollment.")
    elif status == "refunded":
        ineligible_reasons.append("This enrollment has already been refunded.")
    elif status != "active":
        ineligible_reasons.append(f"Enrollment status is '{status}', only active enrollments can be refunded.")

    # 2. 7-day window check
    if days_since_purchase > 7.0:
        ineligible_reasons.append(
            f"Course was purchased {days_since_purchase:.1f} days ago, exceeding the 7-day refund window."
        )

    # 3. Completion threshold check (max 20%)
    if completion_percent > 20.0:
        ineligible_reasons.append(
            f"Course completion is {completion_percent:.1f}%, exceeding the maximum 20% completion threshold."
        )

    is_eligible = len(ineligible_reasons) == 0

    return {
        "eligible": is_eligible,
        "enrollment_id": enrollment["enrollment_id"],
        "course_name": enrollment["course_name"],
        "amount_paid": enrollment["amount_paid"],
        "refund_amount": enrollment["amount_paid"] if is_eligible else 0,
        "currency": "INR",
        "days_since_purchase": round(days_since_purchase, 1),
        "completion_percent": completion_percent,
        "status": status,
        "reasons": ineligible_reasons if not is_eligible else ["Enrollment is eligible for a full refund."],
    }


def request_refund(
    enrollment_id: str,
    reason: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Request a refund for an eligible course enrollment.

    Presents a confirmation dialog to the user before submitting the refund request.

    Args:
        enrollment_id: The ID of the enrollment to refund.
        reason: The reason for requesting a refund.

    Returns:
        A dictionary with the result of the refund request.
    """
    enrollment_id = enrollment_id.strip()
    reason = reason.strip()

    if not reason:
        return {
            "status": "error",
            "message": "A non-blank reason is required to request a refund.",
        }

    # Fetch enrollment details first
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT e.enrollment_id, e.amount_paid, e.status, c.course_name
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.enrollment_id = ?
            """,
            (enrollment_id,),
        )
        row = cursor.fetchone()

    if not row:
        return {
            "status": "error",
            "message": f"Enrollment '{enrollment_id}' was not found.",
        }

    if row["status"] != "active":
        return {
            "status": "error",
            "message": f"Cannot request refund: enrollment status is '{row['status']}'.",
        }

    # Confirmation handling
    confirmation = tool_context.tool_confirmation
    if confirmation is None:
        tool_context.request_confirmation(
            hint=(
                f"Please confirm submitting a refund request of ₹{row['amount_paid']} "
                f"for course '{row['course_name']}' (Enrollment ID: {enrollment_id})."
            ),
            payload={
                "enrollment_id": enrollment_id,
                "amount": row["amount_paid"],
                "course_name": row["course_name"],
                "reason": reason,
            },
        )
        return {
            "status": "confirmation_required",
            "message": f"Confirmation required to submit refund request for enrollment {enrollment_id}.",
        }

    if not confirmation.confirmed:
        return {
            "status": "rejected",
            "message": "Refund request was not confirmed by the user.",
        }

    # Confirmed: update status in database
    with _get_connection() as conn:
        with conn:
            conn.execute(
                """
                UPDATE enrollments
                SET status = 'refund_requested', refund_reason = ?
                WHERE enrollment_id = ?
                """,
                (reason, enrollment_id),
            )

    return {
        "status": "refund_requested",
        "enrollment_id": enrollment_id,
        "course_name": row["course_name"],
        "amount_paid": row["amount_paid"],
        "refund_amount": row["amount_paid"],
        "currency": "INR",
        "refund_reason": reason,
        "message": (
            f"Refund request of ₹{row['amount_paid']} for {row['course_name']} "
            f"(Enrollment: {enrollment_id}) has been recorded and is pending processing."
        ),
    }


def get_refund_status(enrollment_id: str) -> dict[str, Any]:
    """Check the refund status of a course enrollment.

    Args:
        enrollment_id: The ID of the enrollment (e.g. 'ENR001').

    Returns:
        A dictionary with the enrollment and current refund status.
    """
    enrollment_id = enrollment_id.strip()
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                e.enrollment_id,
                e.student_id,
                s.name as student_name,
                s.email as student_email,
                c.course_name,
                e.amount_paid,
                e.status,
                e.refund_reason,
                e.purchased_at
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            JOIN students s ON e.student_id = s.student_id
            WHERE e.enrollment_id = ?
            """,
            (enrollment_id,),
        )
        row = cursor.fetchone()

    if not row:
        return {
            "status": "not_found",
            "message": f"No enrollment found with ID '{enrollment_id}'.",
        }

    status = row["status"]
    if status == "refund_requested":
        message = "Your refund request is currently pending processing."
    elif status == "refunded":
        message = "This enrollment has been refunded."
    else:
        message = "Enrollment is active; no refund has been requested."

    return {
        "status": status,
        "enrollment_id": row["enrollment_id"],
        "course_name": row["course_name"],
        "amount_paid": row["amount_paid"],
        "refund_reason": row["refund_reason"],
        "message": message,
    }
