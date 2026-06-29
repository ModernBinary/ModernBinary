<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Defining functions</h1>
</div>
<div align="center">
</div><br>

To define a simple function in modern binary, just put the name and codes of the function in func-base. To define a new function, the command must be written as ``*name*{ codes }``
### Example :
* Phrase `func` in modern binary: `1100110 11101010 101001010 110001100`
* Phrase `hello` in modern binary : `1101000 11001010 101000100 110110000 1000101011`
```bat
*1100110 11101010 101001010 110001100*{
    (1110000)=(1101000 11001010 101000100 110110000 1000101011)
}
```
* As a result -> hello

## Calling function
To call a variable, just type the name of the function as ``[*function_name*]``.
### Example :
* Phrase `func` in modern binary: `1100110 11101010 101001010 110001100`
* Phrase `hello` in modern binary : `1101000 11001010 101000100 110110000 1000101011`
```bat
* 1100110 11101010 101001010 110001100 *{
    (1110000)=( 1101000 11001010 101000100 110110000 1000101011 )
}

[* 1100110 11101010 101001010 110001100 *]
```
* As a result -> ``hello``