find . \( -name "*.js" -o -name "*.ts" -o -name "*.mjs" -o -name "*.json" -o -name "*.md" \) \
    -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.vscode/*" -type f \
    -exec sh -c 'echo "=== $1 ==="; cat "$1"; echo' _ {} \; > code