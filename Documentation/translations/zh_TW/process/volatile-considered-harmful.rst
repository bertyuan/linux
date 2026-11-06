.. SPDX-License-Identifier: GPL-2.0

.. _tw_volatile_considered_harmful:

.. include:: ../disclaimer-zh_TW.rst

:Original: :ref:`Documentation/process/volatile-considered-harmful.rst
           <volatile_considered_harmful>`

為什麼不應該使用“volatile”類型
------------------------------

C程式設計師常認為volatile表示變數可能在目前的執行緒之外被改變；因此，在核心中
使用共享資料結構時，他們有時會想用volatile。換句話說，他們常把volatile類型當成
某種簡易的原子變數，但它並不是。在核心程式碼中使用volatile幾乎從來都不正確；
本文件將說明原因。

理解volatile的關鍵在於：它的目的是抑制最佳化，而這幾乎從來不是我們真正想做的
事。在核心中，必須保護共享資料結構免受不必要的並行存取，這是一個完全不同的任
務。防範不必要並行的過程，也能以更有效率的方式避免幾乎所有與最佳化相關的問題。

和volatile一樣，核心中讓資料並行存取變得安全的原語（自旋鎖、互斥鎖、記憶體屏障
等）也是為了防止不必要的最佳化而設計的。如果正確使用了這些原語，就不需要再使用
volatile。如果仍然需要volatile，那麼程式碼中幾乎肯定在某處有bug。在正確撰寫的
核心程式碼中，volatile只會讓事情變慢。

思考一下這段典型的核心程式碼::

    spin_lock(&the_lock);
    do_something_on(&shared_data);
    do_something_else_with(&shared_data);
    spin_unlock(&the_lock);

如果所有程式碼都遵循加鎖規則，那麼在持有the_lock期間，shared_data的值不可能意
外改變。任何其他想要操作該資料的程式碼都會在這個鎖上等待。自旋鎖原語會充當記憶
體屏障——它們是刻意這樣撰寫的——這表示資料存取不會被跨越它們而最佳化。所以編譯器
可能自認為知道shared_data裡會是什麼，但由於spin_lock()呼叫充當記憶體屏障，會強
制編譯器忘掉它所知道的一切。存取這些資料時不會有最佳化的問題。

如果把shared_data宣告為volatile，加鎖仍然是必要的。但編譯器也會因此無法在臨界
區 *內* 最佳化對shared_data的存取，而此時我們明知沒有其他人能操作它。在持有鎖期
間，shared_data並不是volatile的。處理共享資料時，正確的加鎖讓volatile變得不必要
——而且可能有害。

volatile儲存類別原本是為記憶體映射的I/O暫存器而設計的。在核心中，暫存器存取同樣
應該受鎖保護，但我們也不希望編譯器“最佳化”臨界區內的暫存器存取。不過在核心中，
I/O記憶體存取一律透過存取函式完成；直接透過指標存取I/O記憶體是不被認可的做法，
而且並非在所有架構上都能運作。這些存取函式就是為了防止不必要的最佳化而撰寫的，
所以，再說一次，volatile是不必要的。

另一種可能讓人想使用volatile的情況，是處理器忙等（busy-wait）某個變數的值。執行
忙等的正確方式是::

    while (my_variable != what_i_want)
        cpu_relax();

cpu_relax()呼叫可以降低CPU功耗，或讓位給超執行緒（hyperthreaded）的另一個邏輯處
理器；它同時也剛好充當編譯器屏障，所以，再說一次，volatile是不必要的。當然，忙
等本身通常就是一種不顧他人的行為。

在核心中，仍有少數罕見的情況下使用volatile是合理的：

  - 在確實支援直接存取I/O記憶體的架構上，上述存取函式可能會使用volatile。基本
    上，每一次存取函式呼叫本身就成為一個小的臨界區，確保存取依照程式設計師預期
    的方式發生。

  - 會修改記憶體、但沒有其他可見副作用的行內組合語言程式碼，有被GCC刪除的風險。
    在asm敘述中加上volatile關鍵字可以防止這種刪除。

  - jiffies變數很特殊，每次引用它時都可能得到不同的值，但讀取它時不需要任何特殊
    的加鎖。所以jiffies可以是volatile，但強烈不贊成再新增其他這類變數。在這方
    面，jiffies被認為是一個“愚蠢的歷史遺留”問題（Linus的原話）；修正它的麻煩會
    比它的價值還大。

  - 指向一致性記憶體（coherent memory）中、可能被I/O裝置修改的資料結構的指標，有
    時可以正當地使用volatile。網路卡使用的環形緩衝區就是這類情況的一個例子，網路
    卡會改變其中的指標，以表示哪些描述符已經處理完畢。

對大多數程式碼來說，上述使用volatile的理由都不適用。因此，使用volatile很可能被
視為bug，並使程式碼受到額外的審查。想使用volatile的開發者應該退一步，想想自己真
正想達成的是什麼。

一般都歡迎移除volatile變數的補丁——只要附上能證明並行問題已經過周全考慮的理由。


參考資料
========

[1] https://lwn.net/Articles/233481/

[2] https://lwn.net/Articles/233482/

致謝
====

最初由Randy Dunlap推動並進行研究

由Jonathan Corbet撰寫

感謝Satyam Sharma、Johannes Stezenbach、Jesper Juhl、Heikki Orsila、
H. Peter Anvin、Philipp Hahn和Stefan Richter的意見讓本文件得以改進。
