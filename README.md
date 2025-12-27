# UnlimitedVerifier - Open Source Email Verifier

A free, open-source unlimited email verification tool by [UnlimitedVerifier.com](https://unlimitedverifier.com).

---

### Want the full experience? Try [UnlimitedVerifier.com](https://unlimitedverifier.com)

**Verify 1 million emails for $29. Or 10 million. Same price.**

| Feature | Open Source | UnlimitedVerifier.com |
|---------|-------------|----------------------|
| Syntax & Domain Check | ✓ | ✓ |
| MX Record Lookup | ✓ | ✓ |
| SMTP Verification | ✓ | ✓ |
| Bulk Verification | - | ✓ Unlimited |
| Catch-All Detection | - | ✓ True-Send™ |
| 99.5% Accuracy | - | ✓ Deep Verification |
| API Access | - | ✓ |
| Web Dashboard | - | ✓ |
| CSV/Excel Export | - | ✓ |

**True-Send™ Catch-All Verification** - We don't guess. We deliver a real email and watch what happens. Bounce or delivered. So you can send with confidence.

**Standard verification is free forever. No credit card required.**

[Start Verifying Free](https://unlimitedverifier.com) | [View Pricing](https://unlimitedverifier.com/pricing) | [API Docs](https://unlimitedverifier.com/docs)

---

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   _   _       _ _           _ _           _               ║
║  | | | |_ __ | (_)_ __ ___ (_) |_ ___  __| |              ║
║  | | | | '_ \| | | '_ ` _ \| | __/ _ \/ _` |              ║
║  | |_| | | | | | | | | | | | | ||  __/ (_| |              ║
║   \___/|_| |_|_|_|_| |_| |_|_|\__\___|\\__,_|              ║
║                                                           ║
║   __     __        _  __ _                                ║
║   \ \   / /__ _ __(_)/ _(_) ___ _ __                      ║
║    \ \ / / _ \ '__| | |_| |/ _ \ '__|                     ║
║     \ V /  __/ |  | |  _| |  __/ |                        ║
║      \_/ \___|_|  |_|_| |_|\___|_|                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## What is Stage 1 Verification?

Stage 1 email verification performs the following checks:

1. **Syntax Validation** - Checks if the email format is valid
2. **MX Record Lookup** - Finds the mail servers for the domain
3. **SMTP Verification** - Connects to the mail server and checks:
   - HELO handshake
   - MAIL FROM command
   - RCPT TO command (checks if mailbox exists)

This is a basic verification that tells you if an email address is likely deliverable without actually sending an email.

## Features

- Single Python file - no complex setup
- Rate limited (1 email per 5 seconds) to be respectful to mail servers
- MIT License - use it however you want
- Clean CLI interface with formatted output
- Works with any email domain

## Requirements

- Python 3.9+
- `dnspython` library

## Installation

```bash
# Clone or download open_source.py
git clone https://github.com/unlimitedverifier/open-source-email-verifier.git
cd open-source-email-verifier

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install dnspython
```

## Usage

### Interactive Mode

```bash
python open_source.py
```

Then enter email addresses one at a time.

### Programmatic Usage

```python
from open_source import verify_email, validate_syntax, get_mx_records

# Full verification
result = verify_email("test@example.com")
print(result)
# {
#     "email": "test@example.com",
#     "valid_syntax": True,
#     "domain": "example.com",
#     "mx_records": ["mail.example.com"],
#     "smtp_check": {...},
#     "deliverable": True/False
# }

# Just syntax check
is_valid = validate_syntax("test@example.com")

# Just MX lookup
mx_servers = get_mx_records("example.com")
```

## Example Output

```
  Verifying: test@gmail.com

  ┌─────────────────────────────────────────────────
  │ Results for: test@gmail.com
  ├─────────────────────────────────────────────────
  │ Syntax Valid:    ✓
  │ Domain:          gmail.com
  │ MX Records:      5 found
  │ SMTP Server:     gmail-smtp-in.l.google.com
  │   Connected:     ✓
  │   HELO:          ✓
  │   MAIL FROM:     ✓
  │   RCPT TO:       ✗
  │   Error:         None
  ├─────────────────────────────────────────────────
  │ Status:          ✗ UNDELIVERABLE
  └─────────────────────────────────────────────────
```

## Important Notes

### Port 25 Access Required

SMTP verification requires outbound access to port 25. Many ISPs and cloud providers block this port to prevent spam. If you see "Connection timeout" errors, your network likely blocks port 25.

**Solutions:**
- Run on a VPS/dedicated server that allows port 25
- Use a hosting provider that permits SMTP connections
- Contact your ISP to unblock port 25

### Rate Limiting

This tool is intentionally rate-limited to 1 verification every 5 seconds. This is to:
- Be respectful to mail servers
- Avoid getting your IP blacklisted
- Comply with acceptable use policies

For high-volume verification, check out [UnlimitedVerifier.com](https://unlimitedverifier.com).

### Limitations

- **Catch-all domains**: Some domains accept all emails (catch-all), so RCPT TO will succeed even for non-existent mailboxes. [UnlimitedVerifier.com](https://unlimitedverifier.com) solves this with True-Send™ technology.
- **Greylisting**: Some servers temporarily reject first connection attempts
- **Rate limiting by mail servers**: Gmail, Yahoo, etc. may throttle or block repeated verification attempts
- **False positives/negatives**: No SMTP verification is 100% accurate. For 99.5% accuracy, use [Deep Verification](https://unlimitedverifier.com).

## Configuration

You can modify these constants at the top of the file:

```python
RATE_LIMIT_SECONDS = 5      # Time between verifications
SMTP_TIMEOUT = 10           # Connection timeout in seconds
HELO_HOSTNAME = "verify.unlimitedverifier.com"  # HELO identity
```

## License

MIT License - Free to use, modify, and distribute.

## Need More Power?

This open-source tool is great for learning and small-scale verification. For production use:

**[UnlimitedVerifier.com](https://unlimitedverifier.com)** - Verify 1 million emails for $29

- **Unlimited bulk verification** - Upload CSV/Excel, get clean results in minutes
- **True-Send™ catch-all verification** - Real delivery testing, not guessing
- **99.5% accuracy** with Deep Verification
- **REST API** for integration
- **Free standard verification** - No credit card required

[Get Started Free](https://unlimitedverifier.com)

## Contributing

Pull requests welcome! Please keep changes minimal and focused.

## Support

- Issues: [GitHub Issues](https://github.com/unlimitedverifier/open-source-email-verifier/issues)
- Website: [unlimitedverifier.com](https://unlimitedverifier.com)
