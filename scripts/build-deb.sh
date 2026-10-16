#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE_NAME="linux-system-diagnostics"
VERSION="1.0.0"
PACKAGE_DIR="${ROOT_DIR}/packaging"
OUTPUT_FILE="${ROOT_DIR}/${PACKAGE_NAME}_${VERSION}_all.deb"

fail() {
    echo "Error: $*" >&2
    exit 1
}

if ! command -v dpkg-deb >/dev/null 2>&1; then
    fail "dpkg-deb is required to build the Debian package."
fi

for file in cli.py log_analyzer.py main.py; do
    [[ -f "${ROOT_DIR}/${file}" ]] ||
        fail "Required source file is missing: ${file}"
done

[[ -f "${PACKAGE_DIR}/DEBIAN/control" ]] ||
    fail "Debian control file is missing."

install -m 644 "${ROOT_DIR}/cli.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/cli.py"
install -m 644 "${ROOT_DIR}/log_analyzer.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/log_analyzer.py"
install -m 644 "${ROOT_DIR}/main.py" \
    "${PACKAGE_DIR}/usr/lib/${PACKAGE_NAME}/main.py"

dpkg-deb --root-owner-group --build "${PACKAGE_DIR}" "${OUTPUT_FILE}"

CONTROL="$(dpkg-deb --field "${OUTPUT_FILE}" Package)"
VERSION_ACTUAL="$(dpkg-deb --field "${OUTPUT_FILE}" Version)"
ARCHITECTURE="$(dpkg-deb --field "${OUTPUT_FILE}" Architecture)"

[[ "${CONTROL}" == "${PACKAGE_NAME}" ]] ||
    fail "Unexpected package name: ${CONTROL}"

[[ "${VERSION_ACTUAL}" == "${VERSION}" ]] ||
    fail "Unexpected package version: ${VERSION_ACTUAL}"

[[ "${ARCHITECTURE}" == "all" ]] ||
    fail "Unexpected package architecture: ${ARCHITECTURE}"

CONTENTS="$(dpkg-deb --contents "${OUTPUT_FILE}")"

for expected in \
    "./usr/bin/linux-system-diagnostics" \
    "./usr/lib/${PACKAGE_NAME}/cli.py" \
    "./usr/lib/${PACKAGE_NAME}/log_analyzer.py" \
    "./usr/lib/${PACKAGE_NAME}/main.py"; do
    grep -Fq "${expected}" <<< "${CONTENTS}" ||
        fail "Expected package file is missing: ${expected}"
done

echo "Package built and validated successfully:"
echo "  File:         ${OUTPUT_FILE}"
echo "  Package:      ${CONTROL}"
echo "  Version:      ${VERSION_ACTUAL}"
echo "  Architecture: ${ARCHITECTURE}"
