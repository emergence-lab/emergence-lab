===============
Generic Process
===============

A process is a generic term encompassing most any task that will be performed on a sample in an experimental context, which can include (but is not limited to) the following:

* Running a sample through a tool
* Running a free-form task on a sample
* Characterizing a sample
* Splitting a sample into multiple pieces

Information associated with a process falls into two categories:

#) Per-instance data
#) Per-process data

Per-instance data
=================

Per-instance data is information that will change every time the process is done, for example timestamp information. All process models include the following fields

::

    created: DateTimeField
    modified: DateTimeField
    comment: TextField
    investigations: ManyToManyField

Process models will include their own process-specific per-instance data where appropriate.

Per-process data
================

Per-process data is information that will rarely change for a given process (for example, when changes are made to the tool itself). It generally encompasses configuraion information that other apps might want to configure on a per-process basis. Some examples:

* ``color`` for sample tracking
* ``max_reservations`` for scheduling

These features need to work on a process-agnostic basis and thus need to be able to grab configuration on a per-process basis.

Another imporant piece of per-process data is associated models. A typical process will include helper models that store information like the following:

* Consumables and semi-consumables
* Recipes/routines
* *in-situ* data or data taken while the process is running such as temperatures, which might be taken multiple times during a single process

Much of this data will be functionality to track which models are associated with a process to be able to properly make a ``GenericForeignKey`` to the information. One possible problem would be how to handle multiple models in each of these categories.


Process Registry
================

The process registry is the way that models or views can do the following tasks:

* Query for a list of models that are processes, especially in the context of a ``GenericForeignKey``
* Retrieve configuration information about a process with minimal database queries, on a per-option or per-process basis
* Update or add configuration information about a process
* Retrieve a list of models associated with the process in the above categories, make it possible to have a ``GenericForeignKey`` to them.
