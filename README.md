<p align="center">
  <img src="public/img/samplelogo.png" width = 30%/>
</p>
<h1 align="center">Cocoon Lexical Analyzer</h1>

`A Python-based programming language designed for young learners.`

## How to use

There are two ways on how to use the lexical analyzer:

1. By running the [GUI](/gui.py)

2. By running the [shell](/shell.py) in your command line, passing two options which is `-c` or `-f`.
        
## Shell Parameters

All parameters are case-insensitive. Only one option can be used at a time.

## -cli | -c

The `-cli` | `-c` is passed to use the cli version of the lexical analyzer.

Example: ```python shell.py -c```

## -file  | -f

The `-file` or `-f` is followed by the file name of the existing KKUN file as it's second passed argument. The file must have an extension of .kkun in order for it to be recognized

Example: ```python shell.py -f <filename>```