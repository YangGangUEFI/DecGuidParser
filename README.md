# DecGuidParser

```
py -3 .\DecGuidParser.py -h
usage: DecGuidParser.py [-h] [--depth DEPTH] [--output OUTPUT] directory

提取.dec文件中的GUID信息

positional arguments:
  directory             要扫描的目录路径

options:
  -h, --help            show this help message and exit
  --depth DEPTH, -d DEPTH
                        递归扫描的最大子目录深度，默认为1（只扫描直接子目录）
  --output OUTPUT, -o OUTPUT
                        输出JSON文件的路径
```
