from brian2 import second, check_units, BrianObject
from brian2.core.network import Network
from brian2.core.base import MagicError, brian_objects

__all__ = ['MagicNetwork', 'magic_network',
           'run', 'reinit', 'stop',
           ]


class MagicNetwork(Network):
    '''
    `Network` that automatically adds all Brian objects
    
    Notes
    -----
    
    All Brian objects that have not been removed by the `clear` function will
    be included.
    
    TODO: notes on validation/invalidation
    
    See Also
    --------
    
    Network, run, reinit, stop, clear
    '''
    def __init__(self):
        super(MagicNetwork, self).__init__()
        
    def add(self, *objs):
        raise MagicError("Cannot directly modify MagicNetwork")

    def remove(self, *objs):
        raise MagicError("Cannot directly modify MagicNetwork")
    
    def _update_magic_objects(self):
        # TODO: check validity and update objects
        if brian_objects.state==brian_objects.STATE_NEW:
            self.t = 0*second
        self.objects[:] = list(brian_objects)
        self._prepared = False
    
    @check_units(duration=second, report_period=second)
    def run(self, duration, report=None, report_period=60*second):
        '''
        run(duration, report=None, report_period=60*second)
        
        Runs the simulation for the given duration.
        
        Notes
        -----
        
        For details see `Network.run`.
        '''
        self._update_magic_objects()
        super(MagicNetwork, self).run(duration, report=report,
                                      report_period=report_period)

    def reinit(self):
        '''
        See `Network.reinit`.
        '''
        self._update_magic_objects()
        super(MagicNetwork, self).reinit()


#: Automatically constructed `MagicNetwork` of all Brian objects
magic_network = MagicNetwork()


@check_units(duration=second, report_period=second)
def run(duration, report=None, report_period=60*second):
    '''
    run(duration, report=None, report_period=60*second)
    
    Runs a simulation with all Brian objects for the given duration.
    
    Parameters
    ----------
    
    duration : `Quantity`
        The amount of simulation time to run for.
    report : {None, 'stdout', 'stderr', 'graphical', function}, optional
        How to report the progress of the simulation. If None, do not
        report progress. If stdout or stderr is specified, print the
        progress to stdout or stderr. If graphical, Tkinter is used to
        show a graphical progress bar. Alternatively, you can specify
        a callback ``function(elapsed, complete)`` which will be passed
        the amount of time elapsed (in seconds) and the fraction complete
        from 0 to 1.
    report_period : `Quantity`
        How frequently (in real time) to report progress.
        
    Notes
    -----
    
    The simulation `Network` will include all defined Brian objects that have
    not been removed by the `clear` function. The start time of the simulation
    will be the minimum time of all the clocks of the objects found. This means
    that in certain unusual circumstances several calls to `run` can lead to
    unexpected time values. For
    example, if two clocks are present with dt=3*ms and dt=5*ms then a call to
    ``run(4*ms)`` followed by ``run(4*ms)`` will run for the time interval
    ``[0*ms, 4*ms)`` for the first call, and then ``[5*ms, 9*ms]``. This is
    because at the end of the first run the first clock time will be set to
    ``6*ms`` and the second to ``5*ms``, so the start time will be taken to be
    ``5*ms``. To fix this problem, either run for durations which are divisible
    by the smallest `~Clock.dt`, or use explicitly `MagicNetwork` or `Network`
    which remember times between runs. 

    The simulation can be stopped by calling the global :func:`stop` function.
    
    See Also
    --------
    
    Network.run, MagicNetwork, reinit, stop, clear
    '''
    #net = MagicNetwork()
    #net.run(duration, report=report, report_period=report_period)
    magic_network.run(duration, report=report, report_period=report_period)


def reinit():
    '''
    Reinitialises all Brian objects.
    
    See Also
    --------
    
    Network.reinit, MagicNetwork, run, stop, clear
    '''
    #net = MagicNetwork()
    #net.reinit()
    magic_network.reinit()


def stop():
    '''
    Stops all running simulations.
    
    See Also
    --------
    
    Network.stop, MagicNetwork, run, reinit
    '''
    Network._globally_stopped = True