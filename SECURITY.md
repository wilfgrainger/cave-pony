# Security policy

Cave Pony is an instruction contract, not executable runtime software. Security reports are still important when a change could weaken authentication, authorisation, trust-boundary validation, secret handling, destructive-operation warnings, recovery, accessibility, data integrity, or workflow supply-chain safety.

## Sensitive reports

Use GitHub's **Security → Report a vulnerability** route when it is available for this repository.

When private vulnerability reporting is unavailable, open a public issue titled `Private security contact requested`. Do not include exploit details, secrets, personal data, or reproduction steps that would create risk. A maintainer can then arrange a private channel.

## Non-sensitive reports

Open a normal GitHub issue with:

- the affected file and version;
- the unsafe or misleading behaviour;
- the smallest reproduction that contains no secrets;
- the expected safe behaviour;
- any proposed minimal correction.

## Scope

Examples include:

- wording that encourages removal of authentication or authorisation;
- compression that hides destructive consequences or recovery;
- instructions that expose secrets or personal data;
- CI changes that grant unnecessary write permissions or use mutable third-party actions;
- claims that tests or checks passed when they did not run.

Do not test against systems, repositories, accounts, or data you do not own or have permission to assess.
