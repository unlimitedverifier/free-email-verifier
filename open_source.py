#!/usr/bin/env python3
"""
UnlimitedVerifier.com - Open Source Email Verifier
Stage 1 Email Verification

https://unlimitedverifier.com
https://github.com/unlimitedverifier/open-source-email-verifier

MIT License - Free to use, modify, and distribute
"""

import re
import dns.resolver
import smtplib
import socket
import time
from typing import Optional

__version__ = "1.0.0"
__author__ = "UnlimitedVerifier.com"
__license__ = "MIT"

RATE_LIMIT_SECONDS = 5
SMTP_TIMEOUT = 10
HELO_HOSTNAME = "verify.unlimitedverifier.com"

last_verification_time = 0


def validate_syntax(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_mx_records(domain: str) -> list[str]:
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_hosts = sorted([(r.preference, str(r.exchange).rstrip('.')) for r in records])
        return [host for _, host in mx_hosts]
    except Exception:
        return []


def verify_smtp(email: str, mx_host: str) -> dict:
    result = {
        "mx_host": mx_host,
        "connected": False,
        "helo_ok": False,
        "mail_from_ok": False,
        "rcpt_to_ok": False,
        "error": None
    }

    try:
        smtp = smtplib.SMTP(timeout=SMTP_TIMEOUT)
        smtp.connect(mx_host, 25)
        result["connected"] = True

        code, _ = smtp.helo(HELO_HOSTNAME)
        if code == 250:
            result["helo_ok"] = True

        code, _ = smtp.mail(f"verify@{HELO_HOSTNAME}")
        if code == 250:
            result["mail_from_ok"] = True

        code, _ = smtp.rcpt(email)
        if code == 250:
            result["rcpt_to_ok"] = True

        smtp.quit()
    except smtplib.SMTPServerDisconnected as e:
        result["error"] = f"Server disconnected: {e}"
    except smtplib.SMTPResponseException as e:
        result["error"] = f"SMTP error {e.smtp_code}: {e.smtp_error}"
    except socket.timeout:
        result["error"] = "Connection timeout"
    except socket.error as e:
        result["error"] = f"Socket error: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result


def verify_email(email: str) -> dict:
    global last_verification_time

    now = time.time()
    elapsed = now - last_verification_time
    if elapsed < RATE_LIMIT_SECONDS:
        wait_time = RATE_LIMIT_SECONDS - elapsed
        print(f"  Rate limit: waiting {wait_time:.1f}s...")
        time.sleep(wait_time)

    last_verification_time = time.time()

    result = {
        "email": email,
        "valid_syntax": False,
        "domain": None,
        "mx_records": [],
        "smtp_check": None,
        "deliverable": False
    }

    if not validate_syntax(email):
        return result
    result["valid_syntax"] = True

    domain = email.split('@')[1]
    result["domain"] = domain

    mx_records = get_mx_records(domain)
    result["mx_records"] = mx_records

    if not mx_records:
        return result

    for mx_host in mx_records:
        smtp_result = verify_smtp(email, mx_host)
        result["smtp_check"] = smtp_result

        if smtp_result["rcpt_to_ok"]:
            result["deliverable"] = True
            break

        if smtp_result["connected"]:
            break

    return result


def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   _   _       _ _           _ _           _               ║
║  | | | |_ __ | (_)_ __ ___ (_) |_ ___  __| |              ║
║  | | | | '_ \\| | | '_ ` _ \\| | __/ _ \\/ _` |              ║
║  | |_| | | | | | | | | | | | | ||  __/ (_| |              ║
║   \\___/|_| |_|_|_|_| |_| |_|_|\\__\\___|\\__,_|              ║
║                                                           ║
║   __     __        _  __ _                                ║
║   \\ \\   / /__ _ __(_)/ _(_) ___ _ __                      ║
║    \\ \\ / / _ \\ '__| | |_| |/ _ \\ '__|                     ║
║     \\ V /  __/ |  | |  _| |  __/ |                        ║
║      \\_/ \\___|_|  |_|_| |_|\\___|_|                        ║
║                                                           ║
║   Open Source Email Verifier - Stage 1                    ║
║   https://unlimitedverifier.com                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")


def main():
    print_banner()
    print(f"  Version: {__version__}")
    print(f"  Rate limit: 1 email per {RATE_LIMIT_SECONDS} seconds")
    print(f"  HELO hostname: {HELO_HOSTNAME}")
    print()

    while True:
        try:
            email = input("  Enter email to verify (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye from UnlimitedVerifier.com!")
            break

        if email.lower() == 'quit':
            print("\n  Goodbye from UnlimitedVerifier.com!")
            break

        if not email:
            continue

        print(f"\n  Verifying: {email}")
        result = verify_email(email)

        print(f"\n  ┌─────────────────────────────────────────────────")
        print(f"  │ Results for: {result['email']}")
        print(f"  ├─────────────────────────────────────────────────")
        print(f"  │ Syntax Valid:    {'✓' if result['valid_syntax'] else '✗'}")
        print(f"  │ Domain:          {result['domain'] or 'N/A'}")
        print(f"  │ MX Records:      {len(result['mx_records'])} found")

        if result['smtp_check']:
            smtp = result['smtp_check']
            print(f"  │ SMTP Server:     {smtp['mx_host']}")
            print(f"  │   Connected:     {'✓' if smtp['connected'] else '✗'}")
            print(f"  │   HELO:          {'✓' if smtp['helo_ok'] else '✗'}")
            print(f"  │   MAIL FROM:     {'✓' if smtp['mail_from_ok'] else '✗'}")
            print(f"  │   RCPT TO:       {'✓' if smtp['rcpt_to_ok'] else '✗'}")
            if smtp['error']:
                print(f"  │   Error:         {smtp['error']}")

        status = "✓ DELIVERABLE" if result['deliverable'] else "✗ UNDELIVERABLE"
        print(f"  ├─────────────────────────────────────────────────")
        print(f"  │ Status:          {status}")
        print(f"  └─────────────────────────────────────────────────")
        print()


if __name__ == "__main__":
    main()
