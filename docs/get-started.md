<div align="center">
<p>
    <img width="128" src="https://github.com/ThisIsMatin/ModernBinary/blob/main/dist/docs-logo.png?raw=true">
</p>
<h1>Getting Started With ModernBinary</h1>
</div>
<div align="center">
</div><br>

First you need to download the executable version of ModernBinary. The official release or compiler of the ModernBinary programming language is not currently officially available, and this language is under development. You can now use the [online version of ModernBinary code executable (Code playground)](https://modernbinary.github.io/ModernBinary/playground) and execute the code online.

Now you need to know how characters are translated and convert in modern binary. The modern binary code playground has the ability to convert text to binary modern, but to know how to do this, you can read [how to convert characters](https://modernbinary.github.io/ModernBinary/translate).

## Let's print Hello, World!
Calling and executing commands in modern binary is in the form ```(action_number)=(argv)```.
Each command has a ``action_number`` for calling and then we enter arguments in ``argv`` if needed.
Let's start with the simplest command, print!
The ``action_number`` of the print command is 112. This number according to the algorithm for calculating characters in modern binary, means the ``p`` (the first character of the phrase print.
Then in argv we can translate our text into modern binary format and then put it in it.
### Example :
Let's print the phrase ``Hi``, which in modern binary equals ``72 210``.
```bat
(112)=(72 210)
```
* As a result -> ``Hi``