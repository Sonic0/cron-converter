#!/usr/bin/env bash
set -euo pipefail
trap 'printf "ERROR: Release command failed at line %s.\n" "$LINENO" >&2' ERR

usage() {
  printf '%s\n' \
    'Usage: ./build_deploy.sh --build | --check | --test | --publish' \
    '  --build, --local  Build and check a wheel and source distribution in dist/.' \
    '  --check           Check the existing artifacts without rebuilding.' \
    '  --test            Check and upload the existing artifacts to TestPyPI.' \
    '  --publish         Check and upload the existing artifacts to PyPI.'
}

# Validate one release in dist/ and pass only its wheel and sdist to Twine.
check_artifacts() {
  local wheels=(dist/*.whl)
  local sdists=(dist/*.tar.gz)
  if (( ${#wheels[@]} != 1 || ${#sdists[@]} != 1 )); then
    printf 'ERROR: dist/ must contain exactly one wheel and one source distribution.\n' >&2
    return 1
  fi
  if [[ ! -f ${wheels[0]} || ! -f ${sdists[0]} || ${wheels[0]} != "${sdists[0]%.tar.gz}"-*-*-*.whl ]]; then
    printf 'ERROR: The wheel and source distribution in dist/ must be for the same release.\n' >&2
    return 1
  fi
  artifacts=("${wheels[0]}" "${sdists[0]}")
  python -m twine check --strict "${artifacts[@]}"
}

if (( $# != 1 )); then
  usage >&2
  exit 2
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
shopt -s nullglob dotglob
artifacts=()

case "$1" in
  --build|--local)
    dist_entries=(dist/*)
    if (( ${#dist_entries[@]} > 0 )); then
      printf 'ERROR: dist/ is not empty. Move the existing artifacts before building again.\n' >&2
      exit 1
    fi
    printf 'INFO: Building release artifacts in dist/.\n'
    python -m build --outdir dist
    check_artifacts
    ;;
  --check)
    check_artifacts
    ;;
  --test)
    check_artifacts
    python -m twine upload --repository-url https://test.pypi.org/legacy/ "${artifacts[@]}"
    ;;
  --publish)
    check_artifacts
    python -m twine upload --repository pypi "${artifacts[@]}"
    ;;
  -h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
