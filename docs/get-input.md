<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Getting Input</h1>
</div>
<div align="center">
</div><br>

To receive input from the user, you can use 105 ``action_code``. This action code means the character ``i`` (the first character of the input phrase). In the input arguments to this command, you can enter input text.
#### Example :
For example, enter the phrase ``"What's your name?"`` into arguments.
```bat
(105)=( 87 208 291 464 195 690 224 968 999 1170 1254 384 1430 1358 1635 1616 1071 )
```
* As a result -> ``What's your name?`` ... (Waiting for user input)

## Save input to a variable
To save the input and output of commands in a variable, just put the command in the Arguments section of the new variable, but the argument and the input command need minor changes.
To enter the input command in the variable arguments section, we must write the input format as ``[105:input_text]``.
### Example :
* Phrase `var` in modern binary: `118 194 342`
* Phrase `Enter your name:` in modern binary : `69 220 348 404 570 192 847 888 1053 1140 352 1392 1313 1680 1740 928`
```bat
(118:( 118 194 342 ))=( [ 105 : 69 220 348 404 570 192 847 888 1053 1140 352 1392 1313 1680 1740 928 ] )
(112)=( [[ 118 194 342 ]] )
```
* As a result -> ``Enter your name:``
* User input -> ``Hello, World!``
* As a result -> ``Hello, World!``