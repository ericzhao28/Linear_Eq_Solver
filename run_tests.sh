#!/usr/bin/env sh
# Run linear_solver on the tests directory.

for fname in tests/*.txt; do
  echo "Running test file $fname";
  echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>';
  python3 -m linear_solver "$fname";
  echo '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<';
  echo '';
done
