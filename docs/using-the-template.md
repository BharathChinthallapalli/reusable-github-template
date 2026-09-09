# Create and reuse the template

## Prepare local validation

The initializer and foundation checker run with Python 3.12+ alone. The AI
configuration checker and full test suite also require the pinned development
dependency. Create a virtual environment in the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell, create it with `py -3.12 -m venv .venv` and activate with
`.venv\Scripts\Activate.ps1`. If activation is unavailable, invoke
`.venv\Scripts\python.exe` directly for the commands below; no shell policy
change is needed. On macOS/Linux, `.venv/bin/python` also works without activation.
Reuse the environment; reinstall dependencies when `requirements-dev.txt` changes.

From that environment, run all three checks:

```bash
python tools/check_repository.py
python tools/check_ai_configuration.py
python -m unittest discover -s tests -v
```

Static AI validation does not inspect your editor. Complete the separate
[host discovery check](ai-assistance.md) in the actual client.

## Set up the shared template once

1. Extract the ZIP and open the `reusable-github-template` folder in VS Code.
2. Prepare the validation environment and run the three checks above.
3. Create an empty GitHub repository named `repository-template` in the intended
   account or organization. Select the visibility appropriate for your team.
4. Push the extracted files, including `.github` and the other dotfiles. From
   the extracted folder, a typical first push is:

   ```bash
   git init -b main
   git add .
   git commit -m "Add reusable repository foundation"
   git remote add origin https://github.com/YOUR-ACCOUNT/repository-template.git
   git push -u origin main
   ```

   Replace `YOUR-ACCOUNT` with the real owner. These commands assume a new,
   empty destination. Do not force-push over an existing repository.
5. In the repository's **Settings → General**, select **Template repository**.

Keep this shared source uninitialized so each new project can run its own setup.
If the source needs real reporting and ownership, maintain those source-only
policies through your organization, or carefully separate them from the project
markers. Do not run the project initializer in the shared source.

## Create a project

1. Click **Use this template → Create a new repository**. Usually copy only the
   default branch. Select the new owner, name, and visibility, then clone it.
2. Run the initializer command from README.md with actual project values. Inspect
   the preview, then repeat it with `--write`.
3. Inspect `git diff`. CODEOWNERS must name an existing user or visible team with
   explicit write access. The script validates syntax, not remote membership.
4. Run the three local checks. Commit and push the initialized project.
5. Follow [GitHub setup](github-setup.md) and select the project license.
6. Add the application, its commands, and meaningful CI. Replace README's
   template introduction with the project's actual purpose and quick start.

Initialization is repeatable with identical inputs. It refuses different inputs
once initialized so later project edits are preserved. For a rename, make an
ordinary reviewed change to the project files and `template.json`.

## What carries over

GitHub templates reproduce files and directory structure, with a new repository
history. They are not a continuous inheritance mechanism. New source-template
changes do not automatically update existing projects. Review and port changes
as described in [maintenance](maintenance.md).

Repository settings need separate configuration. The ZIP does not activate
rules, invite people, register secrets, or provision Azure resources.

Sources: [create a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository),
[create from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
