package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	args := os.Args[1:]

	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "[Error] You must enter the file name in the input arguments.")
		os.Exit(1)
	}

	switch args[0] {
	case "--texttomb":
		fmt.Println(encode(strings.Join(args[1:], " ")))
	case "--mbtotext":
		text, ok := decode(strings.Join(args[1:], " "))
		if !ok {
			fmt.Fprintln(os.Stderr, "[Error] Invalid ModernBinary encoding.")
			os.Exit(1)
		}
		fmt.Println(text)
	default:
		if !strings.HasSuffix(args[0], ".mb") {
			fmt.Fprintln(os.Stderr, "[Error] Your file format must be mb.")
			os.Exit(1)
		}
		data, err := os.ReadFile(args[0])
		if err != nil {
			fmt.Fprintf(os.Stderr, "[Error] %s\n", err)
			os.Exit(1)
		}
		newInterpreter(args[0]).run(string(data))
	}
}
