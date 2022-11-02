# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.

from abc import ABC, abstractmethod
from calendar import day_abbr
from dataclasses import dataclass, field
from typing import Optional, Sequence, List, Tuple

import numpy as np

from .contact_tracer import ContactTracer
from .ids import PersonID, LocationID
from .infection_model import IndividualInfectionState, Risk
from .pandemic_testing_result import PandemicTestResult
from .pandemic_types import NoOP
from .regulation import PandemicRegulation
from .sim_time import SimTime

__all__ = ['Person', 'PersonState']


@dataclass
class PersonState:
    """State of the person."""
    current_location: LocationID
    risk: Risk
    infection_state: Optional[IndividualInfectionState] = None
    infection_spread_multiplier: float = 1.

    quarantine: bool = field(init=False, default=False)
    quarantine_if_contact_positive: bool = field(init=False, default=False)
    quarantine_if_household_quarantined: bool = field(init=False, default=False)
    sick_at_home: bool = field(init=False, default=False)
    avoid_gathering_size: int = field(init=False, default=-1)

    test_result: PandemicTestResult = field(init=False, default=PandemicTestResult.UNTESTED)

    avoid_location_types: List[type] = field(default_factory=list, init=False)
    not_infection_probability: float = field(default=1., init=False)
    not_infection_probability_history: List[Tuple[LocationID, float]] = field(default_factory=list, init=False)

class TravelSchedule:

    _start_day: int
    """The day the visitor enters the sim."""
    _end_day: int
    """The day the visitor exits the sim."""
    _active: bool 
    """Whether the person is active (they are in the city)."""
    _num_visits: int

    

    def __init__(self, start: int):
        self._start_day = start
        duration = np.random.choice(np.arange(1,30))
        self._end_day = start + duration
        self._active = True
        self._num_visits = np.random.choice(np.arange(1,3))

    @property
    def start_day(self)-> int:
        return self._start_day
    
    @property
    def end_day(self)-> int:
        return self._end_day
    
    def start_trip(self)-> None:
        self._active = True
        self._num_visits -= 1
    
    def end_trip(self)-> None:
        self._active = False
        if self._num_visits > 0:
            self.start_day = self.end_day + np.random.choice(np.arange(7,30))
            duration = np.random.choice(np.arange(1,30))
            self._end_day = self._start_day + duration



class Person(ABC):
    """Class that implements a sim person automaton with a pre-defined policy."""

    @abstractmethod
    def step(self, sim_time: SimTime, contact_tracer: Optional[ContactTracer] = None) -> Optional[NoOP]:
        """
        Method that steps through the person's policy. The step can return a
        NoOp to indicate no operation was carried out.

        :param sim_time: Current simulation time.
        :param contact_tracer: Traces of previous contacts of the person.
        :return: Return NoOp if no operation was carried out otherwise None.
        """
        pass

    @abstractmethod
    def receive_regulation(self, regulation: PandemicRegulation) -> None:
        """
        Receive a regulation that can potentially update the person's policy.

        :param regulation: a PandemicRegulation instance
        """
        pass

    @abstractmethod
    def enter_location(self, location_id: LocationID) -> bool:
        """
        Enter a location.

        :param location_id: LocationID instance
        :return: True if successful else False
        """
        pass

    @property
    @abstractmethod
    def id(self) -> PersonID:
        """
        Method that returns the id of the person.

        :return: ID of the person.
        """
        pass

    @property
    @abstractmethod
    def home(self) -> LocationID:
        """
        Property that returns the person's home location id.

        :return: ID of the home location
        """
        pass

    @property
    @abstractmethod
    def assigned_locations(self) -> Sequence[LocationID]:
        """
        Property that returns a sequence of location ids that the person is assigned to.

        :return: A collection of LocationIDs
        """
    
    @property
    @abstractmethod
    def travel_schedule(self)-> TravelSchedule:
        pass

    @travel_schedule.setter
    @abstractmethod
    def travel_schedule(self, schedule: TravelSchedule) -> None:
        pass


    @property
    @abstractmethod
    def state(self) -> PersonState:
        """
        Property that returns the current state of the person.

        :return: Current state of the person.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset person to its initial state."""
