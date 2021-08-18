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
: condition {
    ...
}
```

## Condition Operators

| Operator | Description
| ------ | ------ |
| **``==``** | If the values are equal to each other is executed.
| **``!=``** | If the values are not equal to each other is executed.
| **``<``** | If the value is smaller than the next value.
| **``<=``** | If a value is less than or equal to the next value.
| **``>``** | If a value is larger than the next value.
| **``>=``** | If a value is greater than or equal to the next value.

One of the modern binary rules right now is that you can not place multiple conditions on one condition. This rule is due to being a fun and resembling a binary.
### Example :
* Let's create two variables `X` and `Y` with common `text` values and put them equal in the condition. If this condition is met, the phrase `True` will be printed.
```shell
[120]=( 116 202 360 464 )

[121]=( 116 202 360 464 )

: [120] == [121] {

    (112)=( 84 228 351 404 )

}
```
* As a result -> ``True``