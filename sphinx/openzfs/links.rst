Recommended links
=================

Introductory material
.....................

If you're just getting starting with ZFS, I recommend reading these from start to end to gain a basic understanding of the lingo, tools, and setup choices involved. As usual: don't go in unless you know how to get out; always have backups, never store them using unfamiliar tools, and don't depend on their availability before checking their restorability.

* `"ZFS" <https://wiki.ubuntu.com/ZFS>`_ on Ubuntu wiki. A short description of the file system and its use cases.

* `"Setup a ZFS storage pool" <https://ubuntu.com/tutorials/setup-zfs-storage-pool>`_ on Ubuntu tutorials. A practical introduction to ``zpool`` and pool creation.

* `ZFS mini primer <https://wiki.ubuntu.com/Kernel/Reference/ZFS>`_ by the Ubuntu kernel team. Explains key features along with some command examples.

* `"Getting Started", OpenZFS documentation <https://openzfs.github.io/openzfs-docs/Getting%20Started/index.html>`_. Covers installation on multiple distributions, as well as `their` installation `on` ZFS [#pun]_. There's also a `FAQ <https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ.html>`_, and a link to `Aaron Toponce's documentation <https://pthree.org/2012/04/17/install-zfs-on-debian-gnulinux/>`_ which predates newer OpenZFS features like native encryption, but still holds up well as introductory material.

Tutorials
.........

* `"Incremental backups with zfs send/recv" <https://xai.sh/2018/08/27/zfs-incremental-backups.html>`_. Short and sweet - the whole site sits really well with me. Doesn't cover encryption though, so I've put up some notes :ref:`here <ZFS backups>`.

* `"Testing the self-healing of ZFS on Ubuntu 20.04" <https://ubuntu.com/tutorials/testing-the-self-healing-of-zfs-on-ubuntu#3-create-and-test-a-zfs-pool-with-a-striped-vdev>`_ on Ubuntu tutorials. Steps 3 & 4 include commands to create "fake disks" for testing purposes (spoilers: just ``dd`` a gig from ``/dev/zero``).

* Restoring individual files from snapshots without rolling back. The answer lies in the ``.zfs/snapshot`` directory, located at the top level of each dataset. It's a really hidden virtual directory via which you have read-only access to that dataset's snapshots. You'll need to navigate to it manually. See `"Having access to previous user states" <https://didrocks.fr/2020/05/28/zfs-focus-on-ubuntu-20.04-lts-zsys-general-principle-on-state-management/>`_ for a small how-to, applicable to ZFS `in general <https://www.truenas.com/community/threads/dangerous-zfs-snapshot-directories.30828/>`_. There's also `this Reddit thread <https://old.reddit.com/r/zfs/comments/gc9c54/backuprestore_of_zfs_snapshots/>`_ in which u/DeHackEd describes their non-zfs backup setup.


Command references
..................

* `"Man Pages" <https://openzfs.github.io/openzfs-docs/man/index.html>`_, OpenZFS documentation. One of those manuals you might actually want to read - or at least skim - through before diving in. Unlike some online man pages, these ones have working links, and the subcommands' pages are nicely split out, improving browsability. Here are some quick links for the usual suspects:

  * `zpool subcommands <https://openzfs.github.io/openzfs-docs/man/8/zpool.8.html#SUBCOMMANDS>`_

  * `zfs subcommads <https://openzfs.github.io/openzfs-docs/man/8/zfs.8.html#SUBCOMMANDS>`_


-----

.. [#pun] There's an old Finnish saying which could be translated as "eating feeds hunger". After experiencing the magic of :ref:`zero-trust whole filesystem backups<ZFS backups>` of your data over the (sneaker)net, you'll likely start wishing for all your backups to be as fluid and easy. They can be - you can even install your OS on ZFS! I can personally root for `the Ubuntu 20.04 installation instructions <https://openzfs.github.io/openzfs-docs/Getting%20Started/Ubuntu/Ubuntu%2020.04%20Root%20on%20ZFS.html>`_; haven't tried the newer one yet.
