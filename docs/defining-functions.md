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
* Phrase `func` in modern binary: `102 234 330 396`
* Phrase `hello` in modern binary : `104 202 324 432 555`
```bat
*102 234 330 396*{
    (112)=(104 202 324 432 555)
}
```
* As a result -> hello

## Calling function
To call a variable, just type the name of the function as ``[*function_name*]``.
### Example :
* Phrase `func` in modern binary: `102 234 330 396`
* Phrase `hello` in modern binary : `104 202 324 432 555`
```bat
* 102 234 330 396 *{
    (112)=( 104 202 324 432 555 )
}

[* 102 234 330 396 *]
```
* As a result -> ``hello``