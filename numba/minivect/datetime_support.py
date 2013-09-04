# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import
import numpy as np
from .miniutils import ctypes
from .minitypes import *

### Taken from Numba ###

# NOTE: The following ctypes structures were inspired by Joseph
# Heller's response to python-list question about ctypes complex
# support.  In that response, he said these were only suitable for
# Linux.  Might our milage vary?

class DateTimeMixin (object):
    def _get(self):
        return self._numpy_ty_('')

    def _set(self, value):
        self.timestamp = value.timestamp
        self.units = value.units

    value = property(_get, _set)

    @classmethod
    def from_param(cls, param):
        ret_val = cls()
        ret_val.value = param
        return ret_val

    @classmethod
    def make_ctypes_prototype_wrapper(cls, ctypes_prototype):
        '''This is a hack so that functions that return a complex type
        will construct a new Python value from the result, making the
        Numba compiled function a drop-in replacement for a Python
        function.'''
        # FIXME: See if there is some way of avoiding this additional
        # wrapper layer.
        def _make_datetime_result_wrapper(in_func):
            ctypes_function = ctypes_prototype(in_func)
            def _datetime_result_wrapper(*args, **kws):
                # Return the value property, not the ComplexMixin
                # instance built by ctypes.
                result = ctypes_function(*args, **kws)
                return result.value
            return _datetime_result_wrapper
        return _make_datetime_result_wrapper

class DateTime(ctypes.Structure, DateTimeMixin):
    _fields_ = [('timestamp', ctypes.c_int64), ('units', ctypes.c_int32)]
    _numpy_ty_ = np.datetime64


class TimeDeltaMixin (object):
    def _get(self):
        return self._numpy_ty_('%d-%d'.format(self.diff, self.units))

    def _set(self, value):
        self.diff = value.diff
        self.units = value.units

    value = property(_get, _set)

    @classmethod
    def from_param(cls, param):
        ret_val = cls()
        ret_val.value = param
        return ret_val

    @classmethod
    def make_ctypes_prototype_wrapper(cls, ctypes_prototype):
        '''This is a hack so that functions that return a complex type
        will construct a new Python value from the result, making the
        Numba compiled function a drop-in replacement for a Python
        function.'''
        # FIXME: See if there is some way of avoiding this additional
        # wrapper layer.
        def _make_timedelta_result_wrapper(in_func):
            ctypes_function = ctypes_prototype(in_func)
            def _timedelta_result_wrapper(*args, **kws):
                # Return the value property, not the ComplexMixin
                # instance built by ctypes.
                result = ctypes_function(*args, **kws)
                return result.value
            return _timedelta_result_wrapper
        return _make_timedelta_result_wrapper

class TimeDelta(ctypes.Structure, TimeDeltaMixin):
    _fields_ = [('diff', ctypes.c_int64), ('units', ctypes.c_int32)]


### End Taken from Numba ###
