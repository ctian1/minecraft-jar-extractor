# minecraft-jar-extractor
python tools for extracting data from minecraft .jars

## Usage
### protocol_extractor.py

```bash
 $ python protocol_extractor.py decompiled_files_dir/
```

`decompiled_files_dir` should contain the decompiled source of a minecraft.jar. During testing, I used fernflower from https://the.bytecode.club/showthread.php?tid=5 with:

```bash
 $ java -jar fernflower.jar minecraft.jar decompiled_files_dir
```

after that, extract decompiled_files_dir/minecraft.jar into decompiled_files_dir.

## Comparison to [PrismarineJS's NodeJS protocol_extractor.js](https://github.com/PrismarineJS/minecraft-jar-extractor/blob/master/protocol_extractor.js)
* [sample output](http://www.diff.so/a/35tm2yR5Li) (left side is js, right is this repo)
* this extractor is a python 3.4 port of that, with tiny changes
* that extractor was made with a different version of fernflower possibly
