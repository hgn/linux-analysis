#!/bin/bash

r2 -e bin.relocs.apply=true -e bin.cache=true ./coffee-machine-sim << EOF
aaa
agCd > output.dot
q
EOF

dot -Tpng -Gdpi=300 -o callgraph.png output.dot

