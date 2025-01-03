# Example Package

安装：
```shell
pip install py_diff_pdf2
```

使用：

```python
from py_diff_pdf2 import compare_pdfs

result = compare_pdfs("file1.pdf","file2.pdf", output_path="diff.pdf")

 # result = {
 #        "success": success,
 #        "message": '',
 #        "output_path": output_path
 # }
```