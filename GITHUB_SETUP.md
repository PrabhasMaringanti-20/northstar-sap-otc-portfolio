# Push to GitHub and open the website

GitHub stores the whole repository. GitHub Pages serves its static browser application. Pushing files alone does not enable Pages; the publishing source must be selected once.

## Free route

Use a **public repository** with GitHub Free and the default github.io address. No custom domain, SAP subscription or paid backend is needed. The repository contains synthetic records and simulated analysis. The site and source will be public, so add only information you intend to share. The chat/cloud workspace's own pricing is separate.

## Option A — Git commands

Create a new empty public repository named `northstar-otc` on GitHub. Extract this project's ZIP and open a terminal inside the folder containing index.html, README.md, viewer and scripts. Replace YOUR_USERNAME in the remote URL below.

```bash
git init
git add .
git commit -m "Add simulated NorthStar OTC portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/northstar-otc.git
git push -u origin main
```

Authenticate using your normal GitHub/Git credential workflow. Do not put tokens in source files. If a remote already exists, inspect it with `git remote -v` before changing anything. The downloaded folder contains no .git history, credentials or configured remote.

## Option B — GitHub Desktop

Create a repository from the extracted project folder in GitHub Desktop, make the initial commit and choose Publish repository. Select public visibility for the GitHub Free Pages route. Ensure `index.html` is at the repository root, not inside an extra nested northstar-otc folder.

## Enable Pages once

In the repository, open Settings → Pages. Under Build and deployment, choose **Deploy from a branch**, select **main** and **/(root)**, then Save. Wait for GitHub's deployment result. The usual project URL is `https://YOUR_USERNAME.github.io/northstar-otc/`; copy the actual URL shown by GitHub. Subsequent pushes to the selected branch update the site.

The root index.html is self-contained. Relative file links work under a repository subpath. The supplied .nojekyll prevents Jekyll processing; no Node/Python build is needed to host the prebuilt application. No GitHub Actions deployment workflow is required for this route. The repository ignores generated ZIP archives to avoid recursively committing release bundles; PDFs, screenshots, code, data and editable reports remain included.

## Check your deployed site

Open the actual Pages URL, navigate all sections, search NS-ORD-1001, export a CSV, open a PDF and test on a phone. GitHub deployment has not been run or verified by this handover. Local testing does not claim a live URL exists.

## Sources checked 11 October 2026

- GitHub Pages availability and static hosting: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- Publishing from a branch and root folder: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

The first source confirms GitHub Free supports Pages for public repositories. The second describes the branch/folder configuration above. Future GitHub product or account changes should be checked against the official documentation.
