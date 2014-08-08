Project Organization
====================

Model Layout
------------

    This is a data-/experiment-driven model for project management and data curation. At it's heart is the concept of an experiment. For MOCVD, this would be an individual growth. An arbitrary number of samples may be associated with an experiment and will be individually tracked including if the sample is broken into pieces later. Characterization is associated on a per-sample basis and will be properly associated during a split.

Core
~~~~

    Operator
        Extends User with extra domain-specific information.

            * Full name
            * Active/inactive state
            * Contact information
    
    Project
        Top-level organizational tool. Encompasses a project as it relates to a funding source or grant.

            * Description
            * Lead user (typically the grad student leading the project) for organizational purposes. This can and will change as the project goes on.
            * Active/inactive state
            * List of investigations associated with the project. These are specific to each project.
            * List of users working on/watching the project. These are fellow researchers in the lab who have either contributed or are interested in the project. They can add/remove themselves from a project at any time. When they do an experiment associated with the project they are auto-added (optional) to the watch list.
            * List of collaborators associated with the project.
            * List of published papers drawn from work done on the project.

    Investigation
        Represents a finer-grained organizational tool. It should be used for a series of experiments that are related to each other. Experiments/samples/etc are assigned on a per-investigation basis. There can be no "uncategorized" experiments that are part of a project but not a specific investigation.

            * Description
            * Project
            * Active/inactive state


    Tables
        * operator (extends User)
        * project
        * investigation
        * collaborator
        * serial_number
        * journal


Tool (D180)
~~~~~~~~~~~

    * platter (consumable - part w/ serial number)
    * sources (consumable - gas/chemical)
    * recipe (tool - recipe)
    * reading (tool - readings)
    * schedule (tool - scheduling)

Sample
~~~~~~

    * growth (experiment - references tool)
    * growth_tags (experiment/sample - tagging)
    * sample (references growth/experiment)

Characterization
~~~~~~~~~~~~~~~~

    * characterization type (references sample)


Core Scientific Metadata Model (CSMD)
-------------------------------------

CSMD is a study-data oriented model developed at the Science & Technology Facilities Council (STFC).

Core Entities
~~~~~~~~~~~~~

    * Investigation - Fundamental unit of the study
        * Title
        * Abstract
        * Dates
        * UID
        * Facility
        * Instrument
    * Investigator - People involved in the study
        * Person
        * Institution
        * Role
    * Topic/Keyword - Controlled & uncontrolled tagging
    * Publication - Publications associated with investigation
    * Sample - Material sample under investigation
        * Sample name
        * Chemical formula
        * Special information
        * Safety information
    * Dataset - Datasets associated with the investigation (i.e. runs/analysis)
        * Raw datasets
        * Analyzed datasets
        * Datasets can contain other datasets as well as datafiles
    * Datafile - Unit of storage
        * Name
        * Version
        * Location
        * Data Format
        * Creation time
        * Modification time
        * Checksum
    * Parameter
    * Authorization