#!/usr/bin/env python3
"""Strip credential material from an audit summary before it is published.

The auditing skill is instructed never to write a credential value into its
report, but that instruction constrains the same agent an audited repository
is trying to steer, so it cannot be the only control. This runs after the
report is written and before it replaces the pull request comment.
"""

import base64
import os
import pathlib
import re
import sys

# Credentials this job actually holds. An audited repository that redirects a
# read is reaching for one of these, so match the literal values rather than
# hoping a shape covers them.
KNOWN_VALUE_VARS = ("REDACT_GITHUB_TOKEN", "REDACT_ANTHROPIC_KEY")

# Shapes, as a net for third-party credentials the audited repository itself
# committed. Each is anchored on a vendor prefix and a minimum length, so
# prose that merely discusses a token type does not trip it.
PATTERNS = (
    ("github-token", r"gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,}"),
    ("anthropic-key", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("openai-key", r"sk-[A-Za-z0-9]{32,}"),
    ("aws-access-key", r"(?:AKIA|ASIA)[0-9A-Z]{16}"),
    ("npm-token", r"npm_[A-Za-z0-9]{36}"),
    ("slack-token", r"xox[abprs]-[A-Za-z0-9-]{10,}"),
    ("google-api-key", r"AIza[0-9A-Za-z_-]{35}"),
    ("jwt", r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    (
        "private-key-block",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----",
    ),
)


def _forms(value):
    """Every shape a credential this job holds can wear in a report."""
    yield value
    # actions/checkout writes the token into .git/config as
    # base64("x-access-token:<token>") under http.extraheader. The raw value
    # is not a substring of that, and no `gh*_` shape matches base64 either,
    # so without this the one credential worth catching is the one that gets
    # through.
    yield base64.b64encode(f"x-access-token:{value}".encode()).decode()
    # A quoted Authorization header or an encoded secret carries the bare
    # value the same way.
    yield base64.b64encode(value.encode()).decode()


def redact(text):
    hits = []

    for var in KNOWN_VALUE_VARS:
        value = os.environ.get(var, "")
        # A short or empty value would match everywhere or nowhere useful.
        if len(value) < 12:
            continue
        label = var.removeprefix("REDACT_").lower().replace("_", "-")
        for form in _forms(value):
            if form in text:
                text = text.replace(form, "[REDACTED runner credential]")
                if label not in hits:
                    hits.append(label)

    for label, pattern in PATTERNS:
        text, count = re.subn(pattern, f"[REDACTED {label}]", text)
        if count:
            hits.append(f"{label} x{count}")

    return text, hits


def main():
    if len(sys.argv) != 2:
        print("usage: redact-credentials.py <summary-file>", file=sys.stderr)
        return 2

    path = pathlib.Path(sys.argv[1])
    if not path.is_file():
        print(f"No summary at {path}; nothing to redact.")
        return 0

    # A report can quote `strings` output from a bundled binary, which need
    # not be valid UTF-8. surrogateescape round-trips those bytes so redaction
    # still runs, rather than raising and leaving the gate to withhold a report
    # that was very likely fine.
    text, hits = redact(path.read_text(encoding="utf-8", errors="surrogateescape"))
    if not hits:
        print("No credential material in the audit summary.")
        return 0

    path.write_text(text, encoding="utf-8", errors="surrogateescape")
    detail = ", ".join(hits)
    print(
        f"::error::Redacted credential material from the audit summary ({detail}). "
        "The audit is instructed never to write a credential value into its report, "
        "so this means either that instruction was not followed or the audited "
        "repository steered the agent into reading something it should not have."
    )
    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with open(github_output, "a") as handle:
            handle.write("redacted=true\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
