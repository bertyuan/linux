.. SPDX-License-Identifier: GPL-2.0

.. include:: ../disclaimer-zh_TW.rst

:Original: Documentation/process/maintainer-pgp-guide.rst

.. _tw_pgpguide:

=======================
核心維護者 PGP 指南
=======================

:作者: Konstantin Ryabitsev <konstantin@linuxfoundation.org>

本文件的對象是 Linux 核心開發者，特別是子系統維護者。內容是 Linux 基金會
發布的、更通用的「`Protecting Code Integrity`_」指南中所討論資訊的一部分。
若想更深入了解本指南提到的某些主題，請閱讀該文件。

.. _`Protecting Code Integrity`: https://github.com/lfit/itpol/blob/master/protecting-code-integrity.md

PGP 在 Linux 核心開發中的角色
=============================

PGP 有助於確保 Linux 核心開發社群所產出程式碼的完整性，並在較小程度上，
透過 PGP 簽名的電子郵件往來，在開發者之間建立可信任的通訊管道。

Linux 核心原始碼主要以兩種形式提供：

- 分散式原始碼儲存庫（Git）
- 定期發布的快照（tarball）

Git 儲存庫和 tarball 都帶有建立正式核心版本的核心開發者的 PGP 簽名。這些
簽名提供密碼學上的保證，確保透過 kernel.org 或任何其他鏡像站提供下載的
版本，與這些開發者工作站上的版本完全相同。為此：

- Git 儲存庫的所有標籤都附有 PGP 簽名
- tarball 的所有下載檔都附有分離式（detached）PGP 簽名

.. _tw_devs_not_infra:

信任開發者，而非基礎設施
------------------------

自從 2011 年 kernel.org 核心系統遭到入侵以來，Kernel Archives 專案的主要
運作原則，就是假設基礎設施的任何部分都可能隨時遭到入侵。因此，管理員刻意
採取措施，強調信任必須永遠放在開發者身上，而絕不放在程式碼託管基礎設施
上，不論後者的安全實務做得多好。

上述指導原則正是需要本指南的原因。我們希望確保，把信任放在開發者身上，並
不只是把未來可能發生的安全事件的責任轉嫁給別人。本指南的目標是提供一套
準則，讓開發者可以用來建立安全的工作環境，並保護用來確立 Linux 核心本身
完整性的 PGP 金鑰。

.. _tw_pgp_tools:

PGP 工具
========

使用 GnuPG 2.4 或更新版本
-------------------------

你的發行版應該已經預設安裝了 GnuPG，你只需要確認你使用的是夠新的版本。
要檢查版本，請執行::

    $ gpg --version | head -n1

如果你的版本是 2.4 或以上，那就沒問題了。如果版本更舊，表示你使用的
GnuPG 版本已經不再維護，本指南中的某些指令可能無法運作。

設定 gpg-agent 選項
~~~~~~~~~~~~~~~~~~~

GnuPG agent 是一個輔助工具，每當你使用 ``gpg`` 指令時就會自動啟動，並在
背景執行，用途是快取私鑰的密碼短語。有兩個選項你應該知道，用來調整密碼
短語何時從快取中失效：

- ``default-cache-ttl`` （秒）：如果你在存活時間（time-to-live）到期前再次
  使用同一把金鑰，倒數計時會重設，重新計算一段時間。預設值為 600（10 分
  鐘）。
- ``max-cache-ttl`` （秒）：不論你在第一次輸入密碼短語後最近一次使用金鑰
  是什麼時候，只要最長存活時間的倒數計時到期，你就必須再次輸入密碼短語。
  預設值為 30 分鐘。

如果你覺得這兩個預設值太短（或太長），可以編輯 ``~/.gnupg/gpg-agent.conf``
檔案，設定你自己的值::

    # set to 30 minutes for regular ttl, and 2 hours for max ttl
    default-cache-ttl 1800
    max-cache-ttl 7200

.. note::

    現在已經不需要在 shell 工作階段開始時手動啟動 gpg-agent。你可能需要
    檢查你的 rc 檔案，移除先前為舊版 GnuPG 所做的設定，因為它們可能已經
    不再正確。

.. _tw_protect_your_key:

保護你的 PGP 金鑰
=================

本指南假設你已經有一把用於 Linux 核心開發的 PGP 金鑰。如果你還沒有，請
參閱前面提到的「`Protecting Code Integrity`_」文件，了解如何建立新的金鑰。

如果你目前的金鑰強度低於 2048 位元（RSA），你也應該建立一把新的金鑰。

了解 PGP 子金鑰
---------------

PGP 金鑰很少只由單一金鑰對組成——通常它是一組彼此獨立的子金鑰，可依其
建立時所指派的能力用於不同用途。PGP 定義了金鑰可以具備的四種能力：

- **[S]** 金鑰可用於簽名
- **[E]** 金鑰可用於加密
- **[A]** 金鑰可用於身分驗證
- **[C]** 金鑰可用於認證其他金鑰

具備 **[C]** 能力的金鑰常被稱為「主」金鑰（master key），但這個說法容易
造成誤解，因為它暗示認證金鑰可以取代同一條鏈上的任何其他子金鑰（就像實體
的「萬能鑰匙」可以打開為其他鑰匙打造的鎖）。由於事實並非如此，本指南將它
稱為「認證金鑰」（Certify key），以避免任何歧義。

務必完全理解以下幾點：

1. 所有子金鑰彼此完全獨立。如果你遺失了某把私有子金鑰，就無法從你鏈上的
   任何其他私鑰還原或重新產生它。
2. 除了認證金鑰之外，可以有多把能力相同的子金鑰（例如，你可以有 2 把有效
   的加密子金鑰、3 把有效的簽名子金鑰，但只能有一把有效的認證子金鑰）。
   所有子金鑰都完全獨立——加密給某一把 **[E]** 子金鑰的訊息，無法用你
   可能擁有的任何其他 **[E]** 子金鑰解密。
3. 單一子金鑰可以具備多種能力（例如，你的 **[C]** 金鑰也可以同時是你的
   **[S]** 金鑰）。

具備 **[C]** （認證）能力的金鑰，是唯一可以用來表示與其他金鑰之間關係的
金鑰。只有 **[C]** 金鑰可以用來：

- 新增或撤銷具備 S/E/A 能力的其他金鑰（子金鑰）
- 新增、變更或撤銷與該金鑰關聯的身分（uid）
- 新增或變更它自己或任何子金鑰的到期日
- 為了信任網的目的簽署其他人的金鑰

GnuPG 在產生新金鑰時，預設會建立以下內容：

- 一把同時具備認證與簽名能力的子金鑰（**[SC]**）
- 一把具備加密能力的獨立子金鑰（**[E]**）

如果你產生金鑰時使用的是預設參數，那麼你擁有的就是這些。你可以執行
``gpg --list-secret-keys`` 來確認，例如::

    sec   ed25519 2022-12-20 [SC] [expires: 2024-12-19]
          000000000000000000000000AAAABBBBCCCCDDDD
    uid           [ultimate] Alice Dev <adev@kernel.org>
    ssb   cv25519 2022-12-20 [E] [expires: 2024-12-19]

``sec`` 項目下方那一長串就是你的金鑰指紋——在下面的範例中，每當你看到
``[fpr]``，指的就是這個 40 個字元的字串。

確保你的密碼短語夠強
--------------------

GnuPG 會先用密碼短語加密你的私鑰，再把它們儲存到磁碟上。如此一來，即使
你的整個 ``.gnupg`` 目錄外洩或被竊，攻擊者若沒有先取得用來解密的密碼
短語，也無法使用你的私鑰。

用強度足夠的密碼短語保護你的私鑰是絕對必要的。要設定或變更密碼短語，請
使用::

    $ gpg --change-passphrase [fpr]

建立獨立的簽名子金鑰
--------------------

我們的目標是把你的認證金鑰移到離線媒體上加以保護，所以如果你只有一把合併
的 **[SC]** 金鑰，就應該另外建立一把獨立的簽名子金鑰::

    $ gpg --quick-addkey [fpr] ed25519 sign

備份你的認證金鑰以供災難復原
----------------------------

你的 PGP 金鑰上來自其他開發者的簽名越多，你就越有理由為了災難復原，建立
一份存放在數位媒體以外的備份。

要製作私鑰的可列印紙本，一個好方法是使用專為此目的撰寫的 ``paperkey``
軟體。關於其輸出格式，以及它相較於其他方案的優點，請參閱
``man paperkey``。大多數發行版應該都已經有 Paperkey 的套件。

執行以下指令，建立私鑰的紙本備份::

    $ gpg --export-secret-key [fpr] | paperkey -o /tmp/key-backup.txt

把該檔案列印出來，然後拿一支筆，把你的密碼短語寫在紙張的邊緣。**強烈建議
這麼做**，因為印出來的金鑰仍然是用該密碼短語加密的，而如果你哪天變更了
密碼短語，你將不會記得建立備份時用的是哪一個——*保證如此*。

把印好的紙本和手寫的密碼短語放進信封，存放在安全且受到妥善保護的地方，
最好不在你家裡，例如銀行的保險箱。

.. note::

    金鑰仍然是用你的密碼短語加密的，所以即使用「整合雲端」的現代印表機
    列印，也應該仍是相對安全的操作。

備份你的整個 GnuPG 目錄
-----------------------

.. warning::

    **!!!不要跳過這個步驟!!!**

當你需要復原 PGP 金鑰時，手邊有一份隨時可用的備份是很重要的。這和我們用
``paperkey`` 所做的災難等級準備不同。每當你需要使用認證金鑰時——例如變更
你自己的金鑰，或在研討會和高峰會之後簽署其他人的金鑰——你也會依賴這些
外部副本。

首先，準備一張外接儲存卡（最好是兩張！）作為備份用途。你需要用 LUKS 在
這個裝置上建立一個加密分割區——如何操作請參閱你的發行版文件。

加密用的密碼短語可以和你的 PGP 金鑰使用同一個。

加密程序完成後，重新插入你的裝置，並確認它已正確掛載。把你的整個
``.gnupg`` 目錄複製到加密儲存裝置上::

    $ cp -a ~/.gnupg /media/disk/foo/gnupg-backup

現在你應該測試一下，確認一切仍然正常運作::

    $ gpg --homedir=/media/disk/foo/gnupg-backup --list-key [fpr]

如果沒有出現任何錯誤，那就沒問題了。卸載裝置，清楚地標示它，以免不小心
覆寫，然後把它放在安全的地方——但不要放得太遠，因為你偶爾還需要用它來
做一些事，例如編輯身分、新增或撤銷子金鑰，或簽署其他人的金鑰。

從主目錄中移除認證金鑰
----------------------

我們主目錄中的檔案，並沒有我們想像中受到那麼好的保護。它們可能透過許多
不同的途徑外洩或被竊：

- 為了設定新工作站而快速複製主目錄時意外外洩
- 系統管理員的疏忽或惡意
- 保護不周的備份
- 桌面應用程式（瀏覽器、pdf 檢視器等）中的惡意軟體
- 跨越國境時遭到脅迫

用好的密碼短語保護金鑰，可以大幅降低上述任何一種風險，但密碼短語仍可能
透過鍵盤側錄程式、偷窺螢幕或其他各種方式被發現。因此，建議的做法是把
認證金鑰從主目錄中移除，存放在離線儲存裝置上。

.. warning::

    請參閱上一節，確認你已經完整備份了 GnuPG 目錄。如果你沒有可用的
    備份，我們接下來要做的事會讓你的金鑰變得無法使用！

首先，找出你的認證金鑰的「keygrip」::

    $ gpg --with-keygrip --list-key [fpr]

輸出會類似這樣::

    pub   ed25519 2022-12-20 [SC] [expires: 2022-12-19]
          000000000000000000000000AAAABBBBCCCCDDDD
          Keygrip = 1111000000000000000000000000000000000000
    uid           [ultimate] Alice Dev <adev@kernel.org>
    sub   cv25519 2022-12-20 [E] [expires: 2022-12-19]
          Keygrip = 2222000000000000000000000000000000000000
    sub   ed25519 2022-12-20 [S]
          Keygrip = 3333000000000000000000000000000000000000

找出位於 ``pub`` 那一行下方（就在認證金鑰指紋的正下方）的 keygrip 項目。
它會直接對應到你 ``~/.gnupg`` 目錄中的一個檔案::

    $ cd ~/.gnupg/private-keys-v1.d
    $ ls
    1111000000000000000000000000000000000000.key
    2222000000000000000000000000000000000000.key
    3333000000000000000000000000000000000000.key

只要移除與認證金鑰 keygrip 對應的 .key 檔案就夠了::

    $ cd ~/.gnupg/private-keys-v1.d
    $ rm 1111000000000000000000000000000000000000.key

現在如果你執行 ``--list-secret-keys`` 指令，它會顯示認證金鑰已經不在
（``#`` 表示該金鑰無法使用）::

    $ gpg --list-secret-keys
    sec#  ed25519 2022-12-20 [SC] [expires: 2024-12-19]
          000000000000000000000000AAAABBBBCCCCDDDD
    uid           [ultimate] Alice Dev <adev@kernel.org>
    ssb   cv25519 2022-12-20 [E] [expires: 2024-12-19]
    ssb   ed25519 2022-12-20 [S]

你也應該移除 ``~/.gnupg`` 目錄中所有的 ``secring.gpg`` 檔案，它們可能是
舊版 GnuPG 留下來的。

如果你沒有「private-keys-v1.d」目錄
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你沒有 ``~/.gnupg/private-keys-v1.d`` 目錄，表示你的密鑰仍然儲存在
GnuPG v1 所使用的舊式 ``secring.gpg`` 檔案中。對金鑰做任何變更，例如變更
密碼短語或新增子金鑰，應該都會自動把舊的 ``secring.gpg`` 格式轉換為使用
``private-keys-v1.d``。

完成之後，務必刪除已過時的 ``secring.gpg`` 檔案，因為它仍然含有你的
私鑰。

.. _tw_smartcards:

將子金鑰移到專用的加密裝置
==========================

雖然認證金鑰現在已經不會外洩或被竊，但子金鑰仍然在你的主目錄中。任何
設法取得這些子金鑰的人，都能夠解密你的通訊或偽造你的簽名（如果他們知道
密碼短語）。此外，每次執行 GnuPG 操作時，金鑰都會被載入系統記憶體，夠
先進的惡意軟體可以從那裡把它們偷走（想想 Meltdown 和 Spectre）。

要完整保護你的金鑰，一個好方法是把它們移到能夠執行智慧卡操作的專用硬體
裝置上。

智慧卡的好處
------------

智慧卡內含一顆加密晶片，能夠儲存私鑰，並直接在卡片上執行加密運算。由於
金鑰內容永遠不會離開智慧卡，插入該硬體裝置的電腦，其作業系統無法取得私鑰
本身。這和我們先前用於備份的加密儲存裝置大不相同——那個裝置在插入並掛載
時，作業系統是能夠存取私鑰內容的。

使用外接加密媒體並不能取代具備智慧卡功能的裝置。

可用的智慧卡裝置
----------------

除非你所有的筆記型電腦和工作站都有智慧卡讀卡機，否則最簡單的做法是取得
一個實作智慧卡功能的專用 USB 裝置。有幾種選擇：

- `Nitrokey Start`_：開放硬體與自由軟體，以 FSI Japan 的 `Gnuk`_ 為
  基礎。最便宜的選擇之一，但提供的安全功能最少（例如防竄改或抵抗某些
  旁通道攻擊）。
- `Nitrokey 3`_：與 Nitrokey Start 類似，但更能防竄改，並提供更多安全
  功能和 USB 外形規格。支援 ECC 密碼學（ED25519 和 NISTP）。
- `Yubikey 5`_：專有的硬體與軟體，但比 Nitrokey 便宜，功能也相近。支援
  ECC 密碼學（ED25519 和 NISTP）。

你的選擇將取決於成本、在你所在地區能否運送，以及對開放或專有硬體的考量。

.. note::

    如果你列在 MAINTAINERS 的 `M:` 項目中，或擁有 kernel.org 帳號，你就
    `qualify for a free Nitrokey Start`_ （有資格免費獲得 Linux 基金會
    提供的 Nitrokey Start）。

.. _`Nitrokey Start`: https://www.nitrokey.com/products/nitrokeys
.. _`Nitrokey 3`: https://www.nitrokey.com/products/nitrokeys
.. _`Yubikey 5`: https://www.yubico.com/products/yubikey-5-overview/
.. _Gnuk: https://www.fsij.org/doc-gnuk/
.. _`qualify for a free Nitrokey Start`: https://www.kernel.org/nitrokey-digital-tokens-for-kernel-developers.html

設定你的智慧卡裝置
------------------

你的智慧卡裝置一插上任何現代的 Linux 工作站，就應該能直接運作（Just Work
(TM)）。你可以執行以下指令確認::

    $ gpg --card-status

如果你看到完整的智慧卡詳細資訊，那就沒問題了。可惜的是，要排除所有可能
導致無法運作的原因，遠遠超出本指南的範圍。如果你無法讓智慧卡與 GnuPG
搭配運作，請透過一般的支援管道尋求協助。

要設定你的智慧卡，你需要使用 GnuPG 的選單系統，因為沒有方便的命令列
選項::

    $ gpg --card-edit
    [...omitted...]
    gpg/card> admin
    Admin commands are allowed
    gpg/card> passwd

你應該設定使用者 PIN（1）、管理員 PIN（3）和重設碼（4）。請務必把這些
記錄下來並存放在安全的地方——特別是管理員 PIN 和重設碼（重設碼可以讓你
完全清除智慧卡）。你很少需要用到管理員 PIN，所以如果不記錄下來，你一定會
忘記它是什麼。

回到卡片主選單後，你也可以設定其他值（例如姓名、性別、登入資料等），但這
並非必要，而且萬一你遺失了智慧卡，還會額外洩漏關於這張智慧卡的資訊。

.. note::

    雖然名稱叫做「PIN」，但卡片上的使用者 PIN 和管理員 PIN 都不一定要是
    數字。

.. warning::

    某些裝置可能要求你先把子金鑰移到裝置上，才能變更密碼短語。請查閱
    裝置製造商提供的文件。

將子金鑰移到你的智慧卡
----------------------

離開卡片選單（使用「q」）並儲存所有變更。接下來，我們把你的子金鑰移到
智慧卡上。大多數操作都會同時需要你的 PGP 金鑰密碼短語和卡片的管理員
PIN::

    $ gpg --edit-key [fpr]

    Secret subkeys are available.

    pub  ed25519/AAAABBBBCCCCDDDD
         created: 2022-12-20  expires: 2024-12-19  usage: SC
         trust: ultimate      validity: ultimate
    ssb  cv25519/1111222233334444
         created: 2022-12-20  expires: never       usage: E
    ssb  ed25519/5555666677778888
         created: 2017-12-07  expires: never       usage: S
    [ultimate] (1). Alice Dev <adev@kernel.org>

    gpg>

使用 ``--edit-key`` 會讓我們再次進入選單模式，你會注意到金鑰列表有點
不同。從這裡開始，所有指令都在這個選單模式中執行，如 ``gpg>`` 所示。

首先，選擇我們要放到卡片上的金鑰——方法是輸入 ``key 1`` （它是列表中的
第一把，也就是 **[E]** 子金鑰）::

    gpg> key 1

現在你應該會在輸出中看到 **[E]** 金鑰變成 ``ssb*``。``*`` 表示目前「被
選取」的是哪一把金鑰。它的作用是 *切換*，也就是說，如果你再輸入一次
``key 1``，``*`` 就會消失，該金鑰也就不再被選取。

現在，把那把金鑰移到智慧卡上::

    gpg> keytocard
    Please select where to store the key:
       (2) Encryption key
    Your selection? 2

由於這是我們的 **[E]** 金鑰，把它放進加密（Encryption）槽位是合理的。
送出選擇後，系統會先要求你輸入 PGP 金鑰的密碼短語，然後再要求輸入管理員
PIN。如果指令執行完畢且沒有出現錯誤，你的金鑰就已經移過去了。

**重要**：現在再輸入一次 ``key 1`` 取消選取第一把金鑰，然後輸入
``key 2`` 選取 **[S]** 金鑰::

    gpg> key 1
    gpg> key 2
    gpg> keytocard
    Please select where to store the key:
       (1) Signature key
       (3) Authentication key
    Your selection? 1

**[S]** 金鑰可以同時用於簽名（Signature）和身分驗證（Authentication），
但我們希望確保它放在簽名槽位中，所以選擇（1）。同樣地，如果指令執行完畢
且沒有出現錯誤，操作就成功了::

    gpg> q
    Save changes? (y/N) y

儲存變更後，你移到卡片上的那些金鑰會從主目錄中刪除（不過沒關係，因為我們
的備份裡還有，如果之後要為替換的智慧卡再做一次，就可以使用）。

確認金鑰已經移過去
~~~~~~~~~~~~~~~~~~

如果你現在執行 ``--list-secret-keys``，會在輸出中看到細微的差異::

    $ gpg --list-secret-keys
    sec#  ed25519 2022-12-20 [SC] [expires: 2024-12-19]
          000000000000000000000000AAAABBBBCCCCDDDD
    uid           [ultimate] Alice Dev <adev@kernel.org>
    ssb>  cv25519 2022-12-20 [E] [expires: 2024-12-19]
    ssb>  ed25519 2022-12-20 [S]

``ssb>`` 中的 ``>`` 表示該子金鑰只存在於智慧卡上。如果你回到密鑰目錄檢視
裡面的內容，會發現那裡的 ``.key`` 檔案都已經被替換成存根（stub）::

    $ cd ~/.gnupg/private-keys-v1.d
    $ strings *.key | grep 'private-key'

輸出中應該會有 ``shadowed-private-key``，表示這些檔案只是存根，實際的
內容在智慧卡上。

確認智慧卡正常運作
~~~~~~~~~~~~~~~~~~

要確認智慧卡如預期運作，你可以建立一個簽名::

    $ echo "Hello world" | gpg --clearsign > /tmp/test.asc
    $ gpg --verify /tmp/test.asc

執行第一個指令時，應該會要求你輸入智慧卡 PIN，接著在你執行
``gpg --verify`` 後顯示「Good signature」。

恭喜，你已經成功讓別人極難竊取你的數位開發者身分！

其他常見的 GnuPG 操作
---------------------

以下是一些你會需要對 PGP 金鑰執行的常見操作的快速參考。

掛載你的安全離線儲存裝置
~~~~~~~~~~~~~~~~~~~~~~~~

以下任何一項操作都需要用到認證金鑰，所以你首先需要掛載你的離線備份儲存
裝置，並告訴 GnuPG 使用它::

    $ export GNUPGHOME=/media/disk/foo/gnupg-backup
    $ gpg --list-secret-keys

你要確認輸出中顯示的是 ``sec`` 而不是 ``sec#`` （``#`` 表示該金鑰無法
使用，而你仍在使用一般的主目錄位置）。

延長金鑰的到期日
~~~~~~~~~~~~~~~~

認證金鑰的預設到期日是建立日起 2 年。這麼做既是出於安全考量，也是為了讓
過時的金鑰最終從金鑰伺服器上消失。

要把金鑰的到期日從今天起延長一年，只要執行::

    $ gpg --quick-set-expire [fpr] 1y

如果使用特定日期比較好記，你也可以這麼做（例如你的生日、1 月 1 日或
加拿大國慶日）::

    $ gpg --quick-set-expire [fpr] 2038-07-01

記得把更新後的金鑰發送回金鑰伺服器::

    $ gpg --send-key [fpr]

做了任何變更之後更新你的工作目錄
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

當你使用離線儲存裝置對金鑰做了任何變更之後，會需要把這些變更匯入回你平常
的工作目錄::

    $ gpg --export | gpg --homedir ~/.gnupg --import
    $ unset GNUPGHOME

透過 ssh 使用 gpg-agent
~~~~~~~~~~~~~~~~~~~~~~~

如果你需要在遠端系統上簽署標籤或提交，可以透過 ssh 轉送你的 gpg-agent。
請參考 GnuPG wiki 上提供的說明：

- `Agent Forwarding over SSH`_

如果你能修改遠端的 sshd 伺服器設定，運作起來會更順暢。

.. _`Agent Forwarding over SSH`: https://wiki.gnupg.org/AgentForwarding

.. _tw_pgp_with_git:

在 Git 中使用 PGP
=================

Git 的核心特色之一是它的分散式本質——一旦把儲存庫複製到你的系統上，你就
擁有該專案的完整歷史，包括它所有的標籤、提交和分支。然而，當外面流傳著
數以百計的複製儲存庫時，任何人要如何確認自己手上的 linux.git 副本沒有
被惡意第三方竄改？

又或者，如果在核心中發現了惡意程式碼，而提交中的「Author」行說是你做的，
但你很確定自己 `跟它毫無關係`_，那又會怎樣？

為了同時解決這兩個問題，Git 引入了 PGP 整合。簽名標籤可以確保儲存庫的
內容與建立該標籤的開發者工作站上的內容完全相同，藉此證明儲存庫的完整性；
而簽名提交則讓別人在無法取得你的 PGP 金鑰的情況下，幾乎不可能冒充你。

.. _`跟它毫無關係`: https://github.com/jayphelps/git-blame-someone-else

設定 Git 使用你的 PGP 金鑰
--------------------------

如果你的金鑰環中只有一把密鑰，那其實不需要做任何額外的事，因為它就會是你
的預設金鑰。不過，如果你剛好有多把密鑰，可以告訴 Git 應該使用哪一把
（``[fpr]`` 是你金鑰的指紋）::

    $ git config --global user.signingKey [fpr]

如何使用簽名標籤
----------------

要建立簽名標籤，請在 tag 指令加上 ``-s`` 選項::

    $ git tag -s [tagname]

我們建議一律簽署 Git 標籤，因為這能讓其他開發者確認他們拉取的 Git 儲存庫
沒有遭到惡意竄改。

如何驗證簽名標籤
~~~~~~~~~~~~~~~~

要驗證簽名標籤，請使用 ``verify-tag`` 指令::

    $ git verify-tag [tagname]

如果你是從專案儲存庫的另一個分叉拉取標籤，Git 應該會自動驗證你所拉取的
最新端點上的簽名，並在合併操作期間顯示結果::

    $ git pull [url] tags/sometag

合併訊息中會包含類似以下的內容::

    Merge tag 'sometag' of [url]

    [Tag message]

    # gpg: Signature made [...]
    # gpg: Good signature from [...]

如果你要驗證別人的 Git 標籤，首先需要匯入他們的 PGP 金鑰。請參閱下面的
「:ref:`tw_verify_identities`」一節。

設定 Git 一律簽署附註標籤
~~~~~~~~~~~~~~~~~~~~~~~~~

如果你要建立附註標籤（annotated tag），你很可能也會想要簽署它。要強制
Git 一律簽署附註標籤，可以設定一個全域設定選項::

    $ git config --global tag.forceSignAnnotated true

如何使用簽名提交
----------------

你也可以建立簽名提交，但它們在 Linux 核心開發中的用處有限。核心的貢獻
流程仰賴寄送修補程式，而把提交轉換成修補程式並不會保留 Git 提交簽名。
此外，把你自己的儲存庫 rebase 到較新的上游版本時，PGP 提交簽名最後也會
被捨棄。因此，大多數核心開發者並不費心簽署自己的提交，也會忽略他們工作
所依賴的任何外部儲存庫中的簽名提交。

話雖如此，如果你的工作用 Git 樹公開放在某個 Git 託管服務上（kernel.org、
infradead.org、ozlabs.org 或其他），那麼即使上游開發者無法直接從這種做法
中受益，我們仍建議你簽署所有的 Git 提交。

我們建議這麼做的理由如下：

1. 如果有一天需要進行程式碼鑑識或追查程式碼來源，即使是在外部維護、帶有
   PGP 提交簽名的樹，對這類用途也很有價值。
2. 如果你需要重新複製本地儲存庫（例如，重新安裝系統之後），這可以讓你在
   繼續工作之前驗證儲存庫的完整性。
3. 如果有人需要 cherry-pick 你的提交，這能讓他們在套用之前快速驗證這些
   提交的完整性。

建立簽名提交
~~~~~~~~~~~~

要建立簽名提交，請在 ``git commit`` 指令加上 ``-S`` 旗標（因為和另一個
旗標衝突，所以是大寫的 ``-S``）::

    $ git commit -S

設定 Git 一律簽署提交
~~~~~~~~~~~~~~~~~~~~~

你可以告訴 Git 一律簽署提交::

    git config --global commit.gpgSign true

.. note::

    在開啟這個選項之前，請務必先設定好 ``gpg-agent``。

.. _tw_verify_identities:

如何使用簽名修補程式
--------------------

你可以用 PGP 金鑰簽署發送到核心開發者郵件列表的修補程式。由於現有的電子
郵件簽名機制（PGP-Mime 或 PGP-inline）往往會對一般的程式碼審查工作造成
問題，你應該使用 kernel.org 為此目的建立的工具，它會把密碼學證明
（attestation）簽名放進郵件標頭中（類似 DKIM）：

- `Patatt Patch Attestation`_

.. _`Patatt Patch Attestation`: https://pypi.org/project/patatt/

安裝與設定 patatt
~~~~~~~~~~~~~~~~~

.. note::

    如果你使用 B4 寄送修補程式，patatt 已經安裝好並整合進你的工作流程中。

許多發行版都已經有 Patatt 的套件，所以請先到那裡找找看。你也可以用
「``pip install patatt``」從 pypi 安裝。

如果你已經在 Git 中設定好 PGP 金鑰（透過 ``user.signingKey`` 設定參數），
那麼 patatt 不需要任何額外設定。你可以在想要的儲存庫中安裝 git-send-email
掛鉤（hook），開始簽署你的修補程式::

    patatt install-hook

現在，你用 ``git send-email`` 發送的任何修補程式，都會自動加上你的密碼學
簽名。

檢查 patatt 簽名
~~~~~~~~~~~~~~~~

如果你使用 ``b4`` 取得並套用修補程式，它會自動嘗試驗證遇到的所有 DKIM 和
patatt 簽名，例如::

    $ b4 am 20220720205013.890942-1-broonie@kernel.org
    [...]
    Checking attestation on all messages, may take a moment...
    ---
      ✓ [PATCH v1 1/3] kselftest/arm64: Correct buffer allocation for SVE Z registers
      ✓ [PATCH v1 2/3] arm64/sve: Document our actual ABI for clearing registers on syscall
      ✓ [PATCH v1 3/3] kselftest/arm64: Enforce actual ABI for SVE syscalls
      ---
      ✓ Signed: openpgp/broonie@kernel.org
      ✓ Signed: DKIM/kernel.org

.. note::

    Patatt 和 b4 仍在積極開發中，你應該查閱這些專案的最新文件，了解任何
    新增或更新的功能。

.. _tw_kernel_identities:

如何驗證核心開發者的身分
========================

簽署標籤和提交很簡單，但要如何確認用來簽署某樣東西的金鑰，確實屬於那位
核心開發者，而不是屬於惡意的冒名者？

使用 WKD 和 DANE 設定自動擷取金鑰
---------------------------------

如果你還沒有大量收集其他開發者的公鑰，可以靠金鑰的自動探索與自動擷取來
快速建立你的金鑰環。如果從零開始建立你自己的信任網（Web of Trust）讓你
望而卻步，GnuPG 可以借助其他委派信任技術，也就是 DNSSEC 和 TLS，讓你
先開始使用。

把以下內容加到你的 ``~/.gnupg/gpg.conf``::

    auto-key-locate wkd,dane,local
    auto-key-retrieve

基於 DNS 的具名實體認證（DNS-Based Authentication of Named Entities，
「DANE」）是一種在 DNS 中發布公鑰，並使用 DNSSEC 簽名區域來保護它們的
方法。Web 金鑰目錄（Web Key Directory，「WKD」）則是另一種方法，使用
https 查詢來達到同樣的目的。使用 DANE 或 WKD 查詢公鑰時，GnuPG 會分別先
驗證 DNSSEC 或 TLS 憑證，才把自動擷取到的公鑰加入你的本地金鑰環。

Kernel.org 為所有擁有 kernel.org 帳號的開發者發布 WKD。在你的
``gpg.conf`` 做了上述變更之後，就可以自動擷取 Linus Torvalds 和
Greg Kroah-Hartman 的金鑰（如果你還沒有的話）::

    $ gpg --locate-keys torvalds@kernel.org gregkh@kernel.org

如果你有 kernel.org 帳號，那麼你應該 `把 kernel.org UID 加到你的金鑰`_，
讓 WKD 對其他核心開發者更有用。

.. _`把 kernel.org UID 加到你的金鑰`: https://korg.docs.kernel.org/mail.html#adding-a-kernel-org-uid-to-your-pgp-key

信任網（WOT）與首次使用信任（TOFU）
-----------------------------------

PGP 包含一種稱為「信任網」（Web of Trust）的信任委派機制。其核心是試圖
取代 HTTPS/TLS 世界中對集中式憑證授權單位（Certification Authority）的
需求。PGP 不讓各家軟體廠商來決定誰應該是你信任的認證實體，而是把這個責任
交給每一位使用者。

可惜的是，很少有人了解信任網是如何運作的。雖然它仍是 OpenPGP 規範中重要
的一部分，但較新版本的 GnuPG（2.2 及以上）已經實作了另一種稱為「首次使用
信任」（Trust on First Use，TOFU）的機制。你可以把 TOFU 想成「類似 SSH 的
信任方式」。使用 SSH 時，第一次連線到遠端系統，其金鑰指紋就會被記錄並
記住。如果之後金鑰改變了，SSH 用戶端會警告你並拒絕連線，迫使你決定是否
要信任改變後的金鑰。同樣地，第一次匯入某人的 PGP 金鑰時，它會被假定為
有效。如果之後 GnuPG 在任何時候遇到另一把身分相同的金鑰，先前匯入的金鑰
和新金鑰都會被標記為需要驗證，你必須手動判斷要保留哪一把。

我們建議你使用合併的 TOFU+PGP 信任模型（這是 GnuPG v2 新的預設值）。要
設定它，請在 ``~/.gnupg/gpg.conf`` 中新增（或修改）``trust-model``
設定::

    trust-model tofu+pgp

.. _tw_kernel_org_trust_repository:

使用 kernel.org 信任網儲存庫
----------------------------

Kernel.org 維護一個存放開發者公鑰的 Git 儲存庫，用來取代過去幾年大多已經
停擺的同步式金鑰伺服器網路。關於如何把該儲存庫設定為你的公鑰來源，完整
文件可以在這裡找到：

- `Kernel developer PGP Keyring`_

如果你是核心開發者，請考慮提交你的金鑰，讓它收錄到該金鑰環中。

.. _`Kernel developer PGP Keyring`: https://korg.docs.kernel.org/pgpkeys.html
