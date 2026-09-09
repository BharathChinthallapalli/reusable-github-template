# Security reporting

Project: @@PROJECT_NAME@@

Report suspected vulnerabilities privately through
[the security reporting contact](@@SECURITY_CONTACT@@).
This route must be configured and verified before the project accepts users.
If this page still contains template markers, the maintainer must initialize it.
Do not put sensitive findings, credentials, or exploit details in public issues.

Include affected version or commit, the expected trust boundary, reproduction
steps, impact, and a safe proof of concept where possible. Share only information
you are authorized to disclose. The project maintainer sets response times and
supported release versions in this file when the project starts shipping.

## Maintainer setup

- Confirm that the reporting route is monitored and private.
- Document supported versions and the patch delivery process here.
- Enable appropriate GitHub security features in repository settings.
- If a credential is exposed, revoke or rotate it; deleting a file is insufficient.

The included CI checks do not scan the application's security. See
[GitHub setup](docs/github-setup.md) and [the threat model](docs/threat-model.md).
