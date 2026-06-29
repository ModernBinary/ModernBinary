<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>For Loop</h1>
</div>
<div align="center">
</div><br>

To repeat a block of code a fixed number of times, use `~N~` where `N` is a **binary integer** representing the count.

### Syntax:
```
~N~{
    ...
}
```

`N` is a plain binary number (not encoded text). For example, `101` is 5 in binary, so the block runs 5 times.

### Binary count reference:

| Decimal | Binary |
| ------- | ------ |
| 1 | `1` |
| 2 | `10` |
| 3 | `11` |
| 5 | `101` |
| 10 | `1010` |
| 100 | `1100100` |

### Example:
* `101` in binary = 5 in decimal
* Phrase `Hello` in modern binary: `1001000 11001010 101000100 110110000 1000101011`

```shell
~101~{
    (1110000)=(1001000 11001010 101000100 110110000 1000101011)
}
```
* As a result -> `HelloHelloHelloHelloHello` (printed 5 times)
