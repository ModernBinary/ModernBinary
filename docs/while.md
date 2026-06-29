<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>While Loop</h1>
</div>
<div align="center">
</div><br>

To write a while loop in modern binary, use `::` (double colon) followed by a condition and a code block. The loop runs as long as the condition is true.

### Syntax:
```
:: condition {
    ...
}
```

The condition uses the same operators and syntax as [IF](https://modernbinary.github.io/ModernBinary/if).

## Condition Operators

| Operator | Description |
| ------ | ------ |
| **`==`** | Loop while values are equal. |
| **`!=`** | Loop while values are not equal. |
| **`<`** | Loop while left value is smaller. |
| **`<=`** | Loop while left value is less than or equal. |
| **`>`** | Loop while left value is larger. |
| **`>=`** | Loop while left value is greater than or equal. |

### Example:
* Variable name `1` in modern binary: `110001`
* Value `1` encoded: `110001`
* Value `0` encoded: `110000`
* Phrase `Hello` in modern binary: `1001000 11001010 101000100 110110000 1000101011`

```shell
[110001]=[110001]

:: [110001] == 110001 {
    (1110000)=(1001000 11001010 101000100 110110000 1000101011)
    [110001]=[110000]
}
```
* As a result -> `Hello`

The loop runs once: on the second check the variable `1` now holds `0`, which is not equal to `1`, so the loop exits.
