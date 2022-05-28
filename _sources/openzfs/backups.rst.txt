*************************************************
Encrypted ZFS backup creation and troubleshooting
*************************************************

.. _ZFS backups:

Some notes on using ``zfs send/recv`` to take incremental backups of **encrypted** datasets. This article is not a full tutorial and does not cover eg. ``zpool`` creation or encryption key handling; however, as usual, command arguments will be explained and all sources linked and archieved for further reading.

.. Note::

   If you don't use encryption, or need a refresher on ZFS send/receive functionality, Olaf Lessenich has you covered [#xai]_.

For brevity, the following assumptions are made

#. The source pool ``$src`` has an encryption "pseudo-root" [#pseudoroot]_, ``$src/root``, and neither pool itself is encypted.

#. You want to back up ``$src/root`` to ``$dst/root``.

#. Both pools are local - though transferring over the wire is just a matter of piping through SSH. You may also use sneakernet by using shell redirection to and from a file on a removable storage medium, but do note that such streams can not be considered as backups due to their volatile nature: a single bit flip is enough to prevent their decryption [#cite]_.

#. The pool names don't contain spaces or characters that would need escaping.

#. The target pool ``$dst`` is not mounted, has not been mounted, and will not be mounted between backups. See :ref:`Troubleshooting` for more information.

#. You have working backups of all your data and will not hold me accountable in the event of data loss or worse. You've been warned.

If your setup fits the assumptions, You (future me) can copy & paste these commands straight into your root terminal (preferably from the `raw reST source <https://introt.github.io/docs/_sources/openzfs/backups.rst.txt>`_ to avoid pastejacking) for further, minimal editing, after sourcing the following variables:

.. code-block:: shell

   export src=source_pool_name
   export dst=destination_pool_name
   alias import-backup-pool='zpool import -d /search/path/if/required $dst'

You may use your favorite text editor to replace ``/root`` with a preferably unique [#unique]_ name.

.. todo:: Replace snapshot names with scriptable variables (timestamps)


Initial send/recv
=================

.. code-block:: shell

   import-backup-pool  # alias
   zfs snap -r $src@initial  # -r for recursive
   zfs send -Rw $src/root@initial | zfs recv -s $dst/root
   # zpool export $dst
   
.. Note::

        ``$dst/root`` is not a typo.
        
        * Neither ``-d`` or ``-e`` is needed here, because we're transferring ``$src/root``, not ``$src``.

        * The trailing ``/root`` is required, or else we'd overwrite the true ``$dst`` root dataset.

* On the sending side:

  * ``-R`` replicate the whole filesystem (up until the snapshot)

  * ``-w`` raw, **required with encrypted datasets**

* On the receiving side:

  * ``-s`` saves partial stream in case of error

    * I usually omit this from small (initial) transfers as retries will otherwise require some cleanup.

* On both sides, you may append:

  * ``-v`` for verbosity


Transferring subdatasets created after the initial send/recv
............................................................

New subdatasets created between snapshots are included in the incremental transfers of the pseudo-root [#full_stream]_, but if you for any reason want to transfer a single subdataset, read on.

.. warning::

        This is a bit of a footgun; since "``zfs receive -F cannot be used to destroy an encrypted filesystem``", you'll have to clean up after yourself manually. It *shouldn't* be a big deal, but since it's "left as an exercise for the reader", I'll have to advice against it.

        You've been warned.

.. code-block:: shell

   import-backup-pool
   zfs snap -r $src@sub-initial
   zfs send -Rw $src/root/new@sub-initial | zfs recv -sue $dst/root

If you've created a whole hierarchy of new datasets, you must start from the topmost new one.

* ``-u``: the target is not mounted

* ``-e`` is used here to strip ``root`` from the dataset path; if it was deeper, you'd need to write those steps on the receiving side too.
  
  * I prefer this approach over using ``-d`` (which removes just the ``$src`` (root dataset) name), as it allows receiving into ``$dst/root`` instead of directly to ``$dst``, givin at least some false sense of more control.


Subsequent, incremental transfers
=================================

.. code-block:: shell

   import-backup-pool
   zfs snap -r $src@incremental
   zfs send -Rwi @initial $src/root@incremental | zfs recv -u $dst/root
   # zpool export $dst

* ``-I`` for incremental transfer, including the intermittent snapshots [#xai]_
  
  * use ``-i`` to exclude snapshots taken between ``@initial`` and ``@incremental``

* ``-u``: the target is not mounted

Note that we're again not using either ``-d`` or ``-e``, as we're just transferring snapshots from the pseudoroot to its replicate.


Troubleshooting
===============

This is not an exhaustive list; merely some of the ones I've run into in the wild and whilst writing this article.


Dry runs with ``-n``
....................

* As ``zfs send`` dry runs create no stream, they can not be chained with ``zfs recv``.

* Can not be used on the initial receive: you'll get an error of a missing dataset:
  
        ``cannot open 'destination/root': dataset does not exist``
        ``cannot receive new filesystem stream: unable to restore to destination``


``cannot receive: failed to read from stream``
..............................................

Did you forget to remove ``-n`` from the sending side? Been there. If that doesn't help, add a ``-v`` instead and double check your pipeline.


``cannot receive incremental stream: destination $dst/root has been modified``
..............................................................................

Most tutorials add ``-F`` to the receiving side to prevent this error from popping up by forcing a rollback to the ``fromsnap`` (leftmost snapshot in the send command), but when ``zfs diff`` doesn't show what has changed, my curiosity is not satisfied. Security wise, since we're talking about Zero Trust stuff, wouldn't you like to know if your backup has been touched?

Turns out mounting the backup can "soil" your snapshot and prevent the whole dataset from receiving a stream. Ask me how I know.

To find out whether your snapshot has been soiled, run ``zfs list -po written,written@$LATEST_SNAPSHOT $dst/root`` - non-zero values mean you'll need to roll back with ``zfs rollback -r $dst/root@$LATEST_SNAPSHOT`` [#jiml]_.


``cannot open '$dst/root/sub': dataset does not exist``
.......................................................

Read on.


``cannot receive incremental stream: destination '$dst/root' does not exist``
.............................................................................

If the destination path is as expected and this isn't a dry run, you're missing the initial transfer.


``cannot receive incremental stream: most recent snapshot of $dst/root does not match incremental source``
..........................................................................................................

Check your incremental send's start and end snapshots. The start snapshot *must* exist in the destination, and can not be a bookmark. If you've deleted all common snapshots, tough luck - you'll have to make a new complete transfer.

        *"The "solution" is simply to not delete source snapshots unless those snapshots have been verified to have transmitted successfully (i.e. show up in the remote's zfs list -tall output)."* [#thewabbit]_

``zfs list -tall`` (or ``-t all``) shouldn't be followed by a pool name.


``local fs $dst/root/new does not have fromsnap (initial in stream); must have been deleted locally; ignoring``
...............................................................................................................

If you're not getting a blocking error and the dataset shows up on the destination, this is fine [#full_stream]_. Dry runs should print ``would receive full stream``, as it's just the "incrementality" that's being ignored when doing recursive transfers.

If you are sending/receiving non-recursively, see :ref:`Transferring subdatasets created after the initial send/recv`.


``cannot perform raw receive on top of existing unencrypted dataset``
.....................................................................

Make sure you are receiving the stream into ``$dst/root``, not ``$dst`` directly.

Sources & further reading
=========================

Personally, I'm going to read `"ZFS bookmarks and what they're good for" <https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSBookmarksWhatFor>`_ (as well as the relevant manual pages) and give bookmarks some thought. From skimming, it seems they are like snapshots without the reference, saving space at the sending end by only keeping a timestamp.

.. [#xai] `"Incremental backups with zfs send/recv" <https://xai.sh/2018/08/27/zfs-incremental-backups.html>`_

.. [#pseudoroot] The real root dataset shares its name with the pool, and has some extra protections which can make maintenance harder; a "pseudo-root" is a subdataset, one level down from the real root, that one puts all their other datasets under. You can read more about the practise as well as maintenance of natively-encrypted datasets from these TrueNAS forum threads:

        * `"Difficulty replicating native ZFS encrypted pool to new pool." <https://web.archive.org/web/20220404154555/https://www.truenas.com/community/threads/difficulty-replicating-native-zfs-encrypted-pool-to-new-pool.89816/>`_

        * "Confused by native ZFS encryption, some observations, many questions" (`1 <https://web.archive.org/web/20211123095242/https://www.truenas.com/community/threads/confused-by-native-zfs-encryption-some-observations-many-questions.89081/#post-617134>`_, `2 <https://web.archive.org/web/20220417170801/https://www.truenas.com/community/threads/confused-by-native-zfs-encryption-some-observations-many-questions.89081/#post-620035>`_) (linked to by the above)

.. [#cite] `"Just trust me on this one" <https://xkcd.com/285/>`_.

.. [#unique] Pseudo-roots should have unique names in case you ever need to store multiple ones in a single pool. Don't worry though, you can always ``zfs rename $src/root $src/unique_root42`` at any time - just remember to also rename any backups as well!

.. [#jiml] `Jim L.'s answer <https://unix.stackexchange.com/a/531248>`_ to "How can *efficiently* be determined whether a ZFS dataset has been changed since the last snapshot as a simple yes/no-question?"[sic] on Unix & Linux StackExchange

.. [#thewabbit] `the-wabbit's answer <https://serverfault.com/a/723104>`_ to "ZFS snapshot send incremental" on serverfault

.. [#full_stream] `Dusan's answer <https://www.truenas.com/community/threads/zfs-incremental-send-on-recursive-snapshot.16712/>`_ to "ZFS incremental send on recursive snapshot" on TrueNAS forums.
