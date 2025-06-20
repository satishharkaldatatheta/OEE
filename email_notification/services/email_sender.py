import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .db import get_db_connection
from dotenv import load_dotenv

load_dotenv()

# ────────────────────────────────────────────────────────────────────────────────
def send_email(to_addr: str, subject: str, html_body: str):
    from_addr = os.getenv("EMAIL_ADDRESS")
    pwd       = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"]   = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.office365.com", 587) as smtp:
        smtp.starttls()
        smtp.login(from_addr, pwd)
        smtp.sendmail(from_addr, to_addr, msg.as_string())

# ────────────────────────────────────────────────────────────────────────────────
def send_user_notifications():
    conn = get_db_connection()
    cur  = conn.cursor()

    cur.execute("SELECT DISTINCT user_id FROM oee.user_notifications WHERE is_read = FALSE")
    users = [row[0] for row in cur.fetchall()]

    for uid in users:
        # user info
        cur.execute("""
            SELECT firstname, lastname, email
            FROM oee.loginuser
            WHERE id=%s
        """, (uid,))
        u = cur.fetchone()
        if not u:
            continue
        fname, lname, email = u

        # unread notifications
        cur.execute("""
            SELECT n.item_id, n.equipment_id, n.loc_id, n.intensity,
                   n.description, n.inactive_since, n.inactive_hours, n.created_at
            FROM oee.user_notifications un
            JOIN oee.notifications n ON un.notification_id = n.id
            WHERE un.user_id=%s AND un.is_read = FALSE
            ORDER BY n.created_at DESC
        """, (uid,))
        rows = cur.fetchall()
        if not rows:
            continue

        # build email
        html = f"""
        <p>Hi {fname} {lname},</p>
        <p>The following reactor inactivity alerts require your attention:</p>
        <table border="1" cellpadding="5">
        <tr>
            <th>Item</th><th>Equipment</th><th>Location</th>
            <th>Intensity</th><th>Description</th>
            <th>Inactive&nbsp;Since</th><th>Inactive&nbsp;Hours</th><th>Notified&nbsp;At</th>
        </tr>
        """
        for r in rows:
            item, equip, loc, inten, desc, since, hrs, created = r
            html += (
                "<tr>"
                f"<td>{item}</td><td>{equip}</td><td>{loc}</td>"
                f"<td>{inten.upper()}</td><td>{desc}</td>"
                f"<td>{since}</td><td>{hrs}</td><td>{created}</td>"
                "</tr>"
            )

        html += "</table><p>Regards,<br>OEE Monitoring System</p>"
        send_email(email, "⚠ Reactor Inactivity Alert", html)

    cur.close(); conn.close()
    print("Emails sent.")
