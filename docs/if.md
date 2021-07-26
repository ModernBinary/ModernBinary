<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>IF / Condition</h1>
</div>
<div align="center">
</div><br>

To write a if / condition in modern binary, need to write a special form to write condition.
### Example : 
```
(105 204:( condition )){
    ...
}
```

## Condition Operators

| Operator | Description
| ------ | ------ |
| **``==``** | If the values are equal to each other is executed.
| **``!=``** | If the values are not equal to each other is executed.

One of the modern binary rules for better readability is to use variables in conditions and it's not possible to write expressions directly in conditions.
### Example :
* Let's create two variables `X` and `Y` with common `text` values and put them equal in the condition. If this condition is met, the phrase `True` will be printed.
```bat
(118:(120))=( 116 202 360 464 )

(118:(121))=( 116 202 360 464 )

(105 204:( [[120]] == [[121]] )){

    (112)=( 84 228 351 404 )

}
```
* As a result -> ``True``