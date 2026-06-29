package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// ── AST ──────────────────────────────────────────────────────────────────────

type nodeKind int

const (
	nodeCmd     nodeKind = iota // (action)=(value) or (action)=([callVar])
	nodeAssign                  // [varName]=[value] or [varName]=([callVar])
	nodeFuncDef                 // *funcName*{ body }
	nodeFuncCall                // [*funcName*]
	nodeIf                      // : condLeft op condRight { body }
	nodeWhile                   // :: condLeft op condRight { body }
	nodeFor                     // ~binaryCount~{ body }
)

type node struct {
	kind      nodeKind
	line      int
	action    string
	value     string
	callVar   string
	varName   string
	funcName  string
	body      []*node
	condLeft  string // nodeIf / nodeWhile
	condOp    string
	condRight string
	count     string // nodeFor: binary integer (e.g. "101" = 5)
}

// ── interpreter ──────────────────────────────────────────────────────────────

type interpreter struct {
	fileName string
	vars     map[string]string
	funcs    map[string][]*node
}

func newInterpreter(fileName string) *interpreter {
	return &interpreter{
		fileName: fileName,
		vars:     make(map[string]string),
		funcs:    make(map[string][]*node),
	}
}

func (inp *interpreter) fail(line int, kind, msg string) {
	fmt.Fprintf(os.Stderr, "[ERROR] File \"%s\", line %d\n%s: %s\n", inp.fileName, line, kind, msg)
	os.Exit(1)
}

func (inp *interpreter) run(source string) {
	inp.exec(inp.parse(source))
}

// ── scanner ──────────────────────────────────────────────────────────────────

type scanner struct {
	src  []rune
	pos  int
	line int
}

func newScanner(src string) *scanner {
	return &scanner{src: []rune(src), pos: 0, line: 1}
}

func (s *scanner) eof() bool { return s.pos >= len(s.src) }

func (s *scanner) peek() rune {
	if s.eof() {
		return 0
	}
	return s.src[s.pos]
}

// next advances past the current rune and returns it.
// Returns 0 safely when called at EOF, matching the behaviour of peek().
func (s *scanner) next() rune {
	if s.eof() {
		return 0
	}
	ch := s.src[s.pos]
	s.pos++
	if ch == '\n' {
		s.line++
	}
	return ch
}

func (s *scanner) skipWS() {
	for !s.eof() {
		if ch := s.peek(); ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n' {
			s.next()
		} else {
			break
		}
	}
}

func (s *scanner) skipSpaces() {
	for !s.eof() {
		if ch := s.peek(); ch == ' ' || ch == '\t' || ch == '\r' {
			s.pos++
		} else {
			break
		}
	}
}

// collectUntil returns all runes up to (not including) the first delimiter hit.
func (s *scanner) collectUntil(delimiters ...rune) string {
	var buf []rune
	for !s.eof() {
		ch := s.peek()
		for _, d := range delimiters {
			if ch == d {
				return string(buf)
			}
		}
		buf = append(buf, s.next())
	}
	return string(buf)
}

// ── parser ───────────────────────────────────────────────────────────────────

func (inp *interpreter) parse(source string) []*node {
	return inp.parseBlock(newScanner(source))
}

// parseBlock parses statements until EOF or an unmatched '}' is hit.
func (inp *interpreter) parseBlock(s *scanner) []*node {
	var nodes []*node
	for !s.eof() {
		s.skipWS()
		if s.eof() || s.peek() == '}' {
			break
		}
		if n := inp.parseStatement(s); n != nil {
			nodes = append(nodes, n)
		}
	}
	return nodes
}

func (inp *interpreter) parseStatement(s *scanner) *node {
	line := s.line
	ch := s.peek()
	// '::' must be checked before ':'; '[*' before '['.
	switch {
	case ch == '*':
		return inp.parseFuncDef(s, line)
	case ch == '[' && s.pos+1 < len(s.src) && s.src[s.pos+1] == '*':
		return inp.parseFuncCall(s, line)
	case ch == ':' && s.pos+1 < len(s.src) && s.src[s.pos+1] == ':':
		return inp.parseWhile(s, line)
	case ch == ':':
		return inp.parseIf(s, line)
	case ch == '~':
		return inp.parseFor(s, line)
	case ch == '(':
		return inp.parseCmd(s, line)
	case ch == '[':
		return inp.parseAssign(s, line)
	default:
		s.next()
		return nil
	}
}

// parseCondition splits a raw condition string into (left, op, right).
// Operators are matched longest-first to avoid >= being split as >.
// Tries " op " (with surrounding spaces) first, then falls back to bare match.
func (inp *interpreter) parseCondition(raw string, line int) (left, op, right string) {
	raw = strings.TrimSpace(raw)
	for _, o := range operators {
		if idx := strings.Index(raw, " "+o+" "); idx != -1 {
			return strings.TrimSpace(raw[:idx]), o, strings.TrimSpace(raw[idx+len(o)+2:])
		}
	}
	for _, o := range operators {
		if idx := strings.Index(raw, o); idx != -1 {
			return strings.TrimSpace(raw[:idx]), o, strings.TrimSpace(raw[idx+len(o):])
		}
	}
	inp.fail(line, "ConditionError", "no valid operator in condition: "+raw)
	return
}

func (inp *interpreter) parseFuncDef(s *scanner, line int) *node {
	s.next() // consume opening *
	name := strings.TrimSpace(s.collectUntil('*'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in function name")
	}
	s.next() // consume closing *
	s.skipWS()
	if s.eof() || s.peek() != '{' {
		inp.fail(line, "MBSyntaxError", "expected '{' after function name")
	}
	s.next() // consume {
	body := inp.parseBlock(s)
	if s.eof() || s.peek() != '}' {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in function body")
	}
	s.next() // consume }
	return &node{kind: nodeFuncDef, line: line, funcName: name, body: body}
}

func (inp *interpreter) parseFuncCall(s *scanner, line int) *node {
	s.next() // consume [
	s.next() // consume *
	name := strings.TrimSpace(s.collectUntil('*'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in function call")
	}
	s.next() // consume *
	if s.eof() || s.peek() != ']' {
		inp.fail(line, "MBSyntaxError", "expected ']' to close function call")
	}
	s.next() // consume ]
	return &node{kind: nodeFuncCall, line: line, funcName: name}
}

func (inp *interpreter) parseIf(s *scanner, line int) *node {
	s.next() // consume :
	s.skipSpaces()
	rawCond := strings.TrimSpace(s.collectUntil('{'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in if condition")
	}
	s.next() // consume {
	left, op, right := inp.parseCondition(rawCond, line)
	body := inp.parseBlock(s)
	if s.eof() || s.peek() != '}' {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in if body")
	}
	s.next() // consume }
	return &node{kind: nodeIf, line: line, condLeft: left, condOp: op, condRight: right, body: body}
}

func (inp *interpreter) parseWhile(s *scanner, line int) *node {
	s.next() // consume first :
	s.next() // consume second :
	s.skipSpaces()
	rawCond := strings.TrimSpace(s.collectUntil('{'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in while condition")
	}
	s.next() // consume {
	left, op, right := inp.parseCondition(rawCond, line)
	body := inp.parseBlock(s)
	if s.eof() || s.peek() != '}' {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in while body")
	}
	s.next() // consume }
	return &node{kind: nodeWhile, line: line, condLeft: left, condOp: op, condRight: right, body: body}
}

func (inp *interpreter) parseFor(s *scanner, line int) *node {
	s.next() // consume opening ~
	count := strings.TrimSpace(s.collectUntil('~'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in for count")
	}
	s.next() // consume closing ~
	s.skipWS()
	if s.eof() || s.peek() != '{' {
		inp.fail(line, "MBSyntaxError", "expected '{' after for count")
	}
	s.next() // consume {
	body := inp.parseBlock(s)
	if s.eof() || s.peek() != '}' {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in for body")
	}
	s.next() // consume }
	return &node{kind: nodeFor, line: line, count: count, body: body}
}

func (inp *interpreter) parseCmd(s *scanner, line int) *node {
	s.next() // consume (
	action := strings.TrimSpace(s.collectUntil(')'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in action")
	}
	s.next() // consume )
	s.skipSpaces()
	if s.eof() || s.peek() != '=' {
		inp.fail(line, "MBSyntaxError", "expected '=' after action")
	}
	s.next() // consume =
	s.skipSpaces()
	val, call := inp.parseRvalue(s, line)
	return &node{kind: nodeCmd, line: line, action: action, value: val, callVar: call}
}

func (inp *interpreter) parseAssign(s *scanner, line int) *node {
	s.next() // consume [
	varName := strings.TrimSpace(s.collectUntil(']'))
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "unexpected EOF in variable name")
	}
	if varName == "" {
		inp.fail(line, "MBSyntaxError", "variable name cannot be empty")
	}
	s.next() // consume ]
	s.skipSpaces()
	if s.eof() || s.peek() != '=' {
		inp.fail(line, "MBSyntaxError", "expected '=' after variable name")
	}
	s.next() // consume =
	s.skipSpaces()
	val, call := inp.parseRvalue(s, line)
	return &node{kind: nodeAssign, line: line, varName: varName, value: val, callVar: call}
}

// parseRvalue parses the right-hand side of a statement.
//
//	([varname])  →  callVar = varname  (variable reference)
//	(value)      →  value = literal binary-encoded string
//	[value]      →  value = literal binary-encoded string
func (inp *interpreter) parseRvalue(s *scanner, line int) (value, callVar string) {
	if s.eof() {
		inp.fail(line, "MBSyntaxError", "expected value")
	}
	switch s.peek() {
	case '(':
		s.next() // consume (
		s.skipSpaces()
		if !s.eof() && s.peek() == '[' {
			s.next() // consume [
			callVar = strings.TrimSpace(s.collectUntil(']'))
			if s.eof() {
				inp.fail(line, "MBSyntaxError", "unexpected EOF in variable call")
			}
			s.next() // consume ]
			s.skipSpaces()
			if s.eof() || s.peek() != ')' {
				inp.fail(line, "MBSyntaxError", "expected ')' to close variable call")
			}
			s.next() // consume )
			return "", callVar
		}
		value = strings.TrimSpace(s.collectUntil(')'))
		if s.eof() {
			inp.fail(line, "MBSyntaxError", "unexpected EOF in value")
		}
		s.next() // consume )
		return value, ""
	case '[':
		s.next() // consume [
		value = strings.TrimSpace(s.collectUntil(']'))
		if s.eof() {
			inp.fail(line, "MBSyntaxError", "unexpected EOF in value")
		}
		s.next() // consume ]
		return value, ""
	default:
		inp.fail(line, "MBSyntaxError", fmt.Sprintf("unexpected character '%c' in value", s.peek()))
		return
	}
}

// ── executor ─────────────────────────────────────────────────────────────────

func (inp *interpreter) exec(nodes []*node) {
	for _, n := range nodes {
		inp.execNode(n)
	}
}

func (inp *interpreter) execNode(n *node) {
	switch n.kind {

	case nodeFuncDef:
		inp.funcs[n.funcName] = n.body

	case nodeFuncCall:
		body, ok := inp.funcs[n.funcName]
		if !ok {
			inp.fail(n.line, "UnDefineError",
				fmt.Sprintf("function '%s' is not defined", safeDecode(n.funcName)))
		}
		inp.exec(body)

	case nodeAssign:
		if n.callVar != "" {
			val, ok := inp.vars[n.callVar]
			if !ok {
				inp.fail(n.line, "UnDefineError",
					fmt.Sprintf("variable '%s' is not defined", safeDecode(n.callVar)))
			}
			inp.vars[n.varName] = val
		} else {
			inp.vars[n.varName] = n.value
		}

	case nodeCmd:
		fn, ok := base[n.action]
		if !ok {
			inp.fail(n.line, "UnknownCommand",
				fmt.Sprintf("'%s' is not defined", n.action))
		}
		var encoded string
		if n.callVar != "" {
			val, ok := inp.vars[n.callVar]
			if !ok {
				inp.fail(n.line, "UnDefineError",
					fmt.Sprintf("variable '%s' is not defined", safeDecode(n.callVar)))
			}
			encoded = val
		} else {
			encoded = n.value
		}
		text, ok := decode(encoded)
		if !ok {
			inp.fail(n.line, "MBSyntaxError",
				fmt.Sprintf("invalid binary encoding: %s", encoded))
		}
		inp.callBuiltin(fn, text, n.line)

	case nodeIf:
		left := inp.resolveCondSide(n.condLeft, n.line)
		right := inp.resolveCondSide(n.condRight, n.line)
		if comparePair(left, right, n.condOp) {
			inp.exec(n.body)
		}

	case nodeWhile:
		for {
			left := inp.resolveCondSide(n.condLeft, n.line)
			right := inp.resolveCondSide(n.condRight, n.line)
			if !comparePair(left, right, n.condOp) {
				break
			}
			inp.exec(n.body)
		}

	case nodeFor:
		count, err := strconv.ParseInt(n.count, 2, 64)
		if err != nil || count < 0 {
			inp.fail(n.line, "MBSyntaxError", "invalid for count: "+n.count)
		}
		for i := int64(0); i < count; i++ {
			inp.exec(n.body)
		}
	}
}

func (inp *interpreter) callBuiltin(fn, arg string, line int) {
	switch fn {
	case "print":
		fmt.Print(arg)
	case "input":
		fmt.Print(arg)
		var s string
		fmt.Scanln(&s)
	case "len":
		fmt.Print(len([]rune(arg)))
	default:
		inp.fail(line, "UnknownCommand", fn+" is not defined")
	}
}

// resolveCondSide resolves one side of a condition to a comparable string.
//
//	[varname] → look up variable and decode its binary value
//	binary    → decode directly
//	other     → return as-is
func (inp *interpreter) resolveCondSide(side string, line int) string {
	side = strings.TrimSpace(side)
	if strings.HasPrefix(side, "[") && strings.HasSuffix(side, "]") {
		varName := strings.TrimSpace(side[1 : len(side)-1])
		if varName == "" {
			inp.fail(line, "MBSyntaxError", "variable name cannot be empty in condition")
		}
		val, ok := inp.vars[varName]
		if !ok {
			inp.fail(line, "UnDefineError",
				"variable '"+safeDecode(varName)+"' is not defined in condition")
		}
		text, ok := decode(val)
		if !ok {
			inp.fail(line, "MBSyntaxError",
				fmt.Sprintf("invalid binary encoding in variable '%s'", safeDecode(varName)))
		}
		return text
	}
	return decodeIfBinary(side)
}

// decodeIfBinary decodes a string if it contains only binary digits and spaces.
// Returns the original string unchanged if decoding fails or produces empty output.
func decodeIfBinary(s string) string {
	for _, ch := range s {
		if ch != '0' && ch != '1' && ch != ' ' {
			return s
		}
	}
	if d, ok := decode(s); ok && d != "" {
		return d
	}
	return s
}

func comparePair(left, right, op string) bool {
	switch op {
	case "==":
		return left == right
	case "!=":
		return left != right
	case "<":
		return left < right
	case "<=":
		return left <= right
	case ">":
		return left > right
	case ">=":
		return left >= right
	}
	return false
}

// safeDecode decodes a binary-encoded string for use in error messages.
// Falls back to the raw string if decoding fails.
func safeDecode(s string) string {
	if d, ok := decode(s); ok && d != "" {
		return d
	}
	return s
}
