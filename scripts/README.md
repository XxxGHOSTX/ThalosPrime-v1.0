# Thalos Prime Scripts

This directory contains DevOps automation scripts for Thalos Prime development.

## Available Scripts

### create_feature_branch.sh
Creates a new feature branch with standardized naming.

Usage:
```bash
./scripts/create_feature_branch.sh feature-name
```

Creates branch: `feature/feature-name`

### scaffold_module.sh
Scaffolds a new Python module with standard structure.

Usage:
```bash
./scripts/scaffold_module.sh <module-name> <module-type>
```

Module types: `subsystem`, `integration`, `utility`

Example:
```bash
./scripts/scaffold_module.sh analytics subsystem
```

Creates:
- `src/thalos_prime/module_name/__init__.py`
- Basic class structure
- Tests directory

### commit_changes.sh
Commits changes with AI-generated commit messages.

Usage:
```bash
./scripts/commit_changes.sh "Short description"
```

Features:
- Stages all changes
- Generates descriptive commit message
- Follows conventional commits format

### create_pr.sh
Creates a pull request with detailed description.

Usage:
```bash
./scripts/create_pr.sh "PR Title"
```

Features:
- Creates PR from current branch
- Generates detailed description
- Adds appropriate labels

### create_release.sh
Creates a new release with changelog generation.

Usage:
```bash
./scripts/create_release.sh 1.0.1
```

Features:
- Tags release
- Generates changelog
- Creates GitHub release
- Publishes to PyPI (if configured)

## Prerequisites

All scripts require:
- Git installed and configured
- GitHub CLI (`gh`) for PR/release operations
- Bash shell environment
- Appropriate permissions for the repository

## Configuration

Some scripts may require environment variables:
- `GITHUB_TOKEN` - For GitHub API operations
- `PYPI_TOKEN` - For package publishing

## Best Practices

1. **Always run from repository root**
   ```bash
   ./scripts/script_name.sh
   ```

2. **Review changes before committing**
   ```bash
   git status
   git diff
   ```

3. **Test scripts on feature branches first**

4. **Follow naming conventions**
   - Feature branches: `feature/name`
   - Bugfix branches: `bugfix/name`
   - Hotfix branches: `hotfix/name`

## Troubleshooting

### Permission Denied
```bash
chmod +x scripts/*.sh
```

### GitHub CLI Not Found
```bash
# Install gh CLI
# See: https://cli.github.com/
```

### Script Fails
Check the script output for error messages. Most scripts provide detailed error information.

## Contributing

When adding new scripts:
1. Follow existing naming conventions
2. Add error handling
3. Include usage documentation
4. Make script executable: `chmod +x script.sh`
5. Update this README
