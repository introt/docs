Introductory material
=====================

If you're just getting starting with ZFS, I recommend reading these from start to end to gain a basic understanding of the lingo, tools, and setup choices involved. As usual: don't go in unless you know how to get out; always have backups, never store them using unfamiliar tools, and don't depend on their availability before checking their restorability.

* `"ZFS" <https://wiki.ubuntu.com/ZFS>`_ on Ubuntu wiki. A short description of the file system and its use cases.

* `"Setup a ZFS storage pool" <https://ubuntu.com/tutorials/setup-zfs-storage-pool>`_ on Ubuntu tutorials. A practical introduction to ``zpool`` and pool creation.

* `ZFS mini primer <https://wiki.ubuntu.com/Kernel/Reference/ZFS>`_ by the Ubuntu kernel team. Explains key features along with some command examples.

* `"Getting Started", OpenZFS documentation <https://openzfs.github.io/openzfs-docs/Getting%20Started/index.html>`_. Covers installation on multiple distributions, as well as `their` installation `on` ZFS [#pun]_. There's also a `FAQ <https://openzfs.github.io/openzfs-docs/Project%20and%20Community/FAQ.html>`_, and a link to `Aaron Toponce's documentation <https://pthree.org/2012/04/17/install-zfs-on-debian-gnulinux/>`_ which predates newer OpenZFS features like native encryption, but still holds up well as introductory material.

-----

.. [#pun] There's an old Finnish saying which could be translated as "eating feeds hunger". After experiencing the magic of zero-trust whole filesystem backups of your data over the (sneaker)net, you'll likely start wishing for all your backups to be as fluid and easy. They can be - you can even install your OS on ZFS! I can personally root for `the Ubuntu 20.04 installation instructions <https://openzfs.github.io/openzfs-docs/Getting%20Started/Ubuntu/Ubuntu%2020.04%20Root%20on%20ZFS.html>`_; haven't tried the newer one yet.
