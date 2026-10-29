# Safely add this starter to your existing repository

1. **Make a backup first.** In VS Code, use File → Save All. Optionally make a copy of your current project folder.
2. Unzip this starter into a separate folder first and inspect it.
3. Copy only the new `src/` files, `tests/`, `.env.example`, and relevant README sections into your existing project. If your project already has `src/`, compare files before copying; do not overwrite files with the same name blindly.
4. Keep existing Part A/B/C/D folders until the new path is working.
5. Use the current project virtual environment if possible. Install missing dependencies from `requirements.txt`.
6. Download the UCI dataset into `data/raw/Online Retail.xlsx`.
7. Run Part 1 and verify that `data/processed/online_retail_clean.csv`, `data/processed/retail.sqlite`, and the three charts exist.
8. Only after verifying outputs, stage the intended files with `git status` and commit one part at a time.

If you cannot upload files to ChatGPT, you can paste terminal output or an error traceback (remove secrets first). Never share `.env`, passwords, access tokens, or API keys.
