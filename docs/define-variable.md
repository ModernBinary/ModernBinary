<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Defining a variable</h1>
</div>
<div align="center">
</div><br>

To define a variable in modern binary, just put the name and value of the variable in parentheses. To create a new variable, the command must be written as ``[name]=[value]``
### Example :
* Phrase `var` in modern binary: `1110110 11000010 101010110`
* Phrase `hello` in modern binary : `1101000 11001010 101000100 110110000 1000101011`
```bat
[1110110 11000010 101010110]=[1101000 11001010 101000100 110110000 1000101011]
```
* As a result -> The variable `var` was defined with `hello` value.

## Calling variable
To call a variable, just type the name of the variable as ``[variable_name]``.
### Example :
* Phrase `var` in modern binary: `1110110 11000010 101010110`
* Phrase `hello` in modern binary : `1101000 11001010 101000100 110110000 1000101011`
```bat
[ 1110110 11000010 101010110 ]=[ 1101000 11001010 101000100 110110000 1000101011 ]
( 1110000 )=( [ 1110110 11000010 101010110 ] )
```
* As a result -> ``hello``