.. SPDX-License-Identifier: GPL-2.0

.. include:: ../disclaimer-zh_CN.rst

:Original: Documentation/doc-guide/checktransupdate.rst

:译者: 慕冬亮 Dongliang Mu <dzm91@hust.edu.cn>

检查翻译更新

这个脚本帮助跟踪不同语言的文档翻译状态，即文档是否与对应的英文版本保持更新。

工作原理
------------

该脚本从新到旧搜索翻译文件的提交历史，查找提交信息中记录的英文版本基线。
脚本会根据对应的英文文件验证诸如 ``Update to commit HASH`` 这样的基线标记，
因此，之后仅修改错别字等翻译内容的提交不会让过期翻译看起来已是最新版本。
对于没有显式基线标记的旧翻译历史，脚本仍会按作者日期推断基线。

找到有效基线后，脚本会报告从该基线到 HEAD 之间修改过英文文件的非合并提交。
命令既接受翻译文件，也接受翻译目录；如果显式指定的路径不在
``Documentation/translations/<locale>/`` 下，脚本会报错。

实现的功能

- 检查特定语言中的所有文件
- 检查单个文件或一组文件
- 提供更改输出格式的选项
- 跟踪没有翻译过的文件的翻译状态

用法
-----

::

    tools/docs/checktransupdate.py --help

具体用法请参考参数解析器的输出

示例

-  ``tools/docs/checktransupdate.py -l zh_CN``
   这将打印 zh_CN 语言中需要更新的所有文件。
-  ``tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst``
   这将只打印指定文件的状态。
-  ``tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools``
   这将递归打印指定目录中翻译文件的状态。

然后输出类似如下的内容：

::

    Documentation/dev-tools/kfence.rst
    No translation in the locale of zh_CN

    Documentation/translations/zh_CN/dev-tools/testing-overview.rst
    commit 42fb9cfd5b18 ("Documentation: dev-tools: Add link to RV docs")
    1 commits needs resolving in total
