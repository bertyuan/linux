.. SPDX-License-Identifier: GPL-2.0

.. highlight:: none

.. include:: ../../disclaimer-zh_TW.rst

:Original: Documentation/process/debugging/gdb-kernel-debugging.rst

透過gdb對核心與模組除錯
=======================

核心除錯器kgdb、QEMU等hypervisor，或基於JTAG的硬體介面，都能在執行期間使用
gdb對Linux核心及其模組除錯。Gdb提供了強大的python腳本介面，核心也提供了一組
輔助腳本，可以簡化典型的核心除錯步驟。本文是一份簡短的教學，說明如何啟用與
使用這些腳本。本文以QEMU/KVM虛擬機器作為目標，但其中的範例也同樣適用於其他
gdb stub。


需求
----

- gdb 7.2+（建議：7.4+），並啟用python支援（各發行版通常都已啟用）


設定
----

- 為QEMU/KVM建立一台Linux虛擬機器（詳情請參考www.linux-kvm.org與
  www.qemu.org）。若要進行交叉開發，https://landley.net/aboriginal/bin 提供了
  一批機器映像檔與工具鏈，可以作為起點。

- 建置核心時啟用CONFIG_GDB_SCRIPTS，但保持CONFIG_DEBUG_INFO_REDUCED關閉。
  如果你的架構支援CONFIG_FRAME_POINTER，請保持啟用。

- 在guest上安裝該核心，必要時在核心命令列加上“nokaslr”以關閉KASLR。
  另外，QEMU也可以透過-kernel、-append、-initrd這些命令列選項直接啟動核心。
  這通常只在你不依賴模組時才有用。關於此模式的詳細資訊，請參閱QEMU文件。
  在這種情況下，如果架構支援KASLR，應該在停用CONFIG_RANDOMIZE_BASE的情況下
  建置核心。

- 建置gdb腳本（v5.1以上的核心需要此步驟）::

    make scripts_gdb

- 啟用QEMU/KVM的gdb stub，可以

    - 在VM啟動時，於QEMU命令列加上“-s”

  或

    - 在執行期間，從QEMU monitor主控台下達“gdbserver”

- cd /path/to/linux-build

- 啟動gdb：gdb vmlinux

  注意：某些發行版可能會將gdb腳本的自動載入限制在已知安全的目錄。
  如果gdb回報拒絕載入vmlinux-gdb.py，請將::

    add-auto-load-safe-path /path/to/linux-build

  加入~/.gdbinit。詳情請參閱gdb的說明。

- 連線到已開機的guest::

    (gdb) target remote :1234


使用Linux提供的gdb輔助工具的範例
--------------------------------

- 載入模組（以及主核心）的符號::

    (gdb) lx-symbols
    loading vmlinux
    scanning for modules in /home/user/linux/build
    loading @0xffffffffa0020000: /home/user/linux/build/net/netfilter/xt_tcpudp.ko
    loading @0xffffffffa0016000: /home/user/linux/build/net/netfilter/xt_pkttype.ko
    loading @0xffffffffa0002000: /home/user/linux/build/net/netfilter/xt_limit.ko
    loading @0xffffffffa00ca000: /home/user/linux/build/net/packet/af_packet.ko
    loading @0xffffffffa003c000: /home/user/linux/build/fs/fuse/fuse.ko
    ...
    loading @0xffffffffa0000000: /home/user/linux/build/drivers/ata/ata_generic.ko

- 對某個尚未載入的模組函式設定中斷點，例如::

    (gdb) b btrfs_init_sysfs
    Function "btrfs_init_sysfs" not defined.
    Make breakpoint pending on future shared library load? (y or [n]) y
    Breakpoint 1 (btrfs_init_sysfs) pending.

- 讓目標繼續執行::

    (gdb) c

- 在目標上載入模組，觀察符號的載入以及中斷點的觸發::

    loading @0xffffffffa0034000: /home/user/linux/build/lib/libcrc32c.ko
    loading @0xffffffffa0050000: /home/user/linux/build/lib/lzo/lzo_compress.ko
    loading @0xffffffffa006e000: /home/user/linux/build/lib/zlib_deflate/zlib_deflate.ko
    loading @0xffffffffa01b1000: /home/user/linux/build/fs/btrfs/btrfs.ko

    Breakpoint 1, btrfs_init_sysfs () at /home/user/linux/fs/btrfs/sysfs.c:36
    36              btrfs_kset = kset_create_and_add("btrfs", NULL, fs_kobj);

- 傾印目標核心的日誌緩衝區::

    (gdb) lx-dmesg
    [     0.000000] Initializing cgroup subsys cpuset
    [     0.000000] Initializing cgroup subsys cpu
    [     0.000000] Linux version 3.8.0-rc4-dbg+ (...
    [     0.000000] Command line: root=/dev/sda2 resume=/dev/sda1 vga=0x314
    [     0.000000] e820: BIOS-provided physical RAM map:
    [     0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
    [     0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
    ....

- 檢視目前task struct的欄位（僅支援x86與arm64）::

    (gdb) p $lx_current().pid
    $1 = 4998
    (gdb) p $lx_current().comm
    $2 = "modprobe\000\000\000\000\000\000\000"

- 針對目前或指定的CPU使用per-cpu函式::

    (gdb) p $lx_per_cpu(runqueues).nr_running
    $3 = 1
    (gdb) p $lx_per_cpu(runqueues, 2).nr_running
    $4 = 0

- 使用container_of輔助函式深入檢視hrtimers::

    (gdb) set $leftmost = $lx_per_cpu(hrtimer_bases).clock_base[0].active.rb_root.rb_leftmost
    (gdb) p *$container_of($leftmost, "struct hrtimer", "node")
    $5 = {
      node = {
        node = {
          __rb_parent_color = 18446612686384860673,
          rb_right = 0xffff888231da8b00,
          rb_left = 0x0
        },
        expires = 1228461000000
      },
      _softexpires = 1228461000000,
      function = 0xffffffff8137ab20 <tick_nohz_handler>,
      base = 0xffff888231d9b4c0,
      state = 1 '\001',
      is_rel = 0 '\000',
      is_soft = 0 '\000',
      is_hard = 1 '\001'
    }


命令與函式列表
--------------

命令與便利函式（convenience function）的數量可能會隨時間演進，以下只是初始
版本的快照::

 (gdb) apropos lx
 function lx_current -- Return current task
 function lx_module -- Find module by name and return the module variable
 function lx_per_cpu -- Return per-cpu variable
 function lx_task_by_pid -- Find Linux task by PID and return the task_struct variable
 function lx_thread_info -- Calculate Linux thread_info from task variable
 lx-dmesg -- Print Linux kernel log buffer
 lx-lsmod -- List currently loaded modules
 lx-symbols -- (Re-)load symbols of Linux kernel and currently loaded modules

命令的詳細說明可以透過“help <command-name>”取得，便利函式的詳細說明則可以
透過“help function <function-name>”取得。

除錯GDB腳本
-----------

GDB並未啟用完整的Python回溯（backtrace），這可能讓除錯GDB腳本變得比必要的
更困難。以下設定可以印出python環境的完整回溯::

 (gdb) set python print-stack full
