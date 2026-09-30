#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIRECTORY="${SOURCE_DIRECTORY}/fixture_package"
mkdir -p "${PACKAGE_DIRECTORY}/checks/test"
cat >"${PACKAGE_DIRECTORY}/package.xml" <<'EOF'
<?xml version="1.0"?>
<package format="3">
  <name>clang_tidy_source_fixture</name>
  <version>0.0.0</version>
  <description>Fixture for clang-tidy source directory tests.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>Apache-2.0</license>
  <buildtool_depend>cmake</buildtool_depend>
  <export><build_type>cmake</build_type></export>
</package>
EOF
cat >"${PACKAGE_DIRECTORY}/CMakeLists.txt" <<'EOF'
cmake_minimum_required(VERSION 3.16)
project(clang_tidy_source_fixture LANGUAGES CXX)
add_library(fixture OBJECT
  checks/checked.cpp
  checks/ignored.cpp
  checks/wildcard_ignored.cpp
  checks/test/ignored_test.cpp
)
EOF
printf 'int *checked = nullptr;\n' >"${PACKAGE_DIRECTORY}/checks/checked.cpp"
printf 'int *ignored = 0;\n' >"${PACKAGE_DIRECTORY}/checks/ignored.cpp"
printf 'int *wildcard_ignored = 0;\n' >"${PACKAGE_DIRECTORY}/checks/wildcard_ignored.cpp"
printf 'int *ignored_test = 0;\n' >"${PACKAGE_DIRECTORY}/checks/test/ignored_test.cpp"
printf 'fixture_package/checks/ignored.cpp\n*/wildcard_ignored.cpp\n' >"${SOURCE_DIRECTORY}/.clang-tidy-ignore"
# This invalid local config must be replaced by the selected download.
printf 'Checks: "-*"\n' >"${SOURCE_DIRECTORY}/.clang-tidy"
printf 'Checks: "-*,modernize-use-nullptr"\nWarningsAsErrors: "*"\n' >"${RUNNER_TEMP}/source-directory-clang-tidy.yaml"
