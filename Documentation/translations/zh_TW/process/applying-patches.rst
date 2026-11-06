.. SPDX-License-Identifier: GPL-2.0

.. include:: ../disclaimer-zh_TW.rst

:Original: Documentation/process/applying-patches.rst

.. _tw_applying_patches:

將修補程式套用到 Linux 核心
+++++++++++++++++++++++++++

原作者：
    Jesper Juhl，2005 年 8 月

.. note::

   本文件已經過時。在大多數情況下，你幾乎一定會想改用 Git，而不是手動
   執行 ``patch``。

Linux 核心郵件列表上經常有人問：要如何把修補程式套用到核心？更具體地
說，針對眾多樹或分支之一所製作的修補程式，應該套用到哪個基礎核心上？
希望本文件能為你解答這些問題。

除了說明如何套用與撤銷修補程式，本文件也會簡要介紹不同的核心樹（並舉例
說明如何套用各個核心樹特有的修補程式）。


什麼是修補程式？
================

修補程式是一份小型文字文件，記錄原始碼樹兩個不同版本之間的差異。修補
程式由 ``diff`` 程式產生。

要正確套用修補程式，你需要知道它是以哪個版本為基礎產生的，以及它會把
原始碼樹變成哪個新版本。這兩項資訊應該都記錄在修補程式檔案的中繼資料
中，或者可以從檔名推斷出來。


如何套用或撤銷修補程式？
========================

使用 ``patch`` 程式套用修補程式。patch 程式會讀取 diff 檔（或修補程式
檔），並依照其中的描述修改原始碼樹。

Linux 核心的修補程式是以存放核心原始碼目錄的上層目錄為基準產生的。

這表示修補程式檔案中的檔案路徑，會包含產生修補程式時所用的核心原始碼
目錄名稱（或「a/」與「b/」之類的其他目錄名稱）。

這個名稱不太可能與你本機上的核心原始碼目錄名稱相同（不過，對於沒有標示
版本的修補程式，它常常是判斷其基礎版本的有用資訊），所以你應該先切換到
核心原始碼目錄，套用修補程式時再去掉修補程式檔案中檔名路徑的第一個部分
（``patch`` 的 ``-p1`` 參數就是做這件事）。

要撤銷先前套用的修補程式，請對 patch 使用 -R 參數。所以，如果你是這樣
套用修補程式的::

	patch -p1 < ../patch-x.y.z

就可以這樣撤銷（復原）它::

	patch -R -p1 < ../patch-x.y.z


如何把修補程式檔或 diff 檔交給 ``patch``？
==========================================

這件事（就像在 Linux 和其他類 UNIX 作業系統上常見的那樣）有好幾種不同
的做法。

在下面所有的範例中，我都用以下語法，透過標準輸入（stdin）把（未壓縮的）
檔案交給 patch::

	patch -p1 < path/to/patch-x.y.z

如果你只是想照著下面的範例操作，不想知道 patch 的其他用法，那麼本節讀到
這裡就可以了。

patch 也可以透過 -i 參數取得要使用的檔案名稱，像這樣::

	patch -p1 -i path/to/patch-x.y.z

如果你的修補程式檔案是用 gzip 或 xz 壓縮的，而你不想在套用前先解壓縮，
可以改用這種方式把它交給 patch::

	xzcat path/to/patch-x.y.z.xz | patch -p1
	bzcat path/to/patch-x.y.z.gz | patch -p1

如果你想在套用前先手動解壓縮修補程式檔案（下面的範例都假設你已經這樣
做了），只要對檔案執行 gunzip 或 xz 即可，像這樣::

	gunzip patch-x.y.z.gz
	xz -d patch-x.y.z.xz

這樣會留下一個純文字的 patch-x.y.z 檔案，你可以依自己的喜好，透過標準
輸入或 ``-i`` 參數把它交給 patch。

patch 還有幾個好用的參數：``-s`` 讓 patch 除了錯誤以外不輸出任何訊息，
可以避免錯誤訊息太快捲出螢幕；``--dry-run`` 讓 patch 只列出將會發生的
事情，而不實際做任何修改。最後，``--verbose`` 讓 patch 輸出更多關於
處理過程的資訊。


套用修補程式時的常見錯誤
========================

patch 套用修補程式檔案時，會用各種方式檢查檔案是否合理。

檢查檔案看起來是否像有效的修補程式檔案，以及檢查要修改的部分周圍的程式碼
是否與修補程式提供的上下文相符，只是 patch 所做的兩項基本檢查。

如果 patch 遇到看起來不太對的地方，它有兩種選擇：拒絕套用變更並中止，
或者設法稍作調整，讓修補程式能夠套用。

patch 會嘗試修正的「不太對」的情況之一，是上下文全部相符、要修改的行也
相符，但行號不同。舉例來說，如果修補程式修改的是檔案中間的內容，而檔案
開頭附近因為某些原因增加或刪除了幾行，就會發生這種情況。此時一切看起來
都沒問題，只是位置上下移動了一些，patch 通常會調整行號並套用修補程式。

每當 patch 必須稍微修改修補程式才能套用時，它會告訴你修補程式是經過
**fuzz** （模糊比對）才套用的。你應該對這類變更保持警覺，因為雖然 patch
很可能處理正確，但它並不/總是/正確，結果有時會是錯的。

當 patch 遇到無法用 fuzz 修正的變更時，會直接拒絕它，並留下一個副檔名為
``.rej`` 的檔案（拒絕檔）。你可以閱讀這個檔案，確切了解哪項變更無法套用，
以便視需要手動修正。

如果你的核心原始碼沒有套用任何第三方修補程式，只套用了來自 kernel.org
的修補程式，而且套用順序正確，也沒有自行修改過原始碼檔案，那麼你應該
永遠不會看到 patch 輸出 fuzz 或拒絕的訊息。如果你還是看到了這類訊息，
那麼你的本機原始碼樹或修補程式檔案很有可能已經以某種方式損毀。此時你
大概應該試著重新下載修補程式；如果問題依舊，建議你從 kernel.org 重新
完整下載一份全新的原始碼樹，從頭開始。

下面進一步看看 patch 可能輸出的幾種訊息。

如果 patch 停下來並顯示 ``File to patch:`` 提示，表示 patch 找不到要修改
的檔案。最可能的原因是你忘了指定 -p1，或者你所在的目錄不對。比較少見的
情況是，你會遇到需要用 ``-p0`` 而不是 ``-p1`` 套用的修補程式（閱讀修補
程式檔案應該就能看出是否如此；如果是，這是製作修補程式的人的錯誤，但並
不致命）。

如果你看到 ``Hunk #2 succeeded at 1887 with fuzz 2 (offset 7 lines).``
或類似的訊息，表示 patch 必須調整變更的位置（在這個例子中，它必須把變更
從預期的位置移動 7 行才能套用）。

產生的檔案不一定正確，要看檔案與預期不同的原因而定。

當你嘗試套用一個以不同核心版本產生的修補程式，而不是以你要修改的版本
產生的修補程式時，經常會發生這種情況。

如果你看到像 ``Hunk #3 FAILED at 2387.`` 這樣的訊息，表示修補程式無法
正確套用，patch 程式也無法透過 fuzz 完成套用。這會產生一個 ``.rej`` 檔，
其中包含導致修補程式失敗的變更，還會產生一個 ``.orig`` 檔，顯示無法修改
的原始內容。

如果你看到
``Reversed (or previously applied) patch detected!  Assume -R? [n]``
，表示 patch 偵測到修補程式中的變更似乎已經存在。

如果你確實之前已經套用過這個修補程式，只是不小心又套用了一次，那就回答
[n]o 並中止這個修補程式。如果你之前套用過這個修補程式，本來就打算撤銷
它，只是忘了指定 -R，那麼可以在這裡回答 [**y**]es，讓 patch 替你撤銷。

如果修補程式的製作者在製作時把來源目錄與目的目錄弄反了，也會發生這種
情況；此時撤銷修補程式實際上就是套用它。

類似 ``patch: **** unexpected end of file in patch`` 或
``patch unexpectedly ends in middle of line`` 的訊息，表示 patch 完全
無法理解你交給它的檔案。可能是你下載的檔案已損壞、你沒有先解壓縮就把
壓縮過的修補程式檔案交給 patch，或者你使用的修補程式檔案在傳遞途中被
某個郵件用戶端或郵件傳輸代理弄亂了，例如把一行過長的內容拆成兩行。通常
只要把被拆開的兩行重新接（串接）起來，就能輕鬆解決這類警告。

如前所述，如果你把 kernel.org 的修補程式套用到版本正確、未經修改的原始碼
樹上，這些錯誤應該永遠不會發生。所以，如果你在套用 kernel.org 的修補程式
時遇到這些錯誤，大概就該認定你的修補程式檔案或原始碼樹已經損壞；建議你
重新下載完整的核心樹和要套用的修補程式，從頭開始。


除了 ``patch`` 還有其他選擇嗎？
===============================


有的。

你可以使用 ``interdiff`` 程式 (http://cyberelk.net/tim/patchutils/)
產生一個代表兩個修補程式之間差異的修補程式，然後套用這個結果。

這樣就能一步從 5.7.2 之類的版本更新到 5.7.3。interdiff 的 -z 選項甚至
可以讓你直接傳入以 gzip 或 bzip2 壓縮的修補程式，不必使用 zcat 或 bzcat，
也不必手動解壓縮。

以下是一步從 5.7.2 更新到 5.7.3 的做法::

	interdiff -z ../patch-5.7.2.gz ../patch-5.7.3.gz | patch -p1

雖然 interdiff 可以幫你省下一兩個步驟，但一般仍建議你執行那些額外的步驟，
因為 interdiff 在某些情況下會出錯。

另一個選擇是 ``ketchup``，它是一個自動下載並套用修補程式的 Python 指令碼
(https://www.selenic.com/ketchup/)。

其他好用的工具還有：diffstat，顯示修補程式所做變更的摘要；lsdiff，簡短
列出修補程式檔案影響到的檔案，並可選擇一併顯示每段修補程式的起始行號；
以及 grepdiff，列出修補程式中內容符合指定正規表示式的部分所修改的檔案。


可以從哪裡下載修補程式？
========================

修補程式可以在 https://kernel.org/ 取得。
首頁有最新修補程式的連結，但它們也各自有固定的存放位置。

5.x.y（-stable）與 5.x 修補程式位於

    https://www.kernel.org/pub/linux/kernel/v5.x/

5.x.y 增量修補程式位於

    https://www.kernel.org/pub/linux/kernel/v5.x/incr/

-rc 修補程式不存放在網頁伺服器上，而是從 git 標籤按需產生，例如

    https://git.kernel.org/torvalds/p/v5.1-rc1/v5.0

穩定版的 -rc 修補程式位於

    https://www.kernel.org/pub/linux/kernel/v5.x/stable-review/


5.x 核心
========

這些是 Linus 發布的基礎穩定版本。版本號最大的就是最新的版本。

如果發現迴歸或其他嚴重缺陷，就會在這個基礎版本之上發布 -stable 修正
修補程式（見下文）。一旦新的 5.x 基礎核心發布，也會提供一個修補程式，
內容是前一個 5.x 核心與新核心之間的差異。

要套用從 5.6 更新到 5.7 的修補程式，請依照下列步驟操作（請注意，這類
修補程式 **不能** 套用在 5.x.y 核心之上，而是套用在基礎 5.x 核心之上；
如果你要從 5.x.y 更新到 5.x+1，必須先撤銷 5.x.y 修補程式）。

以下是一些範例::

	# moving from 5.6 to 5.7

	$ cd ~/linux-5.6		# change to kernel source dir
	$ patch -p1 < ../patch-5.7	# apply the 5.7 patch
	$ cd ..
	$ mv linux-5.6 linux-5.7	# rename source dir

	# moving from 5.6.1 to 5.7

	$ cd ~/linux-5.6.1		# change to kernel source dir
	$ patch -p1 -R < ../patch-5.6.1	# revert the 5.6.1 patch
					# source dir is now 5.6
	$ patch -p1 < ../patch-5.7	# apply new 5.7 patch
	$ cd ..
	$ mv linux-5.6.1 linux-5.7	# rename source dir


5.x.y 核心
==========

版本號有三段數字的核心是 -stable 核心。它們包含針對某個 5.x 核心中發現
的安全問題或重大迴歸所做的（較）小型關鍵修正。

對於想要最新穩定核心、又無意幫忙測試開發版或實驗版的使用者，建議使用
這個分支。

如果沒有可用的 5.x.y 核心，那麼版本號最大的 5.x 核心就是目前的穩定核心。

-stable 團隊同時提供一般修補程式與增量修補程式。以下說明如何套用這些
修補程式。

一般修補程式
~~~~~~~~~~~~

這類修補程式不是增量的，也就是說，例如 5.7.3 修補程式並不是套用在
5.7.2 核心原始碼之上，而是套用在基礎 5.7 核心原始碼之上。

因此，要把 5.7.3 修補程式套用到你現有的 5.7.2 核心原始碼，必須先撤銷
5.7.2 修補程式（回到基礎 5.7 核心原始碼），再套用新的 5.7.3 修補程式。

以下是一個簡單的範例::

	$ cd ~/linux-5.7.2		# change to the kernel source dir
	$ patch -p1 -R < ../patch-5.7.2	# revert the 5.7.2 patch
	$ patch -p1 < ../patch-5.7.3	# apply the new 5.7.3 patch
	$ cd ..
	$ mv linux-5.7.2 linux-5.7.3	# rename the kernel source dir

增量修補程式
~~~~~~~~~~~~

增量修補程式則不同：它們不是套用在基礎 5.x 核心之上，而是套用在前一個
穩定版核心（5.x.y-1）之上。

以下是套用這類修補程式的範例::

	$ cd ~/linux-5.7.2		# change to the kernel source dir
	$ patch -p1 < ../patch-5.7.2-3	# apply the new 5.7.3 patch
	$ cd ..
	$ mv linux-5.7.2 linux-5.7.3	# rename the kernel source dir


-rc 核心
========

這些是候選發布版（release-candidate）核心。每當 Linus 認為目前的 git
（核心的原始碼管理工具）樹處於相當穩健、足以進行測試的狀態時，就會發布
這種開發版核心。

這些核心並不穩定，如果你打算執行它們，應該預期偶爾會出問題。不過，這是
幾個主要開發分支中最穩定的一個，也是最終會成為下一個穩定核心的分支，
所以讓越多人測試它越好。

如果你想幫忙測試開發版核心，但又不想執行真正實驗性的東西，這是個適合
執行的分支（想執行實驗性內容的人，請參閱下文關於 -next 與 -mm 核心的
章節）。

-rc 修補程式不是增量的，它們和上文介紹的 5.x.y 修補程式一樣，套用在
基礎 5.x 核心之上。-rcN 字尾前面的核心版本，表示這個 -rc 核心最終會
成為的核心版本。

所以，5.8-rc5 表示這是 5.8 核心的第五個候選發布版，這個修補程式應該
套用在 5.7 核心原始碼之上。

以下是三個套用這類修補程式的範例::

	# first an example of moving from 5.7 to 5.8-rc3

	$ cd ~/linux-5.7			# change to the 5.7 source dir
	$ patch -p1 < ../patch-5.8-rc3		# apply the 5.8-rc3 patch
	$ cd ..
	$ mv linux-5.7 linux-5.8-rc3		# rename the source dir

	# now let's move from 5.8-rc3 to 5.8-rc5

	$ cd ~/linux-5.8-rc3			# change to the 5.8-rc3 dir
	$ patch -p1 -R < ../patch-5.8-rc3	# revert the 5.8-rc3 patch
	$ patch -p1 < ../patch-5.8-rc5		# apply the new 5.8-rc5 patch
	$ cd ..
	$ mv linux-5.8-rc3 linux-5.8-rc5	# rename the source dir

	# finally let's try and move from 5.7.3 to 5.8-rc5

	$ cd ~/linux-5.7.3			# change to the kernel source dir
	$ patch -p1 -R < ../patch-5.7.3		# revert the 5.7.3 patch
	$ patch -p1 < ../patch-5.8-rc5		# apply new 5.8-rc5 patch
	$ cd ..
	$ mv linux-5.7.3 linux-5.8-rc5		# rename the kernel source dir


-mm 修補程式與 linux-next 樹
============================

-mm 修補程式是 Andrew Morton 發布的實驗性修補程式。

過去 -mm 樹也用來測試子系統的修補程式，但這項功能現在改由
`linux-next` (https://www.kernel.org/doc/man-pages/linux-next.html)
樹負責。子系統維護者會先把他們的修補程式推送到 linux-next，並在合併視窗
期間直接發送給 Linus。

-mm 修補程式可以說是新功能和其他未經子系統樹合併的實驗性修補程式的試驗場。
這類修補程式在 -mm 中經過一段時間證明其價值後，Andrew 就會把它推送給
Linus，以納入主線。

linux-next 樹每天更新，並包含 -mm 修補程式。兩者都持續變動，包含許多
實驗性功能、大量不適合進入主線的除錯修補程式等，是本文件所介紹的各分支
中最具實驗性的。

這些修補程式不適合用在需要保持穩定的系統上，執行它們的風險也比其他任何
分支都高（請確保你有最新的備份——這適用於任何實驗性核心，對 -mm 修補
程式或使用 linux-next 樹的核心更是如此）。

我們非常感謝大家測試 -mm 修補程式與 linux-next，因為它們存在的意義，
就是在變更合併進更穩定的 Linus 主線樹之前，找出迴歸、當機、資料損毀
缺陷、建置失敗（以及其他一般的缺陷）。

不過，-mm 與 linux-next 的測試者應該要知道，這些樹出問題的頻率比其他
任何樹都高。


各種核心樹的說明到此結束。希望你現在已經清楚如何套用各種修補程式，並能
幫忙測試核心。

感謝 Randy Dunlap、Rolf Eike Beer、Linus Torvalds、Bodo Eggert、
Johannes Stezenbach、Grant Coady、Pavel Machek，以及其他可能被我遺漏
的人，感謝他們對本文件的審閱與貢獻。
