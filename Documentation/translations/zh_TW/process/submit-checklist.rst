.. SPDX-License-Identifier: GPL-2.0

.. include:: ../disclaimer-zh_TW.rst

:Original: Documentation/process/submit-checklist.rst

.. _tw_submitchecklist:

================================
Linux 核心修補程式提交檢查清單
================================

以下是開發者若希望自己提交的核心修補程式能更快被接受，應該做到的一些基本
事項。

這些事項是在
:ref:`Documentation/translations/zh_TW/process/submitting-patches.rst
<tw_submittingpatches>`
及其他關於提交 Linux 核心修補程式的文件所提供的內容之外，還要額外做到的。

審查你的程式碼
==============

1) 如果你使用了某項功能，就 #include 定義／宣告該功能的檔案。不要依賴其他
   標頭檔幫你引入你所用到的標頭檔。

2) 依照
   :ref:`Documentation/translations/zh_TW/process/coding-style.rst
   <tw_codingstyle>`
   所述，檢查你的修補程式是否符合一般的程式碼風格。

3) 所有記憶體屏障（例如 ``barrier()``、``rmb()``、``wmb()``）都需要在原始碼
   中加上註解，說明它們所做事情的邏輯及原因。

審查 Kconfig 變更
=================

1) 任何新增或修改的 ``CONFIG`` 選項都不應弄亂設定選單，且預設應為關閉，
   除非符合 ``Documentation/kbuild/kconfig-language.rst`` 中
   Menu attributes: default value 一節所記載的例外條件。

2) 所有新的 ``Kconfig`` 選項都有說明文字。

3) 已針對相關的 ``Kconfig`` 組合仔細審查過。這一點很難單靠測試做對，
   在這裡多動腦是值得的。

提供文件
========

1) 加入 :ref:`kernel-doc <kernel_doc>` 來為全域核心 API 撰寫文件。
   （static 函式不需要，但寫了也可以。）

2) 所有新的 ``/proc`` 項目都在 ``Documentation/`` 下有文件記載。

3) 所有新的核心開機參數都記載於
   ``Documentation/admin-guide/kernel-parameters.rst``。

4) 所有新的模組參數都用 ``MODULE_PARM_DESC()`` 記載。

5) 所有新的使用者空間介面都記載於 ``Documentation/ABI/``。
   詳情請參閱 Documentation/admin-guide/abi.rst
   （或 ``Documentation/ABI/README``）。
   更改使用者空間介面的修補程式應該副本（CC）給
   linux-api@vger.kernel.org\ 。

6) 如果修補程式新增了任何 ioctl，也要更新
   ``Documentation/userspace-api/ioctl/ioctl-number.rst``。

使用工具檢查你的程式碼
======================

1) 提交前先用修補程式風格檢查器（``scripts/checkpatch.pl``）檢查有無輕微的
   違規。對於修補程式中仍留下的每一項違規，你都應該能說明理由。

2) 用 sparse 檢查時乾淨無誤。

3) 使用 ``make checkstack`` 並修正它找到的任何問題。
   請注意 ``checkstack`` 不會明確指出問題，但任何在堆疊上使用超過 512 位元組
   的函式，都是應該修改的候選對象。

建置你的程式碼
==============

1) 乾淨地建置：

  a) 使用適用或修改過的 ``CONFIG`` 選項 ``=y``、``=m`` 與 ``=n``。
     沒有 ``gcc`` 警告／錯誤，也沒有連結器警告／錯誤。

  b) 通過 ``allnoconfig``、``allmodconfig``

  c) 使用 ``O=builddir`` 時可以成功建置

  d) Documentation/ 下的任何變更都能成功建置，且不產生新的警告／錯誤。
     使用 ``make htmldocs`` 或 ``make pdfdocs`` 檢查建置結果，並修正任何
     問題。

2) 使用本機的交叉編譯工具或其他建置環境（build farm），在多種 CPU 架構上
   建置。
   請注意，針對不同字組大小（32 位元與 64 位元）及不同位元組順序（big-endian
   與 little-endian）的架構進行測試，能有效找出各種可攜性問題；這些問題源自
   對可表示的數值範圍、資料對齊或位元組順序等的錯誤假設。

3) 新加入的程式碼已用 ``gcc -W`` 編譯過（使用 ``make KCFLAGS=-W``）。這會
   產生大量雜訊，但很適合用來找出像「warning: comparison between signed and
   unsigned」這類的錯誤。

4) 如果你修改的原始碼依賴或使用了與下列 ``Kconfig`` 符號相關的任何核心 API
   或功能，就要在停用相關 ``Kconfig`` 符號及／或設為 ``=m`` （如果有此選項）
   的情況下，測試多種建置組合〔不必同時全部停用，只要各種／隨機的組合即可〕：

   ``CONFIG_SMP``, ``CONFIG_SYSFS``, ``CONFIG_PROC_FS``, ``CONFIG_INPUT``,
   ``CONFIG_PCI``, ``CONFIG_BLOCK``, ``CONFIG_PM``, ``CONFIG_MAGIC_SYSRQ``,
   ``CONFIG_NET``, ``CONFIG_INET=n`` （但後者需搭配 ``CONFIG_NET=y``）。

測試你的程式碼
==============

1) 已在同時啟用 ``CONFIG_PREEMPT``、``CONFIG_DEBUG_PREEMPT``、
   ``CONFIG_SLUB_DEBUG``、``CONFIG_DEBUG_PAGEALLOC``、``CONFIG_DEBUG_MUTEXES``、
   ``CONFIG_DEBUG_SPINLOCK``、``CONFIG_DEBUG_ATOMIC_SLEEP``、
   ``CONFIG_PROVE_RCU`` 與 ``CONFIG_DEBUG_OBJECTS_RCU_HEAD`` 的情況下測試過。

2) 已在啟用與不啟用 ``CONFIG_SMP`` 及 ``CONFIG_PREEMPT.`` 的情況下，進行過
   建置與執行期測試。

3) 所有程式碼路徑都已在啟用所有 lockdep 功能的情況下執行過。

4) 已至少透過注入 slab 與分頁配置失敗進行過檢查。請參閱
   ``Documentation/fault-injection/``。
   如果新程式碼的份量很大，加入子系統專屬的故障注入可能也是適當的。

5) 已用 linux-next 最新的標籤測試過，確保它仍能與所有其他排隊中的修補程式，
   以及 VM、VFS 和其他子系統的各種變更一起正常運作。
