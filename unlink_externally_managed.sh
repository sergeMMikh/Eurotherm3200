#!/usr/bin/env bash
set -euo pipefail

AUTO_YES="${1:-}"

need_root() {
  if [[ $EUID -ne 0 ]]; then
    exec sudo -E bash "$0" "$@"
  fi
}
need_root "$@"

targets=()
# Ищем файлы для всех python3.* в стандартных путях
for base in /usr/lib /usr/local/lib; do
  [[ -d "$base" ]] || continue
  while IFS= read -r -d '' f; do
    targets+=("$f")
  done < <(find "$base" -maxdepth 1 -type d -name 'python3.*' -print0 2>/dev/null | \
           xargs -0 -I{} bash -c '[[ -f "{}/EXTERNALLY-MANAGED" ]] && printf "%s\0" "{}/EXTERNALLY-MANAGED" || true')
done

if [[ ${#targets[@]} -eq 0 ]]; then
  echo "EXTERNALLY-MANAGED не найден ни для одной версии python3 в /usr/lib или /usr/local/lib."
  exit 0
fi

echo "Найдены файлы:"
printf '  %s\n' "${targets[@]}"

if [[ "$AUTO_YES" != "-y" ]]; then
  read -r -p "Удалить все перечисленные файлы? [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || { echo "Отменено."; exit 1; }
fi

ok=0; err=0
for f in "${targets[@]}"; do
  if rm -f -- "$f"; then
    echo "✓ Удалён: $f"; ((ok++)) || true
  else
    echo "✗ Ошибка удаления: $f" >&2; ((err++)) || true
  fi
done

echo "Готово. Успешно: $ok, ошибок: $err"
