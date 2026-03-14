#!/bin/sh
set -e

API_KEY=$(python3 -c "import json; d=json.load(open('/data/options.json')); print(d.get('anthropic_api_key',''))" 2>/dev/null || echo "")

cat > /var/www/html/config.js << JSEOF
window.PAC_CONFIG = { "apiKey": "${API_KEY}" };
JSEOF

echo "[PAC Manager] Démarrage — clé API: ${#API_KEY} caractères"
exec nginx -g "daemon off;"
