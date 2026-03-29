#!/bin/bash
# Validation script for test-u3x32k.md
# Checks: UTF-8 encoding without BOM, Unix LF line endings, file size 300-600 bytes, no trailing whitespace

set -e

FILE="test-u3x32k.md"

if [ ! -f "$FILE" ]; then
    echo "❌ Error: File '$FILE' not found"
    exit 1
fi

echo "Validating: $FILE"
echo "=========================================="
echo ""

# 1. Check UTF-8 encoding
echo "1. Checking character encoding..."
ENCODING=$(file --mime-encoding "$FILE" | cut -d' ' -f2)
# UTF-8 is backwards compatible with ASCII, so ASCII files are valid UTF-8 files
if [ "$ENCODING" = "utf-8" ] || [ "$ENCODING" = "us-ascii" ]; then
    echo "   ✓ File is UTF-8 encoded (detected as $ENCODING)"
else
    echo "   ❌ File encoding is $ENCODING (expected utf-8 or us-ascii)"
    exit 1
fi

# 2. Check for BOM (Byte Order Mark)
echo "2. Checking for BOM (Byte Order Mark)..."
BOM_CHECK=$(od -An -tx1 -N3 "$FILE" | tr -d ' ')
if [ "$BOM_CHECK" = "efbbbf" ]; then
    echo "   ❌ File has UTF-8 BOM (EF BB BF) - should not have BOM"
    exit 1
else
    echo "   ✓ No BOM detected"
fi

# 3. Check line endings (LF vs CRLF)
echo "3. Checking line endings..."
FILE_INFO=$(file "$FILE")
if echo "$FILE_INFO" | grep -q "CRLF"; then
    echo "   ❌ File has Windows CRLF line endings (should be Unix LF)"
    exit 1
elif echo "$FILE_INFO" | grep -q "CR line terminators"; then
    echo "   ❌ File has Mac CR line endings (should be Unix LF)"
    exit 1
else
    echo "   ✓ File uses Unix LF line endings"
fi

# 4. Check file size (300-600 bytes)
echo "4. Checking file size..."
FILE_SIZE=$(wc -c < "$FILE")
if [ "$FILE_SIZE" -ge 300 ] && [ "$FILE_SIZE" -le 600 ]; then
    echo "   ✓ File size is $FILE_SIZE bytes (within 300-600 range)"
else
    echo "   ❌ File size is $FILE_SIZE bytes (outside 300-600 range)"
    exit 1
fi

# 5. Check for trailing whitespace
echo "5. Checking for trailing whitespace..."
TRAILING=$(grep -n ' $' "$FILE" || true)
if [ -z "$TRAILING" ]; then
    echo "   ✓ No trailing whitespace detected"
else
    echo "   ❌ Trailing whitespace found on:"
    echo "$TRAILING" | sed 's/^/      /'
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ All validation checks passed!"
echo "=========================================="
