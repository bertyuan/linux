.. SPDX-License-Identifier: GPL-2.0-or-later

.. include:: ../disclaimer-zh_TW.rst

.. _tw_submittingpatches:

:Original: Documentation/process/submitting-patches.rst

提交補丁：如何讓你的改動進入核心
================================

對於想要將改動提交到 Linux 核心的個人或者公司來說，如果不熟悉“規矩”，
提交的流程會讓人畏懼。本文件包含了一系列建議，可以大大提高你
的改動被接受的機會.

本文件以較為簡潔的行文給出了大量建議。關於核心開發流程如何進行的詳細資訊，
參見： Documentation/translations/zh_TW/process/development-process.rst 。
Documentation/translations/zh_TW/process/submit-checklist.rst 給出了一系列
提交補丁之前要檢查的事項。裝置樹相關的補丁，請參閱
Documentation/devicetree/bindings/submitting-patches.rst 。

本文件假設您正在使用 ``git`` 準備你的補丁。如果您不熟悉 ``git`` ，最好學習
如何使用它，這將使您作為核心開發人員的生活變得更加輕鬆。

部分子系統和維護人員的樹有一些關於其工作流程和要求的額外資訊，請參閱
Documentation/process/maintainer-handbooks.rst 。

獲取目前的原始程式碼樹
----------------------

如果您手頭沒有目前核心原始程式碼的儲存庫，請使用 ``git`` 獲取一份。您需要先獲取
主線儲存庫，它可以透過以下命令拉取::

    git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

但是，請注意，您可能不想直接針對主線樹進行開發。大多數子系統維護人員運
行自己的樹，並希望看到針對這些樹準備的補丁。請參見MAINTAINERS檔案中子系
統的 **T:** 項以尋找該樹，或者直接詢問維護者該樹是否未在其中列出。

.. _tw_describe_changes:

描述你的改動
------------

描述你的問題。無論您的修補程式是一行錯誤修復還是 5000 行新功能，都必須有一個
潛在的問題激勵您完成這項工作。說服審閱者相信確實有一個值得解決的問題，而且值得
他們在讀完第一段之後繼續讀下去。

描述使用者可見的影響。直接崩潰和鎖定是相當有說服力的，但並不是所有的錯誤都
那麼明目張膽。即使在程式碼審閱期間發現了這個問題，也要描述一下您認為它可能
對使用者產生的影響。請記住，大多數Linux安裝執行的核心來自二級穩定樹或特定
於供應商/產品的樹，只從上游精選特定的補丁，因此請包含任何可以幫助您將更改
定位到下游的內容：觸發的場景、DMESG的摘錄、崩潰描述、效能迴歸、延遲尖峯、
鎖定等。

量化最佳化和權衡。如果您聲稱在效能、記憶體消耗、堆疊佔用空間或二進位大小方
面有所改進，請附上支持這些說法的資料。但也要描述不明顯的成本。最佳化通常不是
零成本的，而是在 CPU、記憶體和可讀性之間進行權衡；或者，在啟發式演算法方面，
是在不同的工作負載之間進行權衡。請描述最佳化的預期缺點，以便審閱者可以權衡
成本和收益。

提出問題之後，就要詳細地描述一下您實際在做的技術細節。對於審閱者來說，用簡練的
英語描述程式碼的變化是很重要的，以驗證程式碼的行為是否符合您的意圖。

如果您將補丁描述寫成“標準格式”，可以很容易地作為“提交日誌”放入Linux的源代
碼管理系統 ``git`` 中，那麼維護人員將非常感謝您。
參見 :ref:`tw_the_canonical_patch_format` 。

每個補丁只解決一個問題。如果你的描述開始變長，這就表明你可能需要拆分你的補丁。
請見 :ref:`tw_split_changes` 。

提交或重新提交補丁或補丁系列時，請包括完整的補丁說明和理由。不要只說這是補丁
（系列）的第幾版。不要期望子系統維護人員引用更早的補丁版本或引用URL來查
找補丁描述並將其放入補丁中。也就是說，補丁（系列）及其描述應該是獨立的。這
對維護人員和審閱者都有好處。一些審閱者可能甚至沒有收到補丁的早期版本。

用祈使句描述你的變更，例如“make xyzzy do frotz”而不是“[This patch]make
xyzzy do frotz”或“[I]changed xyzzy to do frotz”，就好像你在命令程式碼庫改變
它的行為一樣。

如果您想要引用一個特定的提交，不要只引用提交的SHA-1 ID。還請包括提交的一行
摘要，以便於審閱者瞭解它是關於什麼的。例如::

        Commit e21d2170f36602ae2708 ("video: remove unnecessary
        platform_set_drvdata()") removed the unnecessary
        platform_set_drvdata(), but left the variable "dev" unused,
        delete it.

您還應該確保至少使用前12位SHA-1 ID。核心儲存庫包含 *許多* 物件，使較短的ID
發生衝突的可能性很大。記住，即使現在不會與您的六個字元ID發生衝突，這種情況
也可能在五年後改變。

如果該變更的相關討論或其他背景資訊可以在網上查閱，請加上「Link:」標籤指向它。
如果該修補程式源自一些早先的郵件列表討論或網路上記錄的內容，請指向它。

當連結到郵件列表存檔時，請首選lore.kernel.org郵件存檔服務。用郵件中的
``Message-ID`` 頭（去掉尖括號）可以建立連結URL。例如::

    Link: https://lore.kernel.org/30th.anniversary.repost@klaava.Helsinki.FI

請檢查該連結以確保可用且指向正確的郵件。

不過，在沒有外部資源的情況下，也要儘量讓你的解釋可理解。除了提供郵件列表存檔或
缺陷的URL之外，還要需要總結該補丁的相關討論要點。

如果你的修補程式修復了一個錯誤，請使用「Closes:」標籤，並附上指向郵件列表存檔
或公開缺陷追蹤器中該報告的 URL。例如::

	Closes: https://example.com/issues/1234

有些缺陷追蹤器能夠在套用帶有此標籤的提交時自動關閉問題。有些監看郵件列表的
機器人也可以追蹤這類標籤並採取特定動作。禁止使用私有缺陷追蹤器和無效的 URL。

如果補丁修復了特定提交中的錯誤，例如使用 ``git bisect`` 發現了一個問題，請使用
帶有至少前12個字元SHA-1 ID的“Fixes:”標籤和單行摘要。為了簡化解析腳本，不要將該
標籤拆分為多行，標籤不受“75列換行”規則的限制。例如::

  Fixes: 54a4f0239f2e ("KVM: MMU: make kvm_mmu_zap_page() return the number of pages it actually freed")

下列 ``git config`` 設定可以讓 ``git log``、``git show`` 指令增加輸出上述風格
的格式::

	[core]
		abbrev = 12
	[pretty]
		fixes = Fixes: %h (\"%s\")

使用範例::

	$ git log -1 --pretty=fixes 54a4f0239f2e
	Fixes: 54a4f0239f2e ("KVM: MMU: make kvm_mmu_zap_page() return the number of pages it actually freed")

.. _tw_split_changes:

拆分你的改動
------------

將每個 **邏輯更改** 拆分成一個單獨的補丁。

例如，如果你的改動裡同時有bug修正和效能最佳化，那麼把這些改動拆分到兩個或
者更多的補丁檔案中。如果你的改動包含對API的修改，並且增加了一個使用該新API
的驅動，那麼把這些修改分成兩個補丁。

另一方面，如果你對許多檔案做了同一個改動，那麼把這些改動合併成一個修補程式。
這樣一個邏輯上單獨的改動只被包含在一個修補程式裡。

需要記住的一點是，每個修補程式的更改都應易於理解，以便審閱者驗證。每個修補程式
本身都應該有成立的理由。

如果有一個補丁依賴另外一個補丁來完成它的改動，那沒問題。直接在你的補丁
描述裡指出 **“這個補丁依賴某補丁”** 就好了。

在將您的更改劃分為一系列補丁時，要特別注意確保核心在應用系列中的每個補丁之後
都能正常建置和執行。使用 ``git bisect`` 來追蹤問題的開發者可能會在任何地方分
割你的補丁系列；如果你在中間引入錯誤，他們不會感謝你。

如果你不能將補丁系列濃縮得更小，那麼每次大約發送出15個補丁，然後等待審閱
和整合。

檢查你的更改風格
----------------

檢查您的修補程式是否違反了基本樣式規定，詳細資訊可在
Documentation/translations/zh_TW/process/coding-style.rst
中找到。如果不這樣做，只會浪費審閱者的時間，並且會導致你的補丁被拒絕，甚至
可能沒有被閱讀。

一個重要的例外是在將程式碼從一個檔案移動到另一個檔案時——在這種情況下，您不
應該在移動程式碼的同一個補丁中修改移動的程式碼。這清楚地描述了移動程式碼和
您的更改的行為。這大大有助於審閱實際差異，並允許工具更好地追蹤程式碼本身的
歷史。

在提交之前，使用補丁樣式檢查程式檢查補丁（scripts/checkpatch.pl）。不過，
請注意，樣式檢查程式應該被視為一個指南，而不是作為人類判斷的替代品。如果您
的程式碼看起來更好，但有違規行為，那麼最好別管它。

檢查者報告三個級別：
 - ERROR：很可能出錯的事情
 - WARNING：需要仔細審閱的事項
 - CHECK：需要思考的事情

您應該能夠說明您的修補程式中仍然存在的所有違規行為的理由。

選擇補丁收件人
--------------

對於任何修改程式碼的修補程式，您都應該抄送給維護該程式碼的子系統維護人員及
郵件列表；查閱 MAINTAINERS 檔案和原始程式碼修訂歷史記錄，以瞭解這些維護人員
是誰。腳本 scripts/get_maintainer.pl 在這個步驟中非常有用（把你的修補程式的
路徑作為參數傳給 scripts/get_maintainer.pl）。如果您找不到正在工作的子系統的
維護人員，那麼 Andrew Morton（akpm@linux-foundation.org）將充當最後的維護
人員。

所有修補程式預設都應發送到 linux-kernel@vger.kernel.org，但這個列表的流量已經
導致了許多開發人員不再看它。不過，請不要向無關的列表和無關的人發送垃圾郵件。

許多與核心相關的列表託管在kernel.org上；您可以在
https://subspace.kernel.org 上找到它們的列表。不過，也有與核心相關
的列表託管在其他地方。

Linus Torvalds是決定改動能否進入 Linux 核心的最終裁決者。他的郵件地址是
<torvalds@linux-foundation.org>。他收到的郵件很多，而且目前很少有修補程式
直接經由 Linus 合入，所以一般來說你應該盡量 **避免** 寄信給他。

如果您有修復可利用安全漏洞的補丁，請將該補丁發送到 security@kernel.org 。
對於嚴重的bug，可以考慮短期禁令以允許分銷商（有時間）向使用者發布補丁；在
這種情況下，顯然不應將補丁發送到任何公共列表。參見
Documentation/process/security-bugs.rst 。

修復已發布核心中嚴重錯誤的補丁程式應該抄送給穩定版維護人員，方法是把以下列行
放進補丁的簽署區（注意，不是電子郵件收件人）::

  Cc: stable@vger.kernel.org

除了本文件之外，您還應該閱讀
Documentation/translations/zh_TW/process/stable-kernel-rules.rst 。

如果更改影響到使用者側核心介面，請向手冊頁維護人員（如MAINTAINERS檔案中所
列）發送手冊頁補丁，或至少發送更改通知，以便一些資訊進入手冊頁。還應將使用
者空間API更改抄送到 linux-api@vger.kernel.org 。


不要MIME編碼，不要連結，不要壓縮，不要附件，只要純文字
------------------------------------------------------

Linus 和其他的核心開發者需要閱讀和評論你提交的改動。對於核心開發者來說
，可以“引用”你的改動很重要，使用一般的郵件工具，他們就可以在你的
程式碼的任何位置添加評論。

因為這個原因，所有的提交的補丁都是郵件中“內嵌”的。最簡單（和推薦）的方法就
是使用 ``git send-email`` 。https://git-send-email.io 有 ``git send-email``
的互動式教學。

如果你選擇不用 ``git send-email`` ：

.. warning::

  如果你使用剪下-貼上你的補丁，小心你的編輯器的自動換行功能破壞你的補丁

不要將補丁作為MIME編碼的附件，不管是否壓縮。很多流行的郵件軟體不
是任何時候都將MIME編碼的附件當作純文字發送的，這會使得別人無法在你的
程式碼中加評論。另外，MIME編碼的附件會讓Linus多花一點時間來處理，這就
降低了你的改動被接受的可能性。

例外：如果你的郵路損壞了補丁，那麼有人可能會要求你使用MIME重新發送補丁。

請參閱 Documentation/translations/zh_TW/process/email-clients.rst
以獲取有關設定電子郵件用戶端以使其不受影響地發送補丁的提示。

回覆審閱意見
------------

你的補丁幾乎肯定會得到審閱者對補丁改進方法的評論（以回覆郵件的形式）。您必須
對這些評論作出回應；讓補丁被忽略的一個好辦法就是忽略審閱者的意見。直接回復郵
件來回應意見即可。不會導致程式碼更改的意見或問題幾乎肯定會帶來註解或變更日誌的
改變，以便下一個審閱者更好地瞭解正在發生的事情。

一定要告訴審閱者你在做什麼改變，並感謝他們的時間。程式碼審閱是一個累人且耗時的
過程，審閱者有時會變得暴躁。即使在這種情況下，也要禮貌地回應並解決他們指出的
問題。當發送下一版時，在封面郵件或獨立補丁里加上 ``patch changelog`` 說明與
前一版本的不同之處（參見 :ref:`tw_the_canonical_patch_format` ）。
發布新版本時，請把曾對你的修補程式提出意見的人加進修補程式的 CC 列表，讓他們
知道有新版本。

關於電子郵件用戶端的建議和郵件列表禮儀，請參閱
Documentation/translations/zh_TW/process/email-clients.rst 。

.. _tw_interleaved_replies:

在郵件討論中使用裁剪過的交錯式回覆
----------------------------------

在Linux核心開發的討論中，強烈不建議置頂回覆（top-posting）。交錯式（或
“行內”）回覆使對話更容易理解。更多細節參見：
https://en.wikipedia.org/wiki/Posting_style#Interleaved_style

正如郵件列表中經常被引用的那樣::

  A: http://en.wikipedia.org/wiki/Top_post
  Q: Where do I find info about this thing called top-posting?
  A: Because it messes up the order in which people normally read text.
  Q: Why is top-posting such a bad thing?
  A: Top-posting.
  Q: What is the most annoying thing in e-mail?

同樣，請裁剪掉所有與你的回覆無關的引文。這使回覆更容易尋找，並節省時間和
空間。更多細節參見： http://daringfireball.net/2007/07/on_top ::

  A: No.
  Q: Should I include quotations after my reply?

.. _tw_resend_reminders:

不要泄氣或不耐煩
----------------

提交更改後，請耐心等待。審閱者是大忙人，可能無法立即審閱您的補丁。

曾幾何時，補丁曾在沒收到評論的情況下消失在虛空中，但現在開發過程應該更加順
利了。您應該在幾週內（通常是 2-3 週）收到評論；如果沒有收到評論，請確保您已
將修補程式發送到正確的位置。在重新提交或聯繫審閱者之前至少等待一週——在諸如
合併視窗之類的繁忙時間可能更長。

在等了幾個星期後，用帶RESEND的主題重發補丁也是可以的::

   [PATCH Vx RESEND] sub/sys: Condensed patch summary

當你發布補丁（系列）修改版的時候，不要加上“RESEND”——“RESEND”只適用於重
新提交之前未經修改的補丁（系列）。

主題中包含 PATCH
----------------

由於到Linus和linux-kernel的電子郵件流量很高，通常會在主題行前面加上[PATCH]
字首。這使Linus和其他核心開發人員更容易將補丁與其他電子郵件討論區分開。

``git send-email`` 會自動為你加上。

簽署你的作品——開發者來源認證
------------------------------

為了加強對誰做了何事的追蹤，尤其是對那些透過好幾層維護者才最終到達的補丁，我
們在透過郵件發送的補丁上引入了“簽署（sign-off）”流程。

「簽署」是在修補程式說明最後的一行簡單文字，認證你編寫了它，或者你有權將它
作為開放原始碼修補程式傳遞下去。規則很簡單：如果你能認證以下內容::

        Developer's Certificate of Origin 1.1

        By making a contribution to this project, I certify that:

        (a) The contribution was created in whole or in part by me and I
            have the right to submit it under the open source license
            indicated in the file; or

        (b) The contribution is based upon previous work that, to the best
            of my knowledge, is covered under an appropriate open source
            license and I have the right under that license to submit that
            work with modifications, whether created in whole or in part
            by me, under the same open source license (unless I am
            permitted to submit under a different license), as indicated
            in the file; or

        (c) The contribution was provided directly to me by some other
            person who certified (a), (b) or (c) and I have not modified
            it.

        (d) I understand and agree that this project and the contribution
            are public and that a record of the contribution (including all
            personal information I submit with it, including my sign-off) is
            maintained indefinitely and may be redistributed consistent with
            this project or the open source license(s) involved.

以下中文譯文僅供參考，以上方英文原文為準::

        開發者來源認證 1.1

        對於本專案的貢獻，我認證如下資訊：

        (a) 這些貢獻是完全或者部分的由我建立，我有權利以檔案中指出
            的開放原始碼許可證提交它；或者

        (b) 這些貢獻基於以前的工作，據我所知，這些以前的工作受恰當的
            開放原始碼許可證保護，而且我有權依據該許可證，以檔案中指出
            的同一個開放原始碼許可證（除非我被允許用其他的許可證）提交
            修改後的作品，無論修改是完全還是部分由我創造；或者

        (c) 這些貢獻由認證（a）、（b）或者（c）的人直接提供給我，而
            且我沒有修改它。

        (d) 我理解並同意這個專案和貢獻是公開的，貢獻的記錄（包括我
            一起提交的所有個人資訊，包括我的 sign-off）會被無限期保存，
            並且可以依照這個專案或相關的開放原始碼許可證再次散布。

那麼加入這樣一行::

  Signed-off-by: Random J Developer <random@developer.example.org>

使用已知的身分（抱歉，不接受匿名貢獻。）如果使用 ``git commit -s`` 的話
將會自動完成。撤銷也應當包含“Signed-off-by”， ``git revert -s`` 會幫你搞定。

有些人會在最後加上額外的標籤。現在這些東西會被忽略，但是你可以這樣做，來標記
公司內部的過程，或者只是指出關於簽署的一些特殊細節。

作者簽署之後的任何其他簽署（Signed-off-by:'s）均來自處理和傳遞補丁的人員，但
未參與其開發。簽署鏈應當反映補丁傳播到維護者並最終傳播到Linus所經過的 **真實**
路徑，首個簽署指明單個作者的主要作者身份。

何時使用Acked-by:，Cc:，和Co-developed-by:
------------------------------------------

Signed-off-by: 標籤表示簽名者參與了修補程式的開發，或者他們在修補程式的傳遞
路徑中。

如果一個人沒有直接參與補丁的準備或處理，但希望表示並記錄他們對補丁的批准/
贊成，那麼他們可以要求在補丁的變更日誌中新增一個Acked-by:。

Acked-by: 供以某種方式對受影響程式碼負責或與之相關的人使用。最常見的情況是，
當維護者既沒有貢獻也沒有轉寄補丁時，由該維護者使用。

Acked-by: 也可以由其他利益相關者使用，例如具有領域知識的人（例如被修改程式
碼的原作者）、核心uAPI補丁的使用者空間側審閱者，或某項功能的關鍵使用者。在
這些情況下，可以視需要加上一個“# 字尾”以澄清其含義::

	Acked-by: The Stakeholder <stakeholder@example.org> # As primary user

Acked-by: 不像簽署那樣正式。這是一個記錄，確認人至少審閱了補丁，並表示接受。
因此，補丁合併有時會手動將Acker的“Yep，looks good to me”轉換為 Acked-By:（但
請注意，通常最好要求一個明確的Ack）。

Acked-by: 也不如 Reviewed-by: 正式。例如，維護者可以用它表示他們同意補丁
合入，但可能沒有像提供Reviewed-by:那樣徹底地審閱過補丁。同樣，關鍵使用者
可能沒有對補丁進行技術審閱，但他們可能對整體方法、功能或面向使用者的介面
感到滿意。

Acked-by：不一定表示對整個補丁的確認。例如，如果一個補丁影響多個子系統，並
且有一個來自某個子系統維護者的Acked-By:，那麼這通常表示只確認影響維護者程
式碼的部分。這裡應該仔細判斷。如有疑問，應參考郵件列表存檔中的原始討論。在
這種情況下也可以使用“# 字尾”來澄清。

如果某人本應有機會對補丁進行評論，但沒有提供此類評論，您可以選擇在補丁中添加
``Cc:`` 標籤。此標籤記錄了討論中包含的潛在利益相關方。注意，這是僅有的三個
可以在未經被指名者明確許可的情況下使用的標籤之一（詳見下面的“標記他人需要
許可”）。

Co-developed-by: 聲明補丁是由多個開發人員共同建立的；當幾個人在一個補丁上工
作時，它用於給出共同作者（除了From:所給出的作者之外）。因為Co-developed-by:
表示作者身份，所以每個 Co-developed-by: 後面必須緊跟著相關共同作者的
Signed-off-by:。標準
簽署程式要求Signed-off-by:標籤的順序應儘可能反映補丁的時間歷史，無論作者是通
過From:還是Co-developed-by:表明。值得注意的是，最後一個Signed-off-by:必須是
提交補丁的開發人員。

注意，如果From:作者也是電子郵件標題的From:行中列出的人，則From:標籤是可選的。

被From:作者提交的補丁範例::

	<changelog>

	Co-developed-by: First Co-Author <first@coauthor.example.org>
	Signed-off-by: First Co-Author <first@coauthor.example.org>
	Co-developed-by: Second Co-Author <second@coauthor.example.org>
	Signed-off-by: Second Co-Author <second@coauthor.example.org>
	Signed-off-by: From Author <from@author.example.org>

被合作開發者提交的補丁範例::

	From: From Author <from@author.example.org>

	<changelog>

	Co-developed-by: Random Co-Author <random@coauthor.example.org>
	Signed-off-by: Random Co-Author <random@coauthor.example.org>
	Signed-off-by: From Author <from@author.example.org>
	Co-developed-by: Submitting Co-Author <sub@coauthor.example.org>
	Signed-off-by: Submitting Co-Author <sub@coauthor.example.org>


使用Reported-by:、Tested-by:、Reviewed-by:、Suggested-by:和Fixes:
-----------------------------------------------------------------

Reported-by 標籤給那些發現錯誤並報告錯誤的人致謝，並希望激勵他們在將來再次
幫助我們。此標籤是為錯誤設計的；請不要將其用於感謝功能請求。除非該報告無法在
網上查閱，否則此標籤後面應接著一個指向該報告的 Closes: 標籤。如果修補程式只
修復了所報告問題的一部分，可以用 Link: 標籤取代 Closes:。注意，Reported-by
標籤是僅有的三個可以在未經被指名者明確許可的情況下使用的標籤之一（詳見下面的
「標記他人需要許可」）。

Tested-by: 標籤表示補丁已由指定的人（在某些環境中）成功測試。這個標籤通知
維護人員已經執行了一些測試，為將來的補丁提供了一種定位測試人員的方法，並彰
顯測試人員的功勞。

而 Reviewed-by: 則表示，根據 Reviewer's Statement，該修補程式已被審閱並被
認為是可接受的::

	Reviewer's statement of oversight

	By offering my Reviewed-by: tag, I state that:

	 (a) I have carried out a technical review of this patch to
	     evaluate its appropriateness and readiness for inclusion into
	     the mainline kernel.

	 (b) Any problems, concerns, or questions relating to the patch
	     have been communicated back to the submitter.  I am satisfied
	     with the submitter's response to my comments.

	 (c) While there may be things that could be improved with this
	     submission, I believe that it is, at this time, (1) a
	     worthwhile modification to the kernel, and (2) free of known
	     issues which would argue against its inclusion.

	 (d) While I have reviewed the patch and believe it to be sound, I
	     do not (unless explicitly stated elsewhere) make any
	     warranties or guarantees that it will achieve its stated
	     purpose or function properly in any given situation.

以下中文譯文僅供參考，以上方英文原文為準::

	審閱者的監督聲明

	透過提供我的 Reviewed-by: 標籤，我聲明：

	 (a) 我已經對這個修補程式進行了一次技術審閱，以評估它是否適合
	     被包含到主線核心中，以及是否已準備就緒。

	 (b) 與修補程式相關的任何問題、顧慮或疑問都已回饋給提交者。我對
	     提交者對我的評論的回應感到滿意。

	 (c) 雖然這一提交可能仍有可改進之處，但我相信，此時，（1）它是
	     對核心有價值的修改，（2）沒有會反對將其納入的已知問題。

	 (d) 雖然我已經審閱了修補程式並認為它是健全的，但我不會（除非另
	     有明確說明）作出任何保證或擔保它會在任何給定情況下達成其所
	     述目的或正常運作。

Reviewed-by是一種觀點聲明，即補丁是對核心的適當修改，沒有任何遺留的嚴重技
術問題。任何感興趣的審閱者（完成了審閱工作且具有已知身分的人）都可以為一個
補丁提供一個Reviewed-by標籤。此標籤用於向審閱者提供致謝，並通知維護者補丁
的審閱進度。當Reviewed-by:標籤由已知了解主題區域並執行徹底檢查的審閱者提供
時，通常會增加補丁進入核心的可能性。

一旦從測試人員或審閱者的“Tested-by”和“Reviewed-by”標籤出現在郵件列表中，作
者應在發送下一個版本時將其添加到適用的補丁中。但是，如果補丁在後續版本中發
生了實質性更改，這些標籤可能不再適用，因此應該刪除。通常，刪除某人的
Acked-by、Tested-by或Reviewed-by標籤時，應在補丁更改日誌中（在 ``---`` 分
隔符之後）提及並附上解釋。

Suggested-by: 表示補丁的想法是由指定的人提出的，並確保將此想法歸功於指定的
人：如果我們勤快地致謝創意提供者，他們將受到鼓舞，很有希望在未來再次幫助
我們。注意，這是僅有的三個可以在未經被指名者明確許可的情況下使用的標籤之一
（詳見下面的“標記他人需要許可”）。

Fixes: 指示補丁修復了之前提交中的一個缺陷。它可以便於確定問題的來源，這有助於
檢查錯誤修復。這個標籤還幫助穩定核心團隊確定應該接收修復的穩定核心版本。這是
指示補丁修復的錯誤的首選方法。請參閱 :ref:`tw_describe_changes` 瞭解更多資訊。

注意：附加 Fixes: 標籤並不會繞過穩定核心規則流程，也不會取代所有穩定版候選
修補程式都要抄送 stable@vger.kernel.org 的要求。有關更多資訊，請閱讀
Documentation/translations/zh_TW/process/stable-kernel-rules.rst 。

最後，雖然提供標籤是受歡迎的且通常非常受讚賞，但請注意，簽署者（即提交者和
維護者）可以自行斟酌是否採用所提供的標籤。

.. _tw_tagging_people:

標記他人需要許可
----------------

在補丁中添加上述標籤時要小心：除了Cc:、Reported-by:和Suggested-by:之外，
所有標籤都需要被指名者的明確許可。對於這三個標籤，如果根據lore存檔或提交
歷史，該人曾以該名字和電子郵件地址對Linux核心做出過貢獻，那麼隱含的許可
就足夠了——並且對於Reported-by:和Suggested-by:，報告或建議必須是公開作出
的。注意，就此而言bugzilla.kernel.org是公開場所，但其中使用的電子郵件地址
是私密的；因此不要在標籤中暴露它們，除非該人在先前的貢獻中使用過。

使用Assisted-by:
----------------

如果您在建立補丁的過程中使用了任何進階編碼工具，您需要透過添加Assisted-by
標籤來聲明這一使用。不這樣做可能會妨礙您的工作被接受。關於聲明編碼助手的
細節，請參見 Documentation/process/coding-assistants.rst 。

.. _tw_the_canonical_patch_format:

標準補丁格式
------------

本節描述如何格式化補丁本身。請注意，如果您的補丁儲存在 ``git`` 儲存庫中，則
可以使用 ``git format-patch`` 進行正確的補丁格式化。但是，這些工具無法建立
必要的文字，因此請務必閱讀下面的說明。

主題行
^^^^^^

標準的補丁標題行是::

    Subject: [PATCH 001/123] subsystem: summary phrase

標準補丁的信體包含如下部分：

  - 一個 ``from`` 行指出補丁作者。後跟空行（僅當發送補丁的人不是作者時才需
    要）。

  - 說明文字，每行最長75列，這將被複制到永久變更日誌來描述這個補丁。

  - 一個空行

  - 上述的 ``Signed-off-by:`` 行，也將出現在更改日誌中。

  - 只包含 ``---`` 的標記線。

  - 任何其他不適合放在變更日誌的註解。

  - 實際補丁（ ``diff`` 輸出）。

標題行的格式，使得對標題行按字母序排序非常的容易——很多郵件用戶端都
可以支援——因為序列號是用零填充的，所以按數字排序和按字母排序是一樣的。

郵件標題中的 ``subsystem`` （子系統）應標明這個修補程式修改的是核心的哪個區域
或子系統。

郵件標題中的 ``summary phrase`` （一句話概述）應扼要地描述該郵件所含的修補
程式。``summary phrase`` 不應該是一個檔名。對於一整個修補程式系列
（``patch series`` 指一系列有順序的多個相關修補程式），不要對每個修補程式都
使用同樣的 ``summary phrase``。

記住郵件的 ``summary phrase`` 會成為該修補程式的全域唯一標識。它會一路進入
``git`` 的改動記錄裡。之後 ``summary phrase`` 可能會被用在開發者的討論裡，用來
指代這個修補程式。人們會想用搜尋引擎搜尋 ``summary phrase`` 來閱讀關於這個
修補程式的討論。當人們在兩三個月後使用諸如 ``gitk`` 或 ``git log --oneline``
之類的工具瀏覽可能數以千計的修補程式時，它也會是人們唯一能快速看到的內容。

出於這些原因，``summary`` 必須不超過 70-75 個字元，並且必須既描述修補程式改了
什麼，也描述為什麼需要這個修補程式。既要簡潔又要具描述性很有挑戰性，但寫得好
的概述就應該做到這一點。

``summary phrase`` 的前面可以加上用中括號括起來的標記：「Subject: [PATCH
<tag>...] <summary phrase>」。這些標記不被視為概述的一部分，而是描述應該如何
處理修補程式。常見的標記可能包括版本號碼（如果修補程式為了回應評論而發送了多個
版本，即「v1, v2, v3」），或用「RFC」表示徵求意見（request for comments）。

如果一個修補程式系列中有四個修補程式，那麼各個修補程式可以這樣編號：1/4、2/4、
3/4、4/4。這可以確保開發人員瞭解修補程式應套用的順序，並確認他們已經審閱或
套用了修補程式系列中的所有修補程式。

一些標題的例子::

    Subject: [PATCH 2/5] ext2: improve scalability of bitmap searching
    Subject: [PATCH v2 01/27] x86: fix eflags tracking
    Subject: [PATCH v2] sub/sys: Condensed patch summary
    Subject: [PATCH v2 M/N] sub/sys: Condensed patch summary

From行
^^^^^^

``from`` 行必須是信體裡的最上面一行，具有如下格式：

        From: Patch Author <author@example.com>

``from`` 行指明在永久改動日誌裡，誰會被確認為作者。如果沒有 ``from`` 行，那
麼郵件頭裡的 ``From:`` 行會被用來決定改動日誌中的作者。

作者可以透過在 ``from`` 行和 ``SoB`` 行中加上組織名稱，來表明其所屬單位
或工作的贊助者，例如：

	From: Patch Author (Company) <author@example.com>

說明主體
^^^^^^^^

說明文字將會被提交到永久的原始程式碼改動日誌裡，因此應讓那些早已忘記可能促成
這個修補程式的討論細節、但具備相關能力的讀者也能理解。包括修補程式所處理的
故障症狀（核心日誌訊息、oops 訊息等），這對於可能正在搜尋提交日誌以尋找適用
修補程式的人特別有用。文字應該寫得如此詳細，以便在數週、數月甚至數年後閱讀
時，能夠為讀者提供所需的細節資訊，以掌握建立補丁的 **原因** 。

如果一個修補程式修復了一個編譯失敗，那麼可能不需要包含 *所有* 編譯失敗；
只要足夠讓搜尋該修補程式的人能夠找到它就行了。與 ``summary phrase`` 一樣，
既要簡潔又要具描述性。


.. _tw_backtraces:

提交訊息中的回溯（Backtraces）
""""""""""""""""""""""""""""""

回溯有助於記錄導致問題的呼叫鏈。然而，並非所有回溯都有幫助。例如，早期引導呼
叫鏈是獨特而明顯的。而逐字複製完整的dmesg輸出則會增加時間戳、模組列表、暫存
器和堆疊轉儲等分散注意力的資訊。

因此，最有用的回溯應該從轉儲中提取相關資訊，以更容易集中在真實問題上。下面是
一個剪裁良好的回溯範例::

  unchecked MSR access error: WRMSR to 0xd51 (tried to write 0x0000000000000064)
  at rIP: 0xffffffffae059994 (native_write_msr+0x4/0x20)
  Call Trace:
  mba_wrmsr
  update_domains
  rdtgroup_mkdir

附加註解（Commentary）
^^^^^^^^^^^^^^^^^^^^^^

``---`` 標記行對於補丁處理工具要找到哪裡是改動日誌資訊的結束，是不可缺少
的。

對於 ``---`` 標記之後的額外註解，一個好的用途就是用來寫 ``diffstat`` ，用
來顯示修改了什麼檔案和每個檔案都增加和刪除了多少行。 ``diffstat`` 對於比較
大的補丁特別有用。如果你要在 ``---`` 標記之後附上 ``diffstat``，請使用
``diffstat`` 的選項 ``-p 1 -w 70``，這樣檔名就會從核心原始程式碼樹的頂層開始
列出，不會佔用太寬的空間（很容易放進 80 列的寬度，也許還能有一些縮排）。
（ ``git`` 預設會產生合適的 diffstat。）

其餘那些只適用於當時或者與維護者相關的註解，不合適放到永久的改動日誌裡的，也
應該放這裡。較好的例子就是 ``patch changelogs`` （修補程式變更記錄），記錄了 v1
和 v2 版本修補程式之間的差異。

請將此資訊放在將變更日誌與補丁的其餘部分分隔開的 ``---`` 行 **之後** 。版本
資訊不是提交到git樹的變更日誌的一部分。只是供審閱人員使用的附加資訊。如果將
其放置在提交標記上方，則需要手動交互才能將其刪除。如果它位於分隔線以下，則在
應用補丁時會自動剝離。如果可以，建議附上指向該補丁先前版本的連結（例如
lore.kernel.org存檔連結），以幫助審閱者::

  <commit message>
  ...
  Signed-off-by: Author <author@mail>
  ---
  V2 -> V3: Removed redundant helper function
  V1 -> V2: Cleaned up coding style and addressed review comments

  v2: https://lore.kernel.org/bar
  v1: https://lore.kernel.org/foo

  path/to/file | 5+++--
  ...

在後面的參考資料中能看到正確補丁格式的更多細節。


.. _tw_explicit_in_reply_to:

明確回覆郵件頭（In-Reply-To）
-----------------------------

手動為修補程式添加 In-Reply-To: 郵件頭（例如在使用 ``git send-email`` 時）
可能會有幫助，可以將修補程式與以前的相關討論關聯起來，例如將錯誤修復連結到
包含錯誤報告的郵件。但是，對於多修補程式系列，通常最好避免使用 In-Reply-To:
連結到該系列的舊版本。這樣，
補丁的多個版本就不會成為電子郵件用戶端中無法管理的引用樹。如果連結有用，
可以使用 https://lore.kernel.org/ 重新導向器（例如，在封面電子郵件文字中）
連結到補丁系列的早期版本。

給出基礎樹資訊
--------------

當其他開發人員收到您的修補程式並開始審閱時，考慮到如今維護者樹的數量之多，他們
絕對有必要知道您的工作是基於哪個基礎提交或分支。請再次留意前面說明過的
MAINTAINERS 檔案中的 **T:** 項。

這對於自動化的持續整合（CI）流程更加重要，這些流程會嘗試執行一系列測試，以便
在維護人員開始審閱之前確定您所提交內容的品質。

如果您使用 ``git format-patch`` 產生補丁，則可以透過 ``--base`` 標誌在提交中
自動包含基礎樹資訊。使用此選項最簡單、最方便的方法是配合主題分支::

    $ git checkout -t -b my-topical-branch master
    Branch 'my-topical-branch' set up to track local branch 'master'.
    Switched to a new branch 'my-topical-branch'

    [perform your edits and commits]

    $ git format-patch --base=auto --cover-letter -o outgoing/ master
    outgoing/0000-cover-letter.patch
    outgoing/0001-First-Commit.patch
    outgoing/...

當你編輯 ``outgoing/0000-cover-letter.patch`` 時，您會注意到在它的最底部有一
行 ``base-commit:`` 尾註，它為審閱者和CI工具提供了足夠的資訊以正確執行
``git am`` 而不必擔心衝突::

    $ git checkout -b patch-review [base-commit-id]
    Switched to a new branch 'patch-review'
    $ git am patches.mbox
    Applying: First Commit
    Applying: ...

有關此選項的更多資訊，請參閱 ``man git-format-patch`` 。

.. note::

    ``--base`` 功能是在2.9.0版git中引入的。

如果您不使用git格式化補丁，仍然可以包含相同的 ``base-commit`` 尾註，以指示您
的工作所基於的樹的提交雜湊值。你應該在封面郵件或系列的第一個補丁中添加它，它應
該放在 ``---`` 行的下面或所有其他內容之後，即只在你的電子郵件簽名之前。

請確認該基礎提交位於官方的維護者樹或主線樹中，而不是某個只有你能存取的內部
樹，否則它將毫無用處。

工具
----

此流程的許多技術層面都可以使用b4自動化，其說明文件見
<https://b4.docs.kernel.org/en/latest/>。它可以幫助追蹤依賴關係、執行
checkpatch，以及格式化和發送郵件。

參考文獻
--------

Andrew Morton，“完美的補丁”（tpp）
  <https://www.ozlabs.org/~akpm/stuff/tpp.txt>

Jeff Garzik，“Linux核心補丁提交格式”
  <https://web.archive.org/web/20180829112450/http://linux.yyz.us/patch-format.html>

Greg Kroah-Hartman，“如何惹惱核心子系統維護人員”
  <http://www.kroah.com/log/linux/maintainer.html>

  <http://www.kroah.com/log/linux/maintainer-02.html>

  <http://www.kroah.com/log/linux/maintainer-03.html>

  <http://www.kroah.com/log/linux/maintainer-04.html>

  <http://www.kroah.com/log/linux/maintainer-05.html>

  <http://www.kroah.com/log/linux/maintainer-06.html>

核心 Documentation/translations/zh_TW/process/coding-style.rst

Linus Torvalds關於標準補丁格式的郵件
  <https://lore.kernel.org/r/Pine.LNX.4.58.0504071023190.28951@ppc970.osdl.org>

Andi Kleen，“提交補丁之路”
  一些幫助合入困難或有爭議的變更的策略。

  http://halobates.de/on-submitting-patches.pdf

