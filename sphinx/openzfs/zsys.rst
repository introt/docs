********************
ZSys tips and tricks
********************

Recovering files from snapshots without rolling back
====================================================

Snapshots can be accessed via ``.zfs``, a truly hidden virtual directory at the top level of each dataset. See "Having access to previous user states" [#zsys_blog_states]_ for a small how-to, applicable to ZFS in general.


ZSys troubleshooting
====================

.. _ZSys troubleshooting:

Some notes on troubleshooting ZSys/``zsysctl`` errors. This article is not a full tutorial; however, as usual, all sources have been linked and archieved for further reading.


Reverting a revert fails
........................

"ZSys" "snapshot delimiter '@' is not expected here" error does not get any hits online; hopefully this'll change that. Also known as the ZSys or zsysctl "Failed to clone snapshot. Make sure that the any problems are corrected and then make sure that the dataset exists and is bootable" error [SIC] [#SIC]_, encountered after a ZSys rollback and trying to roll back to a newer zsys state.

..code-block::

   Begin: Importing ZFS root pool 'rpool' ... Begin: Importing pool 'rpool' using defaults
   done.
   find: /dev/zvol/: No such file or directory
   find: /dev/zvol/: No such file or directory
   Begin: Cloning 'rpool/ROOT/ubuntu_123456@2022-12-17-before-rollback' to 'rpool/ROOT/ubuntu_abcdef@2022-12-17-before-rollback' ... Failure: 1

   Command: /sbin/zfs clone -o canmount=noauto -o com.ubuntu.zsys:bootfs=yes rpool/ROOT/ubuntu_123456@2022-12-17-before-rollback rpool/ROOT/ubuntu_abcdef@2022-12-17-before-rollback
   Message: cannot create 'rpool/ROOT/ubuntu_abcdef@2022-12-17-before-roliback': snapshot delimiter '@' is not expected here
   Error: 1

   Failed to clone snapshot.
   Make sure that the any problems are corrected and then make sure
   that the dataset 'rpool/ROOT/ubuntu_abcdef@2022-12-17-before-rollback' exists and is bootable.

This issue seems to be caused by creating zfs snapshots manually (in this case, `rpool@2022-12-17-before-rollback`) in addition to ZSys/zsysctl states. In my case, the state I was aiming to roll back to (after rolling back to an earlier version) was named `before-rollback`, which might've been the culprit. Deleting the offending snapshot with `zfs destroy -r rpool@2022-12-17-before-rollback` fixed the issue, and I was able to "roll forward" successfully. If you've arrived at this error via other means, at least you may rest assured that rolling back is nondestructive [#zsys_blog_states]_.


Sources & further reading
=========================

.. [#zsys_blog_states] `"ZFS focus on Ubuntu 20.04 LTS: ZSys general principle on state management" <https://didrocks.fr/2020/05/28/zfs-focus-on-ubuntu-20.04-lts-zsys-general-principle-on-state-management/>`_

.. [#SIC] https://github.com/openzfs/zfs/issues/14298
