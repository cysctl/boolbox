#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"

ALGS=("PRESENT" "GIFT")

for ALG in "${ALGS[@]}"; do
    echo "Processing $ALG..."
    
    SBOX_FILE="$SCRIPT_DIR/$ALG/sbox.txt"
    ANF_IMG="$SCRIPT_DIR/$ALG/anf_equations.png"
    QC_IMG="$SCRIPT_DIR/$ALG/circuit.png"
    ANF_TXT="$SCRIPT_DIR/$ALG/anf_equations.txt"
    
    echo "  Generating ANF equations..."
    cat "$SBOX_FILE" | boolbox anf - -f image -o "$ANF_IMG"
    
    echo "  Generating Quantum circuit..."
    cat "$SBOX_FILE" | boolbox qcircuit - -f image -o "$QC_IMG"
    
    cat "$SBOX_FILE" | boolbox anf - -f text > "$ANF_TXT"
    
    echo "  $ALG complete."
done