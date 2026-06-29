<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Getting Started With ModernBinary</h1>
</div>
<div align="center">
</div><br>

## Building from source

ModernBinary is written in Go. To build the interpreter locally:

```bash
git clone https://github.com/ModernBinary/ModernBinary.git
cd ModernBinary
go build -o modernbinary .
```

Run a `.mb` file:

```bash
./modernbinary yourfile.mb
```

Convert text to ModernBinary encoding and back:

```bash
./modernbinary --texttomb "Hello"
./modernbinary --mbtotext "1001000 11001010 101000100 110110000 1000101011"
```

You can also use the [online code playground](https://modernbinary.github.io/ModernBinary/playground) to run code without building.

Now you need to know how characters are translated and convert in modern binary. The modern binary code playground has the ability to convert text to binary modern, but to know how to do this, you can read [how to convert characters](https://modernbinary.github.io/ModernBinary/translate).

## Let's print Hello, World!
Calling and executing commands in modern binary is in the form ```(action_number)=(argv)```.
Each command has a ``action_number`` for calling and then we enter arguments in ``argv`` if needed.
Let's start with the simplest command, print!
The ``action_number`` of the print command is ``1110000`` (112 in decimal, the ASCII code of ``p`` — the first character of the phrase print).
Then in argv we can translate our text into modern binary format and then put it in it.
### Example :
Let's print the phrase ``Hi``, which in modern binary equals ``1001000 11010010``.
```bat
(1110000)=(1001000 11010010)
```
* As a result -> ``Hi``