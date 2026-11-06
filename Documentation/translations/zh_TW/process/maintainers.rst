.. SPDX-License-Identifier: GPL-2.0

.. include:: ../disclaimer-zh_TW.rst

:Original: Documentation/process/maintainers.rst

.. _tw_maintainers:

維護者列表
==========

.. note:: 英文原文使用特殊的 ``maintainers-include`` 指令，把核心原始碼樹
          頂層的 ``MAINTAINERS`` 檔案整份嵌入文件中。本譯文只翻譯該檔案開頭
          說明各欄位的部分；實際的維護者名單請參閱英文原文
          :ref:`Documentation/process/maintainers.rst <maintainers>`，
          或直接查看 ``MAINTAINERS`` 檔案。

各節條目說明與建議順序
----------------------

``M:``
  修補程式的收件人（*Mail*）：``FullName <address@domain>``

``R:``
  指定的審閱者（*Reviewer*）：``FullName <address@domain>``

  發送修補程式時應副本（CC）給這些審閱者。

``L:``
  與此領域相關的郵件列表（*Mailing list*）

``S:``
  狀態（*Status*），為下列其中之一：

  Supported
    有人實際受僱照顧這部分。

  Maintained
    有人實際在照顧它。

  Odd Fixes
    有維護者，但他們沒有時間做太多事，只會偶爾加入一些修補程式。
    見下文。

  Orphan
    目前沒有維護者［不過也許你在撰寫新程式碼的同時，可以接下這個角色］。

  Obsolete
    舊程式碼。標記為 obsolete 的東西通常表示它已經被更好的系統取代，
    你應該改用那個系統。

``W:``
  提供狀態與資訊的網頁（*Web-page*）

``Q:``
  *Patchwork* 網頁式修補程式追蹤系統的網站

``B:``
  回報缺陷（*bugs*）的 URI。可以是含有詳細回報說明的網頁、缺陷追蹤系統的
  直接連結，或 mailto: URI。

``C:``
  聊天（*chat*）的 URI，包含開發者通常聚集的協定、伺服器與頻道，例如
  ``irc://server/channel``。

``P:``
  子系統概要（*Subsystem Profile*）文件，說明向該子系統提交修補程式的
  更多細節。可以是核心原始碼樹中 Documentation/ 底下的 .rst 檔案，或是
  一個 URI。詳見 Documentation/maintainer/maintainer-entry-profile.rst。

``T:``
  原始碼管理（*SCM*）樹的類型與位置。

  類型為下列其中之一：git、hg、quilt、stgit、topgit

``F:``
  檔案（*Files*）與目錄的萬用字元模式。

  結尾的斜線表示包含該目錄下的所有檔案，以及其子目錄中的檔案。

  - ``F: drivers/net/``：drivers/net 中及其下各層的所有檔案
  - ``F: drivers/net/*``：drivers/net 中的所有檔案，但不含其下各層
  - ``F: */net/*``：「任何頂層目錄」/net 中的所有檔案
  - ``F: fs/**/*foo*.c``：fs 任何子目錄中所有符合 ``*foo*.c`` 的檔案

  每行一個模式，可以有多行 F:。

``X:``
  排除（*Excluded*）不由此條目維護的檔案與目錄，規則與 F: 相同。排除規則
  會先於檔案比對進行檢查。可用來排除特定子目錄，例如：

  - ``F: net/``
  - ``X: net/ipv6/``

  會比對 net/ 中及其下各層的所有檔案，但排除 net/ipv6/。

``N:``
  檔案與目錄的正規表示式（*Regex*）模式。

  - ``N: [^a-z]tegra``：路徑中含有 tegra 的所有檔案（不包括像 integrator
    這樣的檔案）

  每行一個模式，可以有多行 N:。

  scripts/get_maintainer.pl 對於符合 F: 模式的檔案與符合 N: 模式的檔案，
  處理方式不同。預設情況下，比對到 F: 模式時，get_maintainer 不會查看
  git log 歷史；比對到 N: 模式時，則會利用 git log 歷史，一併通知在 git
  提交中留有簽名的人。

``K:``
  在修補程式或檔案中比對的內容正規表示式（*Content regex*，perl 擴充語法）。
  例如：

  - ``K: of_get_profile``：比對含有「of_get_profile」的修補程式或檔案
  - ``K: \b(printk|pr_(info|err))\b``：比對含有 printk、pr_info 或 pr_err
    其中一個或多個字詞的修補程式或檔案

  每行一個正規表示式模式，可以有多行 K:。

維護者名單
----------

.. note:: 閱讀此名單時，請先尋找最精確的領域。新增條目時，請保持條目依
          字母順序排列。

完整的維護者名單（依子系統排列的表格）請參閱英文原文
:ref:`Documentation/process/maintainers.rst <maintainers_table>`。
