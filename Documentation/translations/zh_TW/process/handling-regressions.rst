.. SPDX-License-Identifier: (GPL-2.0+ OR CC-BY-4.0)
.. 重新散布的相關資訊請見本文件結尾。

.. include:: ../disclaimer-zh_TW.rst

:Original: Documentation/process/handling-regressions.rst

處理迴歸問題
++++++++++++

*我們不製造迴歸* ——本文件說明這條「Linux 核心開發的首要規則」在實務上對
開發者的意義。本文件是 Documentation/admin-guide/reporting-regressions.rst
的補充，後者從使用者的角度說明這個主題；如果你從未讀過那份文件，請在繼續
閱讀本文之前，至少先大致瀏覽一遍。

重點摘要（亦即「TL;DR」）
=========================

#. 確保 `迴歸郵件列表 <https://lore.kernel.org/regressions/>`_
   （regressions@lists.linux.dev）的訂閱者能盡快得知任何新的迴歸報告：

    * 收到沒有抄送（CC）該列表的郵件報告時，立即至少發送一封簡短的
      「全部回覆」（Reply-all）並抄送該列表，讓列表參與其中。

    * 把提交到缺陷追蹤器的報告轉寄或退回（bounce）到該列表。

#. 讓 Linux 核心迴歸追蹤機器人「regzbot」追蹤這個問題（此步驟可選，但建議
   這麼做）：

    * 對於郵件報告，檢查報告者是否附上了類似 ``#regzbot
      introduced: v5.13..v5.14-rc1`` 的一行。如果沒有，請發送一封回覆（抄送
      迴歸列表），其中包含類似下面的段落，告訴 regzbot 問題從何時開始發生::

       #regzbot ^introduced: 1f2e3d4c5b6a

    * 把缺陷追蹤器中的報告轉寄到迴歸列表時（見上文），請附上類似下面的
      段落::

       #regzbot introduced: v5.13..v5.14-rc1
       #regzbot from: Some N. Ice Human <some.human@example.com>
       #regzbot monitor: http://some.bugtracker.example.com/ticket?id=123456789

#. 提交迴歸的修正時，依照 Documentation/process/submitting-patches.rst 與
   :ref:`Documentation/process/5.Posting.rst <tw_development_posting>` 的要求，
   在修補程式描述中加上「Closes:」標籤，指向所有回報該問題的地方。如果你
   只修正了造成迴歸之問題的一部分，可以改用「Link:」標籤。regzbot 目前
   不區分這兩者。

#. 一旦找出肇事提交（culprit），請盡快修復迴歸；大多數迴歸的修正應在兩週
   內合併，但有些需要在兩到三天內解決。


與開發者相關的 Linux 核心迴歸完整細節
=====================================


重要基本事項詳述
----------------


收到迴歸報告時該怎麼做
~~~~~~~~~~~~~~~~~~~~~~

確保 Linux 核心的迴歸追蹤者以及
`迴歸郵件列表 <https://lore.kernel.org/regressions/>`_
（regressions@lists.linux.dev）的其他訂閱者得知任何新回報的迴歸：

 * 如果你收到的郵件報告沒有抄送該列表，請立即至少發送一封簡短的「全部
   回覆」並抄送該列表，讓列表參與其中；如果你回覆的郵件漏掉了該列表，
   也請設法確保再次抄送它。

 * 如果提交到缺陷追蹤器的報告出現在你的收件匣中，請把它轉寄或退回到該
   列表。轉寄之前，不妨先查看列表的封存，確認報告者是否已經依照
   Documentation/admin-guide/reporting-issues.rst 的指示轉寄過該報告。

進行上述任一動作時，可以考慮讓 Linux 核心迴歸追蹤機器人「regzbot」立即
開始追蹤這個問題：

 * 對於郵件報告，檢查報告者是否附上了類似
   ``#regzbot introduced: 1f2e3d4c5b6a`` 的「regzbot 命令」。如果沒有，
   請發送一封回覆（抄送迴歸列表），其中包含類似下面的段落::

       #regzbot ^introduced: v5.13..v5.14-rc1

   這會告訴 regzbot 問題開始發生的版本範圍；你也可以用 commit ID 指定
   範圍，或在報告者已用二分法找出肇事提交時，只指定單一 commit ID。

   請注意「introduced」前面的插入符號（^）：它告訴 regzbot 把上層郵件
   （你所回覆的那封）當作你想追蹤之迴歸的初始報告；這一點很重要，因為
   regzbot 之後會尋找帶有「Closes:」標籤、指向 lore.kernel.org 封存中
   該報告的修補程式。

 * 轉寄回報到缺陷追蹤器的迴歸時，請附上包含下列 regzbot 命令的段落::

       #regzbot introduced: 1f2e3d4c5b6a
       #regzbot from: Some N. Ice Human <some.human@example.com>
       #regzbot monitor: http://some.bugtracker.example.com/ticket?id=123456789

   之後，regzbot 就會自動把帶有「Closes:」標籤、指向你的郵件或上述工單
   的修補程式與該報告關聯起來。

修復迴歸時的要點
~~~~~~~~~~~~~~~~

提交迴歸的修正時不需要做任何特別的事，只要記得照著
Documentation/process/submitting-patches.rst、
:ref:`Documentation/process/5.Posting.rst <tw_development_posting>` 與
Documentation/process/stable-kernel-rules.rst 中已更詳細說明的做法即可：

 * 使用「Closes:」標籤指向所有回報該問題的地方::

       Closes: https://lore.kernel.org/r/30th.anniversary.repost@klaava.Helsinki.FI/
       Closes: https://bugzilla.kernel.org/show_bug.cgi?id=1234567890

   如果你只修正了問題的一部分，可以依照上述第一份文件的說明改用「Link:」。
   regzbot 目前把兩者視為相同，並將所連結的報告視為已解決。

 * 加上「Fixes:」標籤，指出造成迴歸的提交。

 * 如果肇事提交是在較早的開發週期中合併的，請使用
   ``Cc: stable@vger.kernel.org`` 標籤，明確標記此修正需要向後移植。

以上這些都是對你的期望，且在處理迴歸時十分重要，因為這些標籤對每個可能在
數週、數月甚至數年後研究這個問題的人（包括你自己）都非常有價值。這些標籤
對其他核心開發者或 Linux 發行版所使用的工具和腳本也至關重要；regzbot 就是
其中之一，它高度依賴「Closes:」標籤，把迴歸報告與解決它們的變更關聯起來。

修復迴歸的期望與最佳實務
~~~~~~~~~~~~~~~~~~~~~~~~

身為 Linux 核心開發者，你應該盡最大努力，避免讓你最近的變更所造成的迴歸
使使用者只剩下以下選擇：

 * 執行一個帶有影響使用之迴歸的核心。

 * 改用較舊或較新的核心系列。

 * 在找出迴歸的肇事提交後，繼續執行過時、因而可能不安全的核心超過三週。
   理想情況下應少於兩週。而如果問題嚴重或影響許多使用者（無論是整體而言，
   還是在普遍的環境中），則應該只有短短幾天。

實務上如何做到這一點取決於各種因素。請以下列經驗法則作為指引。

一般而言：

 * 將迴歸的處理優先於所有其他 Linux 核心工作，除非後者涉及嚴重問題（例如
   緊急的安全漏洞、資料遺失、硬體變磚……）。

 * 加速修復最近進入正式主線、穩定版或長期支援版發布（無論是直接進入還是
   經由向後移植）的主線迴歸。

 * 不要把目前週期中的迴歸當作可以等到週期結束再處理的事情，因為這個問題
   可能讓使用者和 CI 系統現在或往後都不願或無法測試主線。

 * 以必要的謹慎進行工作，避免造成額外或更大的損害，即使這樣解決問題可能
   會比下文所述花費更長的時間。

找出迴歸的肇事提交之後，關於時程：

 * 如果問題嚴重或困擾許多使用者（無論是整體而言，還是在特定硬體環境、
   發行版或穩定版／長期支援版系列等普遍情況下），目標是在兩到三天內將修正
   合併進主線。

 * 如果肇事提交進入了最近的主線、穩定版或長期支援版發布（無論是直接進入
   還是經由向後移植），目標是在下下個星期日之前將修正合併進主線；如果
   肇事提交在一週的前段就已確認且容易解決，請盡量在同一週內將修正合併進
   主線。

 * 對於其他迴歸，目標是在接下來三週內的最後一個星期日之前將修正合併進
   主線。如果該迴歸是人們可以輕鬆忍受一段時間的問題（例如輕微的效能迴歸），
   延後一到兩個星期日也可以接受。

 * 強烈不建議把迴歸修正延到下一個合併視窗才合併進主線，除非該修正的風險
   極高，或肇事提交是在一年多以前合併進主線的。

關於流程：

 * 一定要考慮撤銷（revert）肇事提交，因為這通常是修復迴歸最快、危險最小
   的方式。不必擔心之後把修正過的版本合併進主線：這應該很直接，因為大部分
   程式碼都已經審查過一次。

 * 盡量在目前的開發週期結束前，解決過去十二個月內在主線中引入的任何迴歸：
   Linus 希望這類迴歸能像目前週期中的迴歸一樣處理，除非修復它們有不尋常
   的風險。

 * 如果迴歸看起來很棘手，可以考慮在討論或修補程式審查中抄送 Linus。在危急
   或緊急的情況下也這麼做，特別是子系統維護者可能無法聯繫時。當你知道這類
   迴歸已進入主線、穩定版或長期支援版發布時，也請抄送穩定版團隊。

 * 對於緊急的迴歸，可以考慮請 Linus 直接從郵件列表取用修正：對於沒有爭議
   的修正，他完全可以接受這種做法。不過理想情況下，這類請求應該與子系統
   維護者協調一致，或直接由他們提出。

 * 如果你不確定在新的主線版本發布前幾天套用某個修正是否值得冒險，請寄一封
   郵件給 Linus，並照常抄送相關列表與人員；在郵件中概述情況，同時請他考慮
   直接從列表取用該修正。之後他可以自己做出決定，必要時甚至可以延後發布。
   同樣地，這類請求理想上應該與子系統維護者協調一致，或直接由他們提出。

關於穩定版與長期支援版核心：

 * 如果迴歸從未在主線中出現過，或已經在主線中修復，你可以把它們留給穩定版
   團隊處理。

 * 如果某個迴歸在過去十二個月內進入了正式的主線發布，請務必在修正中加上
   「Cc: stable@vger.kernel.org」標籤，因為單靠「Fixes:」標籤並不能保證會
   被向後移植。如果你知道肇事提交已被向後移植到穩定版或長期支援版核心，
   也請加上同樣的標籤。

 * 收到最近的穩定版或長期支援版核心系列的迴歸報告時，請至少簡單評估一下
   該問題是否也可能發生在目前的主線中；如果看起來很可能，請接手處理該報告。
   如有疑問，請報告者在主線上檢查。

 * 每當你想迅速解決一個最近也進入了正式主線、穩定版或長期支援版發布的迴歸
   時，請在主線中盡快修復它；在適當的時候，請 Linus 協助加速處理這個修正
   （見上文）。這是因為穩定版團隊通常既不撤銷、也不修復在主線中造成相同
   問題的變更。

 * 對於緊急的迴歸修正，你可能會想在修正合併進主線後，給穩定版團隊留個訊息，
   以確保它盡快被向後移植；在合併視窗期間及其後不久特別建議這麼做，否則該
   修正可能會排在一個龐大的修補程式佇列的最後面。

關於修補程式的流程：

 * 開發者們，在設法達成上述時限時，請記得把修正接受測試、審查以及被 Linus
   合併所需的時間計算在內，理想情況下修正至少要在 linux-next 中待上一小段
   時間。因此，如果某個修正很緊急，請明確表示出來，確保其他人適當地處理它。

 * 審查者們，懇請你們及時審查迴歸修正，協助開發者達成上述時限。

 * 子系統維護者們，同樣也鼓勵你們加速處理迴歸修正。因此，請評估對於特定的
   修正是否可以跳過 linux-next。必要時也可以考慮比平常更頻繁地發送 git 拉取
   請求。並且盡量避免在週末把迴歸修正壓著不處理，特別是當該修正被標記為需要
   向後移植時。


開發者應該留意的其他迴歸相關面向
--------------------------------


如何處理已知有迴歸風險的變更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

評估迴歸風險有多大，例如在 Linux 發行版和 Git 託管平台（forge）中搜尋
程式碼。也可以考慮請可能受影響的其他開發者或專案評估、甚至測試所提議的
變更；如果出現問題，或許可以找到所有人都能接受的解決方案。

如果最後看來迴歸風險相對較小，就繼續進行這個變更，但要讓所有相關人員知道
這個風險。因此，請確保你的修補程式描述清楚說明這一點。變更合併後，請告知
Linux 核心的迴歸追蹤者和迴歸郵件列表這個風險，讓大家在有報告陸續出現時都
已注意到這個變更。視風險而定，你可能也會想請子系統維護者在他們的主線拉取
請求中提及這個問題。

關於迴歸還有什麼需要知道的？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

請參閱 Documentation/admin-guide/reporting-regressions.rst，其中涵蓋了許多
你可能想要了解的其他面向：

 * 「無迴歸」規則的目的

 * 哪些問題真正算是迴歸

 * 誰負責找出迴歸的根本原因

 * 如何處理棘手的情況，例如迴歸是由安全修正所造成，或修復某個迴歸可能造成
   另一個迴歸

遇到迴歸時可以向誰尋求建議
~~~~~~~~~~~~~~~~~~~~~~~~~~

寄一封郵件到迴歸郵件列表（regressions@lists.linux.dev），同時抄送 Linux
核心的迴歸追蹤者（regressions@leemhuis.info）；如果問題比較適合私下處理，
可以省略該列表。


關於迴歸追蹤與 regzbot 的更多資訊
---------------------------------


為什麼 Linux 核心有迴歸追蹤者？為什麼要使用 regzbot？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

像「無迴歸」這樣的規則需要有人確保它被遵守，否則就會因意外或刻意而遭到
破壞。歷史已經證明，這對 Linux 核心來說也是如此。因此 Thorsten Leemhuis
自願擔任 Linux 核心的迴歸追蹤者來留意這些事，偶爾也有其他人協助。他們都
沒有因此獲得報酬，所以迴歸追蹤是盡力而為的。

先前手動追蹤迴歸的嘗試顯示，這是一項令人筋疲力盡又沮喪的工作，因此在一段
時間後就被放棄了。為了避免這種情況再次發生，Thorsten 開發了 regzbot 來協助
這項工作，長期目標是盡可能為所有相關人員自動化迴歸追蹤。

regzbot 如何進行迴歸追蹤？
~~~~~~~~~~~~~~~~~~~~~~~~~~

這個機器人會留意已追蹤迴歸的報告所收到的回覆。此外，它也會尋找以
「Closes:」標籤引用這些報告、已發布或已提交（commit）的修補程式；對這些
修補程式貼文的回覆也會被追蹤。綜合這些資料，就能清楚了解修復過程目前的
狀態。

regzbot 盡量以最少的額外負擔為報告者和開發者完成工作。事實上，只有報告者
多了一項額外的責任：他們需要使用上述的 ``#regzbot introduced`` 命令，把
迴歸報告告知 regzbot；如果他們沒有這麼做，其他人可以使用
``#regzbot ^introduced`` 代為處理。

對開發者而言，通常不需要額外的工作，只需要確實做到早在 regzbot 出現之前
就被期望做的事：在修補程式描述中加上連結，指向所有關於所修復問題的報告。

我一定要使用 regzbot 嗎？
~~~~~~~~~~~~~~~~~~~~~~~~~

如果你使用，這對所有人都有好處，因為像 Linus Torvalds 這樣的核心維護者在
工作中部分依賴 regzbot 的追蹤，例如在決定要發布新版本或延長開發階段時。
為此，他們需要知道所有尚未修復的迴歸；眾所周知，Linus 會查看 regzbot 每週
發送的報告。

我一定要把遇到的每個迴歸都告訴 regzbot 嗎？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

理想上是的：我們都是凡人，當更重要的事情突然出現時很容易忘記問題，例如
Linux 核心中更大的問題，或是現實生活中讓我們有一陣子無法碰鍵盤的事情。
因此，最好把每個迴歸都告訴 regzbot，除非你立即寫出修正，並把它提交到一個
會定期合併到受影響核心系列的樹中。

如何查看 regzbot 目前追蹤哪些迴歸？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

請查看 `regzbot 的網頁介面 <https://linux-regtracking.leemhuis.info/regzbot/>`_
以取得最新資訊；或者，`搜尋最新的迴歸報告
<https://lore.kernel.org/lkml/?q=%22Linux+regressions+report%22+f%3Aregzbot>`_，
regzbot 通常每週日晚上（UTC）發送一次這份報告，也就是 Linus 通常發布新的
版本或預發布版本的幾個小時之前。

regzbot 監看哪些地方？
~~~~~~~~~~~~~~~~~~~~~~

regzbot 會監看最重要的 Linux 郵件列表，以及 linux-next、主線和穩定版／
長期支援版的 git 儲存庫。

哪些問題應該由 regzbot 追蹤？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

這個機器人是用來追蹤迴歸的，因此請不要讓 regzbot 處理一般問題。不過，如果
你用 regzbot 追蹤嚴重的問題，例如卡死（hang）、資料損毀或內部錯誤（Panic、
Oops、BUG()、warning……）的報告，Linux 核心的迴歸追蹤者也可以接受。

可以把 CI 系統發現的迴歸加入 regzbot 的追蹤嗎？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

可以，只要該迴歸很可能影響實際的使用情境，因而可能被使用者注意到即可；
因此，請不要讓 regzbot 處理不太可能在實際使用中出現的理論上的迴歸。

如何與 regzbot 互動？
~~~~~~~~~~~~~~~~~~~~~

在直接或間接回覆迴歸報告郵件時使用「regzbot 命令」。這些命令必須自成一個
段落（換句話說：必須用空行與郵件的其他內容分隔開）。

其中一個命令是 ``#regzbot introduced: <version or commit>``，如前所述，它會
讓 regzbot 把你的郵件視為一份加入追蹤的迴歸報告；另一個這樣的命令是
``#regzbot ^introduced: <version or commit>``，它會讓 regzbot 把上層郵件
視為一份迴歸報告並開始追蹤。

一旦使用了這兩個命令之一，就可以在直接或間接回覆該報告時使用其他 regzbot
命令。你可以把它們寫在某個 `introduced` 命令的下方，或寫在回覆以下郵件的
郵件中：使用了其中一個命令的郵件，或本身是回覆該郵件的郵件：

 * 設定或更新標題::

       #regzbot title: foo

 * 監看討論該問題其他面向或修正的討論串或 bugzilla.kernel.org 工單，例如
   修復該迴歸的修補程式貼文::

       #regzbot monitor: https://lore.kernel.org/all/30th.anniversary.repost@klaava.Helsinki.FI/

   監看功能只適用於 lore.kernel.org 和 bugzilla.kernel.org；regzbot 會把
   該討論串或工單中的所有訊息都視為與修復過程有關。

 * 指向一個有其他值得注意之細節的地方，例如稍微相關、但主題不同的郵件列表
   貼文或缺陷追蹤器中的工單::

       #regzbot link: https://bugzilla.kernel.org/show_bug.cgi?id=123456789

 * 將迴歸標記為已由某個正在送往上游或已經合併的提交修復::

       #regzbot fix: 1f2e3d4c5d

 * 將迴歸標記為另一個已由 regzbot 追蹤之迴歸的重複::

       #regzbot dup-of: https://lore.kernel.org/all/30th.anniversary.repost@klaava.Helsinki.FI/

 * 將迴歸標記為無效::

       #regzbot invalid: wasn't a regression, problem has always existed

關於 regzbot 及其命令還有更多資訊嗎？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

關於 Linux 核心迴歸追蹤機器人更詳細且最新的資訊，可以在它的
`專案頁面 <https://gitlab.com/knurd42/regzbot>`_ 找到，其中包括
`入門指南 <https://gitlab.com/knurd42/regzbot/-/blob/main/docs/getting_started.md>`_
和 `參考文件 <https://gitlab.com/knurd42/regzbot/-/blob/main/docs/reference.md>`_，
兩者涵蓋的細節都比上面這一節更多。

Linus 關於迴歸的發言
--------------------

以下是 Linus Torvalds 的一些發言，有助於了解 Linux 的「無迴歸」規則，以及
他期望如何處理迴歸：

迴歸應該多快修復
~~~~~~~~~~~~~~~~

* 出自 `2026-01-22 <https://lore.kernel.org/all/CAHk-=wheQNiW_WtHGO7bKkT7Uib-p+ai2JP9M+z+FYcZ6CAxYA@mail.gmail.com/>`_::

    But a user complaining should basically result in an immediate fix -
    possibly a "revert and rethink".

  稍後在 `2026-01-28 <https://lore.kernel.org/all/CAHk-%3Dwi86AosXs66-yi54%2BmpQjPu0upxB8ZAfG%2BLsMyJmcuMSA@mail.gmail.com/>`_ 又進一步說明::

    It's also worth noting that "immediate" obviously doesn't mean "right
    this *second* when the problem has been reported".

    But if it's a regression with a known commit that caused it, I think
    the rule of thumb should generally be "within a week", preferably
    before the next rc.

* 出自 `2023-04-21 <https://lore.kernel.org/all/CAHk-=wgD98pmSK3ZyHk_d9kZ2bhgN6DuNZMAJaV0WTtbkf=RDw@mail.gmail.com/>`_::

    Known-broken commits either
     (a) get a timely fix that doesn't have other questions
    or
     (b) get reverted

* 出自 `2021-09-20(2) <https://lore.kernel.org/all/CAHk-=wgOvmtRw1TNbMC1rn5YqyTKyn0hz+sc4k0DGNn++u9aYw@mail.gmail.com/>`_::

    [...] review shouldn't hold up reported regressions of existing code. That's
    just basic _testing_ - either the fix should be applied, or - if the fix is
    too invasive or too ugly - the problematic source of the regression should
    be reverted.

    Review should be about new code, it shouldn't be holding up "there's a
    bug report, here's the obvious fix".

* 出自 `2023-05-08 <https://lore.kernel.org/all/CAHk-=wgzU8_dGn0Yg+DyX7ammTkDUCyEJ4C=NvnHRhxKWC7Wpw@mail.gmail.com/>`_::

    If something doesn't even build, it should damn well be fixed ASAP.

以撤銷來修復迴歸如何有助於避免維護者過勞
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-01-28 <https://lore.kernel.org/all/CAHk-%3Dwi86AosXs66-yi54%2BmpQjPu0upxB8ZAfG%2BLsMyJmcuMSA@mail.gmail.com/>`_::

    > So how can I/we make "immediate fixes" happen more often without
    > contributing to maintainer burnout?

    [...] the "revert and rethink" model [...] often a good idea in general [...]

    Exactly so that maintainers don't get stressed out over having a pending
    problem report that people keep pestering them about.

    I think people are sometimes a bit too bought into whatever changes
    they made, and reverting is seen as "too drastic", but I think it's
    often the quick and easy solution for when there isn't some obvious
    response to a regression report.

最後一個 -rc 或新版本即將發布時，將修正合併進主線
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-02-01 <https://lore.kernel.org/all/CAHk-%3DwhXTw1oPsa%2BTLuY1Rc9D1OAiPVOdR_-R2xG45kwDObKdA@mail.gmail.com/>`_::

    So I think I'd rather see them hit rc8 (later today) and have a week
    of testing in my tree and be reverted if they cause problems, than
    have them go in after rc8 and then cause problems in the 6.19 release
    instead.

* 出自 `2023-04-20 <https://lore.kernel.org/all/CAHk-=wis_qQy4oDNynNKi5b7Qhosmxtoj1jxo5wmB6SRUwQUBQ@mail.gmail.com/>`_::

    But something like this, where the regression was in the previous release
    and it's just a clear fix with no semantic subtlety, I consider to be just a
    regular regression that should be expedited - partly to make it into stable,
    and partly to avoid having to put the fix into _another_ stable kernel.

只為單一修正發送合併請求
~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2024-04-24 <https://lore.kernel.org/all/CAHk-=wjy_ph9URuFt-pq+2AJ__p7gFDx=yzVSCsx16xAYvNw9g@mail.gmail.com/>`_::

    If the issue is just that there's nothing else happening, I think people
    should just point me to the patch and say "can you apply this single fix?"

* 出自 `2023-04-20 <https://lore.kernel.org/all/CAHk-=wis_qQy4oDNynNKi5b7Qhosmxtoj1jxo5wmB6SRUwQUBQ@mail.gmail.com/>`_::

    I'm always open to direct fixes when there is no controversy about the fix.
    No problem. I still happily deal with individual patches.

使用 Link:/Closes: 標籤指向缺陷報告的重要性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2025-07-29(1) <https://lore.kernel.org/all/CAHk-=wj2kJRPWx8B09AAtzj+_g+T6UBX11TP0ebs1WJdTtv=WQ@mail.gmail.com/>`_::

    [...] revert like this, it really would be good to link to the problems, so
    that when people try to re-enable it, they have the history for why it
    didn't work the first time.

* 出自 `2022-05-08 <https://lore.kernel.org/all/CAHk-=wjMmSZzMJ3Xnskdg4+GGz=5p5p+GSYyFBTh0f-DgvdBWg@mail.gmail.com/>`_::

    So I have to once more complain [...]

    [...] There's no link to the actual problem the patch fixes.

* 出自 `2022-06-22 <https://lore.kernel.org/all/CAHk-=wjxzafG-=J8oT30s7upn4RhBs6TX-uVFZ5rME+L5_DoJA@mail.gmail.com/>`_::

    See, *that* link [to the report] would have been useful in the commit.

為什麼會有「無迴歸」規則
~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-01-22 <https://lore.kernel.org/all/CAHk-=wheQNiW_WtHGO7bKkT7Uib-p+ai2JP9M+z+FYcZ6CAxYA@mail.gmail.com/>`_::

    But the basic rule is: be so good about backwards compatibility that
    users never have to worry about upgrading. They should absolutely feel
    confident that any kernel-reported problem will either be solved, or
    have an easy solution that is appropriate for *them* (ie a
    non-technical user shouldn't be expected to be able to do a lot).

    Because the last thing we want is people holding back from trying new
    kernels.

* 出自 `2024-05-28 <https://lore.kernel.org/all/CAHk-=wgtb7y-bEh7tPDvDWru7ZKQ8-KMjZ53Tsk37zsPPdwXbA@mail.gmail.com/>`_::

    I introduced that "no regressions" rule something like two decades
    ago, because people need to be able to update their kernel without
    fear of something they relied on suddenly stopping to work.

* 出自 `2018-08-03 <https://lore.kernel.org/all/CA+55aFwWZX=CXmWDTkDGb36kf12XmTehmQjbiMPCqCRG2hi9kw@mail.gmail.com/>`_::

    The whole point of "we do not regress" is so that people can upgrade
    the kernel and never have to worry about it.

    [...]

    Because the only thing that matters IS THE USER.

* 出自 `2017-10-26(1) <https://lore.kernel.org/lkml/CA+55aFxW7NMAMvYhkvz1UPbUTUJewRt6Yb51QAx5RtrWOwjebg@mail.gmail.com/>`_::

    If the kernel used to work for you, the rule is that it continues to work
    for you.

    [...]

    People should basically always feel like they can update their kernel
    and simply not have to worry about it.

    I refuse to introduce "you can only update the kernel if you also
    update that other program" kind of limitations. If the kernel used to
    work for you, the rule is that it continues to work for you.

「無迴歸」規則的例外
~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-01-22 <https://lore.kernel.org/all/CAHk-=wheQNiW_WtHGO7bKkT7Uib-p+ai2JP9M+z+FYcZ6CAxYA@mail.gmail.com/>`_::

    There are _very_ few exceptions to that rule, the main one being "the
    problem was a fundamental huge and gaping security issue and we *had* to
    make that change, and we couldn't even make your limited use-case just
    continue to work".

    The other exception is "the problem was reported years after it was
    introduced, and now most people rely on the new behavior".

    [...]

    Now, if it's one or two users and you can just get them to recompile,
    that's one thing. Niche hardware and odd use-cases can sometimes be
    solved that way, and regressions can sometimes be fixed by handholding
    every single reporter if the reporter is willing and able to change
    his or her workflow.

* 出自 `2023-04-20 <https://lore.kernel.org/all/CAHk-=wis_qQy4oDNynNKi5b7Qhosmxtoj1jxo5wmB6SRUwQUBQ@mail.gmail.com/>`_::

    And yes, I do consider "regression in an earlier release" to be a
    regression that needs fixing.

    There's obviously a time limit: if that "regression in an earlier
    release" was a year or more ago, and just took forever for people to
    notice, and it had semantic changes that now mean that fixing the
    regression could cause a _new_ regression, then that can cause me to
    go "Oh, now the new semantics are what we have to live with".

* 出自 `2017-10-26(2) <https://lore.kernel.org/lkml/CA+55aFxW7NMAMvYhkvz1UPbUTUJewRt6Yb51QAx5RtrWOwjebg@mail.gmail.com/>`_::

    There have been exceptions, but they are few and far between, and they
    generally have some major and fundamental reasons for having happened,
    that were basically entirely unavoidable, and people _tried_hard_ to
    avoid them. Maybe we can't practically support the hardware any more
    after it is decades old and nobody uses it with modern kernels any
    more. Maybe there's a serious security issue with how we did things,
    and people actually depended on that fundamentally broken model. Maybe
    there was some fundamental other breakage that just _had_ to have a
    flag day for very core and fundamental reasons.

更新使用者空間的某些東西即可解決迴歸的情況
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2018-08-03 <https://lore.kernel.org/all/CA+55aFwWZX=CXmWDTkDGb36kf12XmTehmQjbiMPCqCRG2hi9kw@mail.gmail.com/>`_::

    And dammit, we upgrade the kernel ALL THE TIME without upgrading any
    other programs at all. It is absolutely required, because flag-days
    and dependencies are horribly bad.

    And it is also required simply because I as a kernel developer do not
    upgrade random other tools that I don't even care about as I develop the
    kernel, and I want any of my users to feel safe doing the same time.

* 出自 `2017-10-26(3) <https://lore.kernel.org/lkml/CA+55aFxW7NMAMvYhkvz1UPbUTUJewRt6Yb51QAx5RtrWOwjebg@mail.gmail.com/>`_::

    But if something actually breaks, then the change must get fixed or
    reverted. And it gets fixed in the *kernel*. Not by saying "well, fix your
    user space then". It was a kernel change that exposed the problem, it needs
    to be the kernel that corrects for it, because we have a "upgrade in place"
    model. We don't have a "upgrade with new user space".

    And I seriously will refuse to take code from people who do not understand
    and honor this very simple rule.

    This rule is also not going to change.

    And yes, I realize that the kernel is "special" in this respect. I'm proud
    of it.

* 出自 `2017-10-26(4) <https://lore.kernel.org/all/CA+55aFwiiQYJ+YoLKCXjN_beDVfu38mg=Ggg5LFOcqHE8Qi7Zw@mail.gmail.com/>`_::

    If you break existing user space setups THAT IS A REGRESSION.

    It's not ok to say "but we'll fix the user space setup".

    Really. NOT OK.

什麼算是使用者空間介面、ABI、API、有文件記載的介面等
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-01-20 <https://lore.kernel.org/all/CAHk-=wga8Qu0-OSE9VZbviq9GuqwhPhLUXeAt-S7_9+fMCLkKg@mail.gmail.com/>`_::

    So I absolutely detest the whole notion of "ABI changes". It's a
    meaningless concept, and I hate it with a passion, [...]

    The Linux rule for regressions is basically based on the philosophical
    question of "If a tree falls in the forest, and nobody is around to
    hear it, does it make a sound?".

    So the only thing that matters is if something breaks user-*conscious*
    behavior.

    And when that happens, the distinction between "bug fix" and "new
    feature" and "ABI change" matters not one whit, and the change needs
    to be done differently.

    [...]

    I just wanted to point out that the argument about whether it's an ABI
    change or not is irrelevant. If it turns out that some program - not a test
    script, but something with relevance to conscious user expectations ~
    depended on the old broken behavior, then it needs to be done some other
    way.

* 出自 `2026-02-13 <https://lore.kernel.org/all/CAHk-=whY-N8kjm8kiFUV5Ei-8AuYw--EPGD-AR3Pd+5GTx2sAQ@mail.gmail.com/>`_::

    > [...] this should not fall under the don't break user space rule [...]

    Note that the rule is about breaking *users*, not breaking user space per
    se. [...]

    If some user setup breaks, things need fixing.

    [...] but I want to make it very clear that there are no excuses about "user
    space applications".

* 出自 `2021-09-20(4) <https://lore.kernel.org/all/CAHk-=wi7DB2SJ-wngVvsJ7Ak2cM556Q8437sOXo4EJt2BWPdEg@mail.gmail.com/>`_::

    [...] a regression is a bit like Schrödinger's cat - if nobody is around
    to notice it and it doesn't actually affect any real workload, then you
    can treat the regression as if it doesn't exist.

* 出自 `2020-05-21 <https://lore.kernel.org/all/CAHk-=wiVi7mSrsMP=fLXQrXK_UimybW=ziLOwSzFTtoXUacWVQ@mail.gmail.com/>`_::

    The rules about regressions have never been about any kind of documented
    behavior, or where the code lives.

    The rules about regressions are always about "breaks user workflow".

    Users are literally the _only_ thing that matters.

* 出自 `2019-09-15 <https://lore.kernel.org/lkml/CAHk-=wiP4K8DRJWsCo=20hn_6054xBamGKF2kPgUzpB5aMaofA@mail.gmail.com/>`_::

    One _particularly_ last-minute revert is the top-most commit (ignoring
    the version change itself) done just before the release, and while
    it's very annoying, it's perhaps also instructive.

    What's instructive about it is that I reverted a commit that wasn't
    actually buggy. In fact, it was doing exactly what it set out to do,
    and did it very well. In fact it did it _so_ well that the much
    improved IO patterns it caused then ended up revealing a user-visible
    regression due to a real bug in a completely unrelated area.

    The actual details of that regression are not the reason I point that
    revert out as instructive, though. It's more that it's an instructive
    example of what counts as a regression, and what the whole "no
    regressions" kernel rule means.

    [...] The reverted commit didn't change any API's, and it didn't introduce
    any new bugs. But it ended up exposing another problem, and as such caused
    a kernel upgrade to fail for a user. So it got reverted.

    The point here being that we revert based on user-reported _behavior_, not
    based on some "it changes the ABI" or "it caused a bug" concept. The problem
    was really pre-existing, and it just didn't happen to trigger before. [...]

    Take-away from the whole thing: it's not about whether you change the
    kernel-userspace ABI, or fix a bug, or about whether the old code
    "should never have worked in the first place". It's about whether
    something breaks existing users' workflow.

* 出自 `2017-11-05 <https://lore.kernel.org/all/CA+55aFzUvbGjD8nQ-+3oiMBx14c_6zOj2n7KLN3UsJ-qsd4Dcw@mail.gmail.com/>`_::

    And our regression rule has never been "behavior doesn't change".
    That would mean that we could never make any changes at all.

* 出自 `2020-05-21 <https://lore.kernel.org/all/CAHk-=wiVi7mSrsMP=fLXQrXK_UimybW=ziLOwSzFTtoXUacWVQ@mail.gmail.com/>`_::

    No amount of "you shouldn't have used this" or "that behavior was
    undefined, it's your own fault your app broke" or "that used to work
    simply because of a kernel bug" is at all relevant.

* 出自 `2021-05-21 <https://lore.kernel.org/all/CAHk-=wiVi7mSrsMP=fLXQrXK_UimybW=ziLOwSzFTtoXUacWVQ@mail.gmail.com/>`_::

    But no, "that was documented to be broken" (whether it's because the code
    was in staging or because the man-page said something else) is irrelevant.
    If staging code is so useful that people end up using it, that means that
    it's basically regular kernel code with a flag saying "please clean this
    up".

    [...]

    The other side of the coin is that people who talk about "API stability" are
    entirely wrong. API's don't matter either. You can make any changes to an
    API you like - as long as nobody notices.

    Again, the regression rule is not about documentation, not about API's, and
    not about the phase of the moon.

* 出自 `2012-07-06 <https://lore.kernel.org/all/CA+55aFwnLJ+0sjx92EGREGTWOx84wwKaraSzpTNJwPVV8edw8g@mail.gmail.com/>`_::

    > Now this got me wondering if Debian _unstable_ actually qualifies as a
    > standard distro userspace.

    Oh, if the kernel breaks some standard user space, that counts. Tons
    of people run Debian unstable

* 出自 `2011-05-06 <https://lore.kernel.org/all/BANLkTi=KVXjKR82sqsz4gwjr+E0vtqCmvA@mail.gmail.com/>`_::

    It's clearly NOT an internal tracepoint. By definition. It's being
    used by powertop.

使用者或測試套件／CI 發現的迴歸
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2026-01-22 <https://lore.kernel.org/all/CAHk-=wheQNiW_WtHGO7bKkT7Uib-p+ai2JP9M+z+FYcZ6CAxYA@mail.gmail.com/>`_::

    Users complaining is the only real line in the end.

    [...] a test-suite complaining is then often a *very* good indication that
    maybe users will hit some problem, and test suite issues should be taken
    very seriously [...]

    But a test-suite error isn't necessarily where you have to draw the
    line - it's a big red flag [...]

* 出自 `2024-29-01 <https://lore.kernel.org/all/CAHk-=wg8BrZEzjJ5kUyZzHPZmFqH6ooMN1gRBCofxxCfucgjaw@mail.gmail.com/>`_::

    The "no regressions" rule is not about made-up "if I do this, behavior
    changes".

    The "no regressions" rule is about *users*.

    If you have an actual user that has been doing insane things, and we
    change something, and now the insane thing no longer works, at that
    point it's a regression, and we'll sigh, and go "Users are insane" and
    have to fix it.

    But if you have some random test that now behaves differently, it's
    not a regression. It's a *warning* sign, sure: tests are useful.

承認迴歸的發生
~~~~~~~~~~~~~~

* 出自 `2026-01-22 <https://lore.kernel.org/all/CAHk-=wheQNiW_WtHGO7bKkT7Uib-p+ai2JP9M+z+FYcZ6CAxYA@mail.gmail.com/>`_::

    But starting to argue about users reporting breaking changes is
    basically the final line for me. I have a couple of people that I have
    in my spam block-list and refuse to have anything to do with, and they
    have generally been about exactly that.

    Note how it's not about making mistakes and _causing_ the regression.
    That's normal. That's development. But then arguing about it is a
    no-no.

* 出自 `2024-06-23 <https://lore.kernel.org/all/CAHk-=wi_KMO_rJ6OCr8mAWBRg-irziM=T9wxGC+J1VVoQb39gw@mail.gmail.com/>`_::

    We don't introduce regressions and then blame others.

    There's a very clear rule in kernel development: things that break
    other things ARE NOT FIXES.

    EVER.

    They get reverted, or the thing they broke gets fixed.

* 出自 `2021-06-05 <https://lore.kernel.org/all/CAHk-=wiUVqHN76YUwhkjZzwTdjMMJf_zN4+u7vEJjmEGh3recw@mail.gmail.com/>`_::

    THERE ARE NO VALID ARGUMENTS FOR REGRESSIONS.

    Honestly, security people need to understand that "not working" is not
    a success case of security. It's a failure case.

    Yes, "not working" may be secure. But security in that case is *pointless*.

* 出自 `2017-10-26(5) <https://lore.kernel.org/lkml/CA+55aFwiiQYJ+YoLKCXjN_beDVfu38mg=Ggg5LFOcqHE8Qi7Zw@mail.gmail.com/>`_::

    [...] when regressions *do* occur, we admit to them and fix them, instead of
    blaming user space.

    The fact that you have apparently been denying the regression now for
    three weeks means that I will revert, and I will stop pulling apparmor
    requests until the people involved understand how kernel development
    is done.

反覆來回
~~~~~~~~

* 出自 `2024-05-28 <https://lore.kernel.org/all/CAHk-=wgtb7y-bEh7tPDvDWru7ZKQ8-KMjZ53Tsk37zsPPdwXbA@mail.gmail.com/>`_::

    The "no regressions" rule is that we do not introduce NEW bugs.

    It *literally* came about because we had an endless dance of "fix two
    bugs, introduce one new one", and that then resulted in a system that
    you cannot TRUST.

* 出自 `2021-09-20(1) <https://lore.kernel.org/all/CAHk-=wi7DB2SJ-wngVvsJ7Ak2cM556Q8437sOXo4EJt2BWPdEg@mail.gmail.com/>`_::

    And the thing that makes regressions special is that back when I
    wasn't so strict about these things, we'd end up in endless "seesaw
    situations" where somebody would fix something, it would break
    something else, then that something else would break, and it would
    never actually converge on anything reliable at all.

* 出自 `2015-08-13 <https://lore.kernel.org/all/CA+55aFxk8-BsiKwr_S-c+4G6wihKPQVMLE34H9wOZpeua6W9+Q@mail.gmail.com/>`_::

    The strict policy of no regressions actually originally started mainly wrt
    suspend/resume issues, where the "fix one machine, break another" kind of
    back-and-forth caused endless problems, and meant that we didn't actually
    necessarily make any forward progress, just moving a problem around.

有造成迴歸風險的變更
~~~~~~~~~~~~~~~~~~~~

* 出自 `2023-06-02 <https://lore.kernel.org/all/CAHk-=wgyAGUMHmQM-5Eb556z5xiHZB7cF05qjrtUH4F7P-1rSA@mail.gmail.com/>`_::

    So what I think you should do is to fix the bug right, with a clean
    patch, and no crazy hacks. That is something we can then apply and
    test. All the while knowing full well that "uhhuh, this is a visible
    change, we may have to revert it".

    If then some *real* load ends up showing a regression, we may just be
    screwed. Our current behavior may be buggy, but we have the rule that
    once user space depends on kernel bugs, they become features pretty
    much by definition, however much we might dislike it.

以核心內的權宜做法避免迴歸
~~~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2017-10-26(6) <https://lore.kernel.org/lkml/CA+55aFxW7NMAMvYhkvz1UPbUTUJewRt6Yb51QAx5RtrWOwjebg@mail.gmail.com/>`_::

    Behavioral changes happen, and maybe we don't even support some
    feature any more. There's a number of fields in /proc/<pid>/stat that
    are printed out as zeroes, simply because they don't even *exist* in
    the kernel any more, or because showing them was a mistake (typically
    an information leak). But the numbers got replaced by zeroes, so that
    the code that used to parse the fields still works. The user might not
    see everything they used to see, and so behavior is clearly different,
    but things still _work_, even if they might no longer show sensitive
    (or no longer relevant) information.

缺陷修正造成的迴歸
~~~~~~~~~~~~~~~~~~

* 出自 `2018-08-03 <https://lore.kernel.org/all/CA+55aFwWZX=CXmWDTkDGb36kf12XmTehmQjbiMPCqCRG2hi9kw@mail.gmail.com/>`_::

    > Kernel had a bug which has been fixed

    That is *ENTIRELY* immaterial.

    Guys, whether something was buggy or not DOES NOT MATTER.

    [...]

    It's basically saying "I took something that worked, and I broke it,
    but now it's better". Do you not see how f*cking insane that statement
    is?

內部 API 的變更
~~~~~~~~~~~~~~~

* 出自 `2017-10-26(7) <https://lore.kernel.org/lkml/CA+55aFxW7NMAMvYhkvz1UPbUTUJewRt6Yb51QAx5RtrWOwjebg@mail.gmail.com/>`_::

    We do API breakage _inside_ the kernel all the time. We will fix
    internal problems by saying "you now need to do XYZ", but then it's
    about internal kernel API's, and the people who do that then also
    obviously have to fix up all the in-kernel users of that API. Nobody
    can say "I now broke the API you used, and now _you_ need to fix it
    up". Whoever broke something gets to fix it too.

很久之後才發現的迴歸
~~~~~~~~~~~~~~~~~~~~

* 出自 `2024-03-28 <https://lore.kernel.org/all/CAHk-=wgFuoHpMk_Z_R3qMXVDgq0N1592+bABkyGjwwSL4zBtHA@mail.gmail.com/>`_::

    I'm definitely not reverting a patch from almost a decade ago as a
    regression.

    If it took that long to find, it can't be that critical of a regression.

    So yes, let's treat it as a regular bug.

在 linux-next 中測試迴歸修正
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 在 `2024 年維護者高峰會 <https://lwn.net/Articles/990599/>`_ 上::

   So running fixes though linux-next is just a waste of time.

與迴歸相關的其他幾個面向
~~~~~~~~~~~~~~~~~~~~~~~~

* 出自 `2025-07-29(2) <https://lore.kernel.org/all/CAHk-=wjj9DvOZtmTkoLtyfHmy5mNKy6q_96d9=4FUEDXre=cww@mail.gmail.com/>`_
  [這件事 `雖然不完全算是迴歸，但造成了極大的不便 <https://lore.kernel.org/all/CAHk-=wgO0Rx2LcYT4f75Xs46orbJ4JxO2jbAFQnVKDYAjV5HeQ@mail.gmail.com/>`_]::

    I no longer have sound.

    I also suspect that it's purely because "make oldconfig" doesn't work,
    and probably turned off my old Intel HDA settings. Or something.

    Renaming config parameters is *bad*. I've harped on the Kconfig phase
    of the kernel build probably being our nastiest point, and a real pain
    point to people getting involved with development simply because
    building your own kernel can be so daunting with hundreds of fairly
    esoteric questions.

..
   end-of-content
..
   如本文件開頭所述，本文以 GPL-2.0+ 或 CC-BY-4.0 授權提供。如果你想只以
   CC-BY-4.0 授權散布本文，請以「The Linux kernel developers」作為作者署名，
   並連結以下網址作為來源：
   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/process/handling-regressions.rst
..
   注意：只有在 Linux 核心原始碼中找到的本 RST 檔案內容才以 CC-BY-4.0 授權
   提供，因為經過處理的文字版本（例如經由核心的建置系統處理）可能包含取自
   授權較嚴格之檔案的內容。
