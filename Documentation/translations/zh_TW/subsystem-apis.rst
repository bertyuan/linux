.. SPDX-License-Identifier: GPL-2.0

.. include:: ./disclaimer-zh_TW.rst
.. include:: ./unmaintained-zh_TW.rst

:Original: Documentation/subsystem-apis.rst

==============
核心子系統文件
==============

這些書從核心開發者的角度，深入介紹特定核心子系統如何運作。這裡的大部分
資訊直接取自核心原始碼，並視需要加上補充材料（或者至少是我們設法加上的
部分——很可能 *並非* 所有需要的材料都已具備）。

基礎子系統
----------

TODOList:

* core-api/index
* driver-api/index
* mm/index
* power/index
* scheduler/index
* timers/index
* locking/index

人機介面
--------

TODOList:

* input/index
* hid/index
* sound/index
* gpu/index
* fb/index
* leds/index

網路介面
--------

TODOList:

* networking/index
* netlabel/index
* infiniband/index
* mhi/index

儲存介面
--------

.. toctree::
   :maxdepth: 1

   filesystems/index

TODOList:

* block/index
* cdrom/index
* scsi/index
* target/index
* nvme/index

其他子系統
----------

**Fixme**：這裡還需要更多的分類整理工作。

.. toctree::
   :maxdepth: 1

   cpu-freq/index

TODOList:

* accounting/index
* edac/index
* fpga/index
* i2c/index
* iio/index
* pcmcia/index
* spi/index
* w1/index
* watchdog/index
* virt/index
* hwmon/index
* accel/index
* security/index
* crypto/index
* bpf/index
* usb/index
* PCI/index
* misc-devices/index
* peci/index
* wmi/index
* tee/index
