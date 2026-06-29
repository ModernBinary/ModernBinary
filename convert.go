package main

import (
	"strconv"
	"strings"
)

// encode converts a plain-text string into the ModernBinary format:
// each character's ASCII value is multiplied by its 1-based position,
// then expressed as a binary number. Tokens are space-separated.
func encode(text string) string {
	runes := []rune(strings.TrimSpace(text))
	if len(runes) == 0 {
		return ""
	}
	tokens := make([]string, len(runes))
	for i, r := range runes {
		tokens[i] = strconv.FormatInt(int64(r)*int64(i+1), 2)
	}
	return strings.Join(tokens, " ")
}

// decode reverses encode: it splits the space-separated binary string,
// parses each token as a base-2 integer, and divides by its 1-based position
// to recover the original ASCII value.
// Returns ("", false) if any token is invalid binary or maps outside [0, 127].
func decode(encoded string) (string, bool) {
	tokens := strings.Fields(strings.TrimSpace(encoded))
	if len(tokens) == 0 {
		return "", true
	}
	result := make([]byte, len(tokens))
	for i, token := range tokens {
		bits, err := strconv.ParseInt(token, 2, 64)
		if err != nil {
			return "", false
		}
		ascii := int(bits) / (i + 1)
		if ascii < 0 || ascii > 127 {
			return "", false
		}
		result[i] = byte(ascii)
	}
	return string(result), true
}
