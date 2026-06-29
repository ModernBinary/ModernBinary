<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Calculate and convert characters in modern binary</h1>
</div>
<div align="center">
</div><br>

Modern binary language has relatively easy and difficult calculations. The characters are originally English characters, but must be written as numbers when executed.

### How to translate characters into binary modern?
First need to convert the character numbers to ``ASCII`` format, respectively. ``(Numbers [1-9] start at 49 in ASCII, and English letters [a-z] start at 97 ASCII)``
#### Example :
`hello` Letters in ASCII format :
```bat
h ==> 104
e ==> 101
l ==> 108
l ==> 108
o ==> 111
```
* As a result -> ``1101000 1100101 1101100 1101100 1101111``

Then we have to multiply each number by the index number of that number. ``(Note: Indexes start at 1, because if they start at 0, the first number is 0)``

#### Example :

```bat
1101000 * 1 = 1101000
1100101 * 10 = 11001010
1101100 * 11 = 101000100
1101100 * 100 = 110110000
1101111 * 101 = 1000101011
```
* As a result -> ``1101000 11001010 101000100 110110000 1000101011``

***You now have a phrase in modern binary language and can use it in your code!***
