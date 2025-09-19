#!/usr/bin/env bash
set -euo pipefail

# === settings ===
ZBX_SERVER_IP="${1:-"192.168.1.160"}"
ZBX_CONF="/etc/zabbix/zabbix_agent2.conf"
ZBX_D_DIR="/etc/zabbix/zabbix_agent2.d"
SERVICE_NAME="start-eurotherm.service"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

need_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "Restarting as root..."
    # -H so HOME=/root (pip does not complain about cache), -E to preserve PATH and other envs
    exec sudo -E -H bash "$0" "$@"
  fi
}
need_root "$@"

echo "== 1) Updating packages and installing dependencies =="
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip zabbix-agent2

echo "== 2) Installing Python library minimalmodbus (system-wide) =="
python3 -m pip install --upgrade pip
PIP_BRK=()
# if PEP 668 protection exists — add the flag
if [[ -e /usr/lib/python3*/EXTERNALLY-MANAGED || -e /usr/local/lib/python3*/EXTERNALLY-MANAGED ]]; then
  PIP_BRK+=(--break-system-packages)
fi
python3 -m pip install "${PIP_BRK[@]}" minimalmodbus

echo "== 3) Configuring Zabbix Agent 2 =="
if [[ -f "$ZBX_CONF" ]]; then
  cp -a "$ZBX_CONF" "${ZBX_CONF}.bak.$(date +%F_%H%M%S)"
fi

# remove old Server/ServerActive lines and add new ones
sed -i '/^[[:space:]]*Server[[:space:]]*=.*/d' "$ZBX_CONF" || true
sed -i '/^[[:space:]]*ServerActive[[:space:]]*=.*/d' "$ZBX_CONF" || true
# ensure newline before appending
tail -c1 "$ZBX_CONF" | read -r _ || echo >> "$ZBX_CONF"
{
  echo "Server=${ZBX_SERVER_IP}"
  echo "ServerActive=${ZBX_SERVER_IP}"
} >> "$ZBX_CONF"

mkdir -p "$ZBX_D_DIR"

echo "== 4) Copying Zabbix configs and scripts =="
if [[ -d "${REPO_ROOT}/Zabbix" ]]; then
  cp -a "${REPO_ROOT}/Zabbix/." "$ZBX_D_DIR/"
else
  echo "WARNING: ${REPO_ROOT}/Zabbix folder not found. Skipping copy."
fi

if [[ -f "${ZBX_D_DIR}/script_4_zabbix.py" ]]; then
  chown root:root "${ZBX_D_DIR}/script_4_zabbix.py"
  chmod 0755 "${ZBX_D_DIR}/script_4_zabbix.py"
else
  echo "WARNING: ${ZBX_D_DIR}/script_4_zabbix.py not found. Skipping permissions setup."
fi

find "$ZBX_D_DIR" -type f -name "*.conf" -exec chmod 0644 {} \; -exec chown root:root {} \;

echo "== 5) Installing and starting systemd service start-eurotherm.service =="
UNIT_DST="/etc/systemd/system/start-eurotherm.service"
UNIT_SRC="$(find "$REPO_ROOT" -type f -name 'start-eurotherm.service' -print -quit)"

if [[ -n "${UNIT_SRC:-}" && -f "$UNIT_SRC" ]]; then
  echo "Found unit file: $UNIT_SRC"
  cp -a "$UNIT_SRC" "$UNIT_DST"
  chown root:root "$UNIT_DST"
  chmod 0644 "$UNIT_DST"
  systemctl daemon-reload
  systemctl enable --now start-eurotherm.service
  systemctl status start-eurotherm.service --no-pager || true
else
  echo "WARNING: start-eurotherm.service not found in repository (${REPO_ROOT}). Skipping installation."
fi

echo "== 6) Restarting and checking Zabbix Agent 2 =="
systemctl restart zabbix-agent2
systemctl enable zabbix-agent2 >/dev/null 2>&1 || true
systemctl status zabbix-agent2 --no-pager || true

echo "== Done =="
echo "• Zabbix Server/ServerActive: ${ZBX_SERVER_IP}"
echo "• Includes directory: ${ZBX_D_DIR}"
if systemctl is-enabled "$SERVICE_NAME" >/dev/null 2>&1; then
  echo "• Service ${SERVICE_NAME}: installed and running"
else
  echo "• Service ${SERVICE_NAME}: skipped (unit file not found)"
fi
