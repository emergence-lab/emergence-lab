Sample / Process API
====================

::python
def foo():
    # typical flow
    # user recieves a substrate from a vendor and creates a sample from it
    substrate = Substrate.objects.create(serial='xxx', source='vendor')
    sample = Sample.objects.create_sample(substrate=substrate, comment='material from vendor')

    # user performs an initial process on the sample
    process = Process.objects.create_process(prefix='afm-', comment='afm on as-recieved substrate')
    sample.run_process(process)

    # user recieves data from the vendor they want to associate with the sample
    process = Process.objects.create_process(prefix='afm-',
                                             comment='vendor char',
                                             datafile='data.csv')
    node = sample.get_process_node('smpl-0001_a.afm-0001')
    sample.add_historical_before(process, sample.process_tree)