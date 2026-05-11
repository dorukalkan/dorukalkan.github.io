# doruk docs

Personal docs site for technical notes, tooling references, and project documentation.

The site is built with [Zensical](https://zensical.org/) and is intended to deploy to GitHub Pages at `https://docs.dorukalkan.com`.

## Local development

This project uses `uv` for Python dependency management.

```bash
uv sync
uv run zensical serve
```

Build the static site:

```bash
uv run zensical build --clean
```

The generated site is written to `site/`.

## Deployment

GitHub Actions builds and deploys the site from `main` using `.github/workflows/docs.yml`.

GitHub Pages should be configured to deploy from GitHub Actions, and the custom domain should be set to:

```text
docs.dorukalkan.com
```

DNS for the subdomain is managed in Squarespace.
