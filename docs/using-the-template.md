# Create and reuse the template

## Set up the shared template once

1. Extract the ZIP and open the `reusable-github-template` folder in VS Code.
2. Run `python3 tools/check_repository.py` and
   `python3 -m unittest discover -s tests -v`.
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
4. Run both local checks. Commit and push the initialized project.
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
