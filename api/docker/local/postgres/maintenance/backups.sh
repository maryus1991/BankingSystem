#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

working_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${working_dir}/_sourced/constants.sh"
source "${working_dir}/_sourced/messages.sh"

message_welcome "These are the backups that you have created so far:"

printf "%-21s   %-7s   %s\n" "Timestamp" "Size" "Filename"
echo "---------------------   -------   -----------------------------------"

if [[ ! -d "${BACKUP_DIR_PATH}" ]] || [[ -z "$(ls -A "${BACKUP_DIR_PATH}" 2>/dev/null)" ]]; then
    message_info "No backup files found in '${BACKUP_DIR_PATH}'."
    exit 0
fi

ls -lht "${BACKUP_DIR_PATH}" | awk 'NR>1 {
    timestamp = $6" "$7" "$8
    size = $5
    filename = $9
    printf "%-21s   %-7s   %s\n", timestamp, size, filename
}'
