#!/bin/bash
# Sum of two numbers with validation

read -p "Enter first number: " num1
read -p "Enter second number: " num2

# Check if inputs are integers
if ! [[ "$num1" =~ ^-?[0-9]+$ && "$num2" =~ ^-?[0-9]+$ ]]; then
    echo "Error: Please enter valid integers."
    exit 1
fi

sum=$((num1 + num2))
echo "Sum: $sum"
