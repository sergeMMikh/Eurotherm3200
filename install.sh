#!/usr/bin/env bash
set -euo pipefail

# === settings ===
ZBX_SERVER_IP="192.168.1.160"
ZBX_CONF="/etc/zabbix/zabbix_agent2.conf"
ZBX_D_DIR="/etc/zabbix/zabbix_agent2.d"
SERVICE_NAME="start-eurotherm.service"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

need_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "Перезапускаю от root..."
    exec sudo -E bash "$0" "$@"
  fi
}
need_root "$@"

echo "== 1) Обновление пакетов и установка зависимостей =="
apt-get update -y
# zabbix-agent2 из репозиториев + базовые инструменты
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip zabbix-agent2

echo "== 2) Установка Python-библиотеки minimalmodbus (системно) =="
python3 -m pip install --upgrade pip
# В некоторых системах потребуется --break-system-packages; раскомментируй при необходимости:
# python3 -m pip install --break-system-packages minimalmodbus
python3 -m pip install minimalmodbus

echo "== 3) Конфигурирование Zabbix Agent 2 =="
if [[ -f "$ZBX_CONF" ]]; then
  cp -a "$ZBX_CONF" "${ZBX_CONF}.bak.$(date +%F_%H%M%S)"
fi

# Гарантируем наличие Server и ServerActive с нужным IP (удалим старые и добавим новые)
sed -i '/^[[:space:]]*Server[[:space:]]*=.*/d' "$ZBX_CONF" || true
sed -i '/^[[:space:]]*ServerActive[[:space:]]*=.*/d' "$ZBX_CONF" || true
{
  echo "Server=${ZBX_SERVER_IP}"
  echo "ServerActive=${ZBX_SERVER_IP}"
} >> "$ZBX_CONF"

# Убедимся, что директория под инклуды существует
mkdir -p "$ZBX_D_DIR"

echo "== 4) Копирование Zabbix-конфигов и скриптов =="
# Ожидается, что в репо есть папка Zabbix с .conf/.py
if [[ -d "${REPO_ROOT}/Zabbix" ]]; then
  cp -a "${REPO_ROOT}/Zabbix/." "$ZBX_D_DIR/"
else
  echo "WARNING: Папка ${REPO_ROOT}/Zabbix не найдена. Пропускаю копирование."
fi

# Права для скрипта script_4_zabbix.py (если есть)
if [[ -f "${ZBX_D_DIR}/script_4_zabbix.py" ]]; then
  chown root:root "${ZBX_D_DIR}/script_4_zabbix.py"
  chmod 0755 "${ZBX_D_DIR}/script_4_zabbix.py"
else
  echo "WARNING: ${ZBX_D_DIR}/script_4_zabbix.py не найден. Пропускаю установку прав."
fi

# Проставим корректные права на конфиги
find "$ZBX_D_DIR" -type f -name "*.conf" -exec chmod 0644 {} \; -exec chown root:root {} \;

echo "== 5) Установка и запуск systemd-сервиса start-eurotherm.service =="
UNIT_SRC="${REPO_ROOT}/${SERVICE_NAME}"
UNIT_DST="/etc/systemd/system/${SERVICE_NAME}"

if [[ -f "$UNIT_SRC" ]]; then
  cp -a "$UNIT_SRC" "$UNIT_DST"
  chown root:root "$UNIT_DST"
  chmod 0644 "$UNIT_DST"
  systemctl daemon-reload
  systemctl enable --now "$SERVICE_NAME"
  systemctl status "$SERVICE_NAME" --no-pager || true
else
  echo "WARNING: Юнит ${SERVICE_NAME} не найден в репозитории (${UNIT_SRC}). Пропускаю установку сервиса."
fi

echo "== 6) Перезапуск и проверка Zabbix Agent 2 =="
systemctl restart zabbix-agent2
systemctl enable zabbix-agent2 >/dev/null 2>&1 || true
systemctl status zabbix-agent2 --no-pager || true

echo "== Готово =="
echo "• Zabbix Server/ServerActive: ${ZBX_SERVER_IP}"
echo "• Инклуды: ${ZBX_D_DIR}"
if systemctl is-enabled "$SERVICE_NAME" >/dev/null 2>&1; then
  echo "• Сервис ${SERVICE_NAME}: установлен и запущен"
else
  echo "• Сервис ${SERVICE_NAME}: пропущен (юнит не найден)"
fi
