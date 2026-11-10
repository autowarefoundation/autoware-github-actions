#!/bin/bash
# Test the "Check if the build is needed" step of the check-if-build-is-needed workflow.
# Usage: test-check-if-build-is-needed.sh <the run script of the step>

set -euo pipefail

check_script=$(realpath "$1")
failures=0

repository=$(mktemp -d)
trap 'rm -rf "${repository}"' EXIT
cd "${repository}"
git init --quiet --initial-branch=main
git config user.name test
git config user.email test@example.com

mkdir -p pkg_a/src .github/workflows .github/actions/setup docs
echo '<package/>' >pkg_a/package.xml
echo a >pkg_a/src/a.cpp
echo a >CODEOWNERS
echo a >.github/workflows/build.yaml
echo a >.github/workflows/other.yaml
echo a >.github/actions/setup/action.yaml
git add --all
git commit --quiet --message base
# The step compares HEAD with origin/<base>.
git update-ref refs/remotes/origin/main HEAD

# test_case <name> <command that changes the repository> <build-inputs> <modified-packages> <expected> [<expected text>]
# <expected> is 'true' or 'false' (the result), or 'error' (the step must fail).
function test_case() {
    local name=$1 change=$2 build_inputs=$3 modified_packages=$4 expected=$5 expected_text=${6-}
    local output status=0 actual

    git checkout --quiet -B test main
    eval "${change}"
    git add --all
    git commit --quiet --allow-empty --message change

    output=$(GITHUB_BASE_REF=main GITHUB_OUTPUT=/dev/null BUILD_INPUTS="${build_inputs}" MODIFIED_PACKAGES="${modified_packages}" \
        bash --noprofile --norc -eo pipefail "${check_script}" 2>&1) || status=$?

    if [ "${status}" -ne 0 ]; then
        actual=error
    else
        actual=$(sed -n 's/^result=//p' <<<"${output}")
    fi

    if [ "${actual}" != "${expected}" ]; then
        echo "FAILED: ${name}: expected '${expected}', got '${actual}'"
    elif [ -n "${expected_text}" ] && ! grep -qF -- "${expected_text}" <<<"${output}"; then
        echo "FAILED: ${name}: the output does not contain '${expected_text}'"
    elif [ -z "${expected_text}" ] && grep -qE '::(warning|error)::' <<<"${output}"; then
        echo "FAILED: ${name}: the output has a warning or an error"
    else
        echo "passed: ${name}"
        return 0
    fi
    echo "${output}"
    failures=$((failures + 1))
}

build_inputs=$'  .github/workflows/build.yaml  \n\n# A comment\n.github/actions'

test_case "CODEOWNERS only" 'echo b >>CODEOWNERS' "${build_inputs}" "" false
test_case "no change" 'true' "${build_inputs}" "" false
test_case "another workflow" 'echo b >>.github/workflows/other.yaml' "${build_inputs}" "" false
test_case "build workflow" 'echo b >>.github/workflows/build.yaml' "${build_inputs}" "" true
test_case "build workflow, no build-inputs" 'echo b >>.github/workflows/build.yaml' "" "" false
test_case "file in a build input directory" 'echo b >>.github/actions/setup/action.yaml' "${build_inputs}" "" true
test_case "modified package" 'echo b >>pkg_a/src/a.cpp' "${build_inputs}" "pkg_a" true
test_case "package.xml, no build-inputs" 'echo b >>pkg_a/package.xml' "" "" true
test_case "deleted package, no build-inputs" 'git rm --quiet -r pkg_a' "" "" true
test_case "new COLCON_IGNORE, no build-inputs" 'touch pkg_a/COLCON_IGNORE' "" "" true
test_case "new AMENT_IGNORE, no build-inputs" 'touch pkg_a/AMENT_IGNORE' "" "" true
test_case "new CATKIN_IGNORE, no build-inputs" 'touch pkg_a/CATKIN_IGNORE' "" "" true
test_case "comment line that names the changed file" 'echo b >>CODEOWNERS' '# CODEOWNERS' "" false
test_case "pattern with a wildcard" 'echo b >>docs/a.md' '*.md' "" true
test_case "build input that the PR adds" 'echo b >new.repos' 'new.repos' "" true
test_case "pattern that matches no file" 'echo b >>.github/workflows/build.yaml' '.github/workflows/build.yml' "" false \
    "::warning::build-inputs: '.github/workflows/build.yml' matches no file."
test_case "build input that the PR deletes" 'git rm --quiet .github/workflows/build.yaml' '.github/workflows/build.yaml' "" true \
    "::warning::build-inputs: '.github/workflows/build.yaml' matches no file."
test_case "line that starts with a colon" 'git rm --quiet -r pkg_a' ':!*package.xml' "" error \
    "::error::build-inputs: a line must not start with ':'"
test_case "line that starts with spaces and a colon" 'echo b >>CODEOWNERS' '  :(exclude)CODEOWNERS' "" error \
    "::error::build-inputs: a line must not start with ':'"

if [ "${failures}" -ne 0 ]; then
    echo "${failures} test case(s) failed."
    exit 1
fi
echo "All test cases passed."
