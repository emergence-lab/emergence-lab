====
core
====

.. py:module:: core

models
======

------------------
Project Management
------------------

Sample and experimentation organization is done via organizational units of projects and investigations. Every experiment or process that is done is associated with one or more investigations in a semi-structured tagging system. In turn, each investigation is associated with one or more projects. A user can 'subscribe' to projects to view experiments and data associated with all investigations that are a part of that project.

These views may be filtered down to whatever level of specificity is neccessary, such as looking at information associated with only a particular investigation or associated with a specific user or process.

The motivation for this system is to allow for the flexability that a tagging system offers but having a structure to the tags that prevents the tagging system from being used consistently and effectively.

.. py:class:: Project

    Stores information on a project, which is a higher level organizational tool.

    .. py:attribute:: name
    .. py:attribute:: slug
    .. py:attribute:: description
    .. py:attribute:: created
    .. py:attribute:: modified
    .. py:attribute:: is_active
    .. py:attribute:: status_changed

Investigation
-------------

Stores information on an individual investigation related to one or more projects.

---------------------
Samples and Processes
---------------------

The basic organizational units of experimentation are samples and processes. These two build the generic organizational tools to enable multidisciplinary tracking.

The sample is a representation of the physical object(s) that are being experimented on. Examples may include pieces of solid crystal, chemical mixtures or polymers, or cell lines, among others. Anything done to a sample is represented as a process. Examples include characterization (both destructive and non-destructive) as well as experiments that alter the sample in some way, for instance crystal growth or chemical treatment to cells.

Process
-------

Base class for all processes. A process represents an experiment or anything done to a sample which results in data (numerical or visual) or alters the properties of the sample.

Sample
------

Class representing a sample, which is an organizational unit representing a single piece of material, chemical mixture, etc. on which experimentation is done, represented as processes.

SplitProcess
------------

Process representing splitting a sample into multiple parts or pieces.

ProcessNode
-----------

Model representing the nodes in a tree of various processes done to a sample.

Substrate
---------

Base class for all substrates.


views
=====

.. automodule:: core.views
    :members:
