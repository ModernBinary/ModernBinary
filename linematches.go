package main

// operators are checked longest-first to avoid >= being matched as >.
var operators = []string{"==", "!=", ">=", "<=", "<", ">"}

// builtins lists every built-in function name.
// The action code a caller uses in .mb source is encode(name[0]),
// so the binary dispatch key is derived automatically in init().
var builtins = []string{"print", "input", "len"}

// base maps binary action codes → built-in function names.
// Populated at startup from builtins so keys never go out of sync with encode().
var base map[string]string

func init() {
	base = make(map[string]string, len(builtins))
	for _, name := range builtins {
		key := encode(string([]rune(name)[0]))
		base[key] = name
	}
}
