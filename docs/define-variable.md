<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Defining a variable</h1>
</div>
<div align="center">
</div><br>

To define a variable in modern binary, you must use 118 ``action_code``. In modern binary language, this number is equal to ``v`` (the first character of the expression variable).
**Note, however, that using this action code to create a new variable is different.** To create a new variable, the command must be written as ``(118:(name))=(value)``
### Example :
* Phrase `var` in modern binary: `118 194 342`
* Phrase `hello` in modern binary : `104 202 324 432 555`
```bat
(118:( 118 194 342 ))=( 104 202 324 432 555 )
```
* As a result -> The variable `var` was defined with `hello` value.

## Calling variable
To call a variable, just type the name of the variable as ``[[variable_name]]``.
### Example :
* Phrase `var` in modern binary: `118 194 342`
* Phrase `hello` in modern binary : `104 202 324 432 555`
```bat
(118:( 118 194 342 ))=( 104 202 324 432 555 )
(112)=( [[ 118 194 342 ]] )
```
* As a result -> ``hello``