#!/bin/bash
set -e
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
readonly SOURCE_ROOT="${SCRIPT_DIR}/../.."

function compile() {
  local filename="${1}"
  local proto_path="protos"
  local src="protos/langbot/common/${filename}"
  local dst="src"

  cd "${SOURCE_ROOT}/src/common"
  if [[ ! -f "${src}" ]]; then
    echo 1>&2 "Proto file doesn't exist: ${src}"
    exit 1
  fi
  python -m grpc_tools.protoc -I "./${proto_path}" --python_out="./${dst}" --grpc_python_out="./${dst}" "./${src}"
}

function usage() {
  cat <<EOUSAGE
Usage: $(basename $0) COMMAND [OPTIONS]

 compile       Compile proto files into python script

EOUSAGE
}

function main() {
  while getopts "h" flag; do
    case "${flag}" in
      h)
        usage
        exit 0
        ;;
      \?) exit 1 ;;
    esac
  done

  shift  $(($OPTIND - 1))
  subcommand=$1; shift
  unset OPTIND
  case "${subcommand}" in
    compile) compile $@ ;;
    *)
      [ ! -z ${subcommand} ] && echo "Invalid subcommand: ${subcommand}"
      exit 1
      ;;
  esac
}

main "$@"
