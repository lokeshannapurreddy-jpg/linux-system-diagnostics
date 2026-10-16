#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE_NAME="linux-system-diagnostics"
VERSION="1.0.0"
PACKAGE_DIR="${ROOT_DIR}/packaging"
OUTPUT_FILE="${ROOT_DIR}/${PACKAGE_NAME}_${VERSION}_all.deb"

if ! command -v dpkg-deb >/dev/null 2>&1; then
    echo "Error: dpkg-deb is required to build the Debian package." >&2
    exit 1
fi

for file in cli.py log_analyzer.py main.py; do
    if [[ ! -f "${ROOT_DIR}/${file}" ]]; then
        echo "Error: required source file is missing: ${file}" >&2
        exit 1
    fi
done

install -m 644 "${ROOT_DIR}/cli.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/cli.py"
install -m 644 "${ROOT_DIR}/log_analyzer.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/log_analyzer.py"
install -m 644 "${ROOT_DIR}/main.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/main.py"

dpkg-deb --root-owner-group --build "${PACKAGE_DIR}" "${OUTPUT_FILE}"

dpkg-deb --info "${OUTPUT_FILE}" >/dev/null
dpkg-deb --contents "${OUTPUT_FILE}" >/dev/null

echo "Package built and inspected successfully: ${OUTPUT_FILE}"
