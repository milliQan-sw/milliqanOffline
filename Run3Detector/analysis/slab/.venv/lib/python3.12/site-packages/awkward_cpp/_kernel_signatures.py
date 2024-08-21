# AUTO GENERATED ON 2024-08-02 AT 15:42:46
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-kernel-signatures.py
#
# (It is usually run as part of pip install . or localbuild.py.)

# fmt: off

from ctypes import (
    POINTER,
    Structure,
    c_bool,
    c_int8,
    c_uint8,
    c_int16,
    c_uint16,
    c_int32,
    c_uint32,
    c_int64,
    c_uint64,
    c_float,
    c_double,
    c_char_p,
)

import numpy as np

from numpy import (
    bool_,
    int8,
    uint8,
    int16,
    uint16,
    int32,
    uint32,
    int64,
    uint64,
    float32,
    float64,
)

class ERROR(Structure):
    _fields_ = [
        ("str", c_char_p),
        ("filename", c_char_p),
        ("id", c_int64),
        ("attempt", c_int64),
    ]


def by_signature(lib):
    out = {}

    f = lib.awkward_BitMaskedArray_to_ByteMaskedArray
    f.argtypes = [POINTER(c_int8), POINTER(c_uint8), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_BitMaskedArray_to_ByteMaskedArray', int8, uint8] = f

    f = lib.awkward_BitMaskedArray_to_IndexedOptionArray64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint8), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_BitMaskedArray_to_IndexedOptionArray', int64, uint8] = f

    f = lib.awkward_ByteMaskedArray_getitem_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_getitem_nextcarry', int64, int8] = f

    f = lib.awkward_ByteMaskedArray_getitem_nextcarry_outindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_getitem_nextcarry_outindex', int64, int64, int8] = f

    f = lib.awkward_ByteMaskedArray_numnull
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_numnull', int64, int8] = f

    f = lib.awkward_ByteMaskedArray_overlay_mask8
    f.argtypes = [POINTER(c_int8), POINTER(c_int8), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_overlay_mask', int8, int8, int8] = f

    f = lib.awkward_ByteMaskedArray_reduce_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_reduce_next_64', int64, int64, int64, int8, int64] = f

    f = lib.awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64', int64, int8] = f

    f = lib.awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, c_bool, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int8, int64] = f

    f = lib.awkward_ByteMaskedArray_toIndexedOptionArray64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ByteMaskedArray_toIndexedOptionArray', int64, int8] = f

    f = lib.awkward_Content_getitem_next_missing_jagged_getmaskstartstop
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'out', 'out', 'out', 'in']
    out['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', int64, int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArray_fill_to64_from32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_fill', int64, int32] = f

    f = lib.awkward_IndexedArray_fill_to64_from64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_fill', int64, int64] = f

    f = lib.awkward_IndexedArray_fill_to64_fromU32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_fill', int64, uint32] = f

    f = lib.awkward_IndexedArray_fill_to64_count
    f.argtypes = [POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_fill_count', int64] = f

    f = lib.awkward_IndexedArray32_flatten_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_nextcarry', int64, int32] = f

    f = lib.awkward_IndexedArray64_flatten_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_nextcarry', int64, int64] = f

    f = lib.awkward_IndexedArrayU32_flatten_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_nextcarry', int64, uint32] = f

    f = lib.awkward_IndexedArray32_flatten_none2empty_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_none2empty', int64, int32, int64] = f

    f = lib.awkward_IndexedArray64_flatten_none2empty_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_none2empty', int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_flatten_none2empty_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_flatten_none2empty', int64, uint32, int64] = f

    f = lib.awkward_IndexedArray32_getitem_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry', int64, int32] = f

    f = lib.awkward_IndexedArray64_getitem_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry', int64, int64] = f

    f = lib.awkward_IndexedArrayU32_getitem_nextcarry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry', int64, uint32] = f

    f = lib.awkward_IndexedArray32_getitem_nextcarry_outindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, int32, int32] = f

    f = lib.awkward_IndexedArray64_getitem_nextcarry_outindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_getitem_nextcarry_outindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, uint32, uint32] = f

    f = lib.awkward_IndexedArray_local_preparenext_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_local_preparenext_64', int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArray32_numnull
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_numnull', int64, int32] = f

    f = lib.awkward_IndexedArray64_numnull
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_numnull', int64, int64] = f

    f = lib.awkward_IndexedArrayU32_numnull
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_numnull', int64, uint32] = f

    f = lib.awkward_IndexedArray32_numnull_parents
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in']
    out['awkward_IndexedArray_numnull_parents', int64, int64, int32] = f

    f = lib.awkward_IndexedArray64_numnull_parents
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in']
    out['awkward_IndexedArray_numnull_parents', int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_numnull_parents
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in']
    out['awkward_IndexedArray_numnull_parents', int64, int64, uint32] = f

    f = lib.awkward_IndexedArray_numnull_unique_64
    f.argtypes = [POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in']
    out['awkward_IndexedArray_numnull_unique_64', int64] = f

    f = lib.awkward_IndexedArray32_index_of_nulls
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_index_of_nulls', int64, int32, int64, int64] = f

    f = lib.awkward_IndexedArray64_index_of_nulls
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_index_of_nulls', int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_index_of_nulls
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_index_of_nulls', int64, uint32, int64, int64] = f

    f = lib.awkward_IndexedArray32_overlay_mask8_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_overlay_mask', int64, int8, int32] = f

    f = lib.awkward_IndexedArray64_overlay_mask8_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_overlay_mask', int64, int8, int64] = f

    f = lib.awkward_IndexedArrayU32_overlay_mask8_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_overlay_mask', int64, int8, uint32] = f

    f = lib.awkward_IndexedArray32_reduce_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, int32, int64] = f

    f = lib.awkward_IndexedArray64_reduce_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_reduce_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, uint32, int64] = f

    f = lib.awkward_IndexedArray_reduce_next_fix_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_fix_offsets_64', int64, int64] = f

    f = lib.awkward_IndexedArray_unique_next_index_and_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_IndexedArray_unique_next_index_and_offsets_64', int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, int32] = f

    f = lib.awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, int64] = f

    f = lib.awkward_IndexedArrayU32_reduce_next_nonlocal_nextshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, uint32] = f

    f = lib.awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int32, int64] = f

    f = lib.awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_fromshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_reduce_next_nonlocal_nextshifts_fromshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, uint32, int64] = f

    f = lib.awkward_IndexedArray32_simplify32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int32, int32] = f

    f = lib.awkward_IndexedArray32_simplify64_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int32, int64] = f

    f = lib.awkward_IndexedArray32_simplifyU32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int32, uint32] = f

    f = lib.awkward_IndexedArray64_simplify32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int64, int32] = f

    f = lib.awkward_IndexedArray64_simplify64_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int64, int64] = f

    f = lib.awkward_IndexedArray64_simplifyU32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, int64, uint32] = f

    f = lib.awkward_IndexedArrayU32_simplify32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, uint32, int32] = f

    f = lib.awkward_IndexedArrayU32_simplify64_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, uint32, int64] = f

    f = lib.awkward_IndexedArrayU32_simplifyU32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_IndexedArray_simplify', int64, uint32, uint32] = f

    f = lib.awkward_IndexedArray32_validity
    f.argtypes = [POINTER(c_int32), c_int64, c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_IndexedArray_validity', int32] = f

    f = lib.awkward_IndexedArray64_validity
    f.argtypes = [POINTER(c_int64), c_int64, c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_IndexedArray_validity', int64] = f

    f = lib.awkward_IndexedArrayU32_validity
    f.argtypes = [POINTER(c_uint32), c_int64, c_int64, c_bool]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_IndexedArray_validity', uint32] = f

    f = lib.awkward_IndexedArray32_ranges_next_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    out['awkward_IndexedArray_ranges_next_64', int32, int64, int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArray64_ranges_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    out['awkward_IndexedArray_ranges_next_64', int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_ranges_next_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    out['awkward_IndexedArray_ranges_next_64', uint32, int64, int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArray32_ranges_carry_next_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_IndexedArray_ranges_carry_next_64', int32, int64, int64, int64] = f

    f = lib.awkward_IndexedArray64_ranges_carry_next_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_IndexedArray_ranges_carry_next_64', int64, int64, int64, int64] = f

    f = lib.awkward_IndexedArrayU32_ranges_carry_next_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_IndexedArray_ranges_carry_next_64', uint32, int64, int64, int64] = f

    f = lib.awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_IndexedOptionArray_rpad_and_clip_mask_axis1', int64, int8] = f

    f = lib.awkward_ListArray32_broadcast_tooffsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_broadcast_tooffsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_broadcast_tooffsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_combinations_64
    f.argtypes = [POINTER(POINTER(c_int64)), POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations', int64, int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_combinations_64
    f.argtypes = [POINTER(POINTER(c_int64)), POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations', int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_combinations_64
    f.argtypes = [POINTER(POINTER(c_int64)), POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations', int64, int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_combinations_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations_length', int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_combinations_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations_length', int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_combinations_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_combinations_length', int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_compact_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_compact_offsets', int64, int32, int32] = f

    f = lib.awkward_ListArray64_compact_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_compact_offsets', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_compact_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_compact_offsets', int64, uint32, uint32] = f

    f = lib.awkward_ListArray_fill_to64_from32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_fill', int64, int64, int32, int32] = f

    f = lib.awkward_ListArray_fill_to64_from64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_fill', int64, int64, int64, int64] = f

    f = lib.awkward_ListArray_fill_to64_fromU32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_fill', int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_getitem_jagged_apply_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_jagged_apply_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_jagged_apply_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray_getitem_jagged_carrylen_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_carrylen', int64, int64, int64] = f

    f = lib.awkward_ListArray32_getitem_jagged_descend_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int32), POINTER(c_int32)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_jagged_descend_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_jagged_descend_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_uint32), POINTER(c_uint32)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_getitem_jagged_expand_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_jagged_expand_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_jagged_expand_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, uint32, uint32] = f

    f = lib.awkward_ListArray_getitem_jagged_numvalid_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_numvalid', int64, int64, int64, int64] = f

    f = lib.awkward_ListArray_getitem_jagged_shrink_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_jagged_shrink', int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArray32_getitem_next_array_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array', int64, int64, int32, int32, int64] = f

    f = lib.awkward_ListArray64_getitem_next_array_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array', int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_array_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array', int64, int64, uint32, uint32, int64] = f

    f = lib.awkward_ListArray32_getitem_next_array_advanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, int32, int32, int64, int64] = f

    f = lib.awkward_ListArray64_getitem_next_array_advanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_array_advanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, uint32, uint32, int64, int64] = f

    f = lib.awkward_ListArray32_getitem_next_at_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_at', int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_next_at_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_at', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_at_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_at', int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_getitem_next_range_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range', int32, int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_next_range_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range', int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_range_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range', uint32, int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_getitem_next_range_carrylength
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_carrylength', int64, int32, int32] = f

    f = lib.awkward_ListArray64_getitem_next_range_carrylength
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_carrylength', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_range_carrylength
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_carrylength', int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_getitem_next_range_counts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_counts', int64, int32] = f

    f = lib.awkward_ListArray64_getitem_next_range_counts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_counts', int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_range_counts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_counts', int64, uint32] = f

    f = lib.awkward_ListArray32_getitem_next_range_spreadadvanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int32] = f

    f = lib.awkward_ListArray64_getitem_next_range_spreadadvanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_getitem_next_range_spreadadvanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, uint32] = f

    f = lib.awkward_ListArray32_localindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_localindex', int64, int32] = f

    f = lib.awkward_ListArray64_localindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_localindex', int64, int64] = f

    f = lib.awkward_ListArrayU32_localindex_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListArray_localindex', int64, uint32] = f

    f = lib.awkward_ListArray32_min_range
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_min_range', int64, int32, int32] = f

    f = lib.awkward_ListArray64_min_range
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_min_range', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_min_range
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListArray_min_range', int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_rpad_and_clip_length_axis1
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, int32, int32] = f

    f = lib.awkward_ListArray64_rpad_and_clip_length_axis1
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_rpad_and_clip_length_axis1
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, uint32, uint32] = f

    f = lib.awkward_ListArray32_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    out['awkward_ListArray_rpad_axis1', int64, int32, int32, int32, int32] = f

    f = lib.awkward_ListArray64_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    out['awkward_ListArray_rpad_axis1', int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListArrayU32_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    out['awkward_ListArray_rpad_axis1', int64, uint32, uint32, uint32, uint32] = f

    f = lib.awkward_ListArray32_validity
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_ListArray_validity', int32, int32] = f

    f = lib.awkward_ListArray64_validity
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_ListArray_validity', int64, int64] = f

    f = lib.awkward_ListArrayU32_validity
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in']
    out['awkward_ListArray_validity', uint32, uint32] = f

    f = lib.awkward_ListOffsetArray_drop_none_indexes_32
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_drop_none_indexes', int32, int32, int32] = f

    f = lib.awkward_ListOffsetArray_drop_none_indexes_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_drop_none_indexes', int64, int64, int64] = f

    f = lib.awkward_ListOffsetArray32_flatten_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_flatten_offsets', int64, int32, int64] = f

    f = lib.awkward_ListOffsetArray64_flatten_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_flatten_offsets', int64, int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_flatten_offsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_flatten_offsets', int64, uint32, int64] = f

    f = lib.awkward_ListOffsetArray_local_preparenext_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_local_preparenext_64', int64, int64] = f

    f = lib.awkward_ListOffsetArray32_reduce_local_nextparents_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int32] = f

    f = lib.awkward_ListOffsetArray64_reduce_local_nextparents_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_reduce_local_nextparents_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, uint32] = f

    f = lib.awkward_ListOffsetArray_reduce_local_outoffsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_local_outoffsets_64', int64, int64] = f

    f = lib.awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64', int64, int64, int64] = f

    f = lib.awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64', int64, int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64', int64, int64] = f

    f = lib.awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64', int64, int64, int64] = f

    f = lib.awkward_ListOffsetArray_reduce_nonlocal_preparenext_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_reduce_nonlocal_preparenext_64', int64, int64, int64, int64, int64, int64, int64] = f

    f = lib.awkward_ListOffsetArray32_rpad_and_clip_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int32] = f

    f = lib.awkward_ListOffsetArray64_rpad_and_clip_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_rpad_and_clip_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, uint32] = f

    f = lib.awkward_ListOffsetArray32_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_axis1', int64, int32] = f

    f = lib.awkward_ListOffsetArray64_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_axis1', int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_rpad_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_rpad_axis1', int64, uint32] = f

    f = lib.awkward_ListOffsetArray32_rpad_length_axis1
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'out']
    out['awkward_ListOffsetArray_rpad_length_axis1', int32, int32, int64] = f

    f = lib.awkward_ListOffsetArray64_rpad_length_axis1
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'out']
    out['awkward_ListOffsetArray_rpad_length_axis1', int64, int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_rpad_length_axis1
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'out']
    out['awkward_ListOffsetArray_rpad_length_axis1', uint32, uint32, int64] = f

    f = lib.awkward_ListOffsetArray32_toRegularArray
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_toRegularArray', int64, int32] = f

    f = lib.awkward_ListOffsetArray64_toRegularArray
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_toRegularArray', int64, int64] = f

    f = lib.awkward_ListOffsetArrayU32_toRegularArray
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_ListOffsetArray_toRegularArray', int64, uint32] = f

    f = lib.awkward_MaskedArray32_getitem_next_jagged_project
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    out['awkward_MaskedArray_getitem_next_jagged_project', int32, int64, int64, int64, int64] = f

    f = lib.awkward_MaskedArray64_getitem_next_jagged_project
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    out['awkward_MaskedArray_getitem_next_jagged_project', int64, int64, int64, int64, int64] = f

    f = lib.awkward_MaskedArrayU32_getitem_next_jagged_project
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    out['awkward_MaskedArray_getitem_next_jagged_project', uint32, int64, int64, int64, int64] = f

    f = lib.awkward_NumpyArray_rearrange_shifted_toint64_fromint64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_NumpyArray_rearrange_shifted', int64, int64, int64, int64, int64] = f

    f = lib.awkward_NumpyArray_reduce_adjust_starts_64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_NumpyArray_reduce_adjust_starts_64', int64, int64, int64] = f

    f = lib.awkward_NumpyArray_reduce_adjust_starts_shifts_64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_NumpyArray_reduce_adjust_starts_shifts_64', int64, int64, int64, int64] = f

    f = lib.awkward_NumpyArray_reduce_mask_ByteMaskedArray_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_NumpyArray_reduce_mask_ByteMaskedArray_64', int8, int64] = f

    f = lib.awkward_ListOffsetArray_argsort_strings
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_uint8), POINTER(c_int64), POINTER(c_int64), c_bool, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_ListOffsetArray_argsort_strings', int64, int64, uint8, int64, int64] = f

    f = lib.awkward_NumpyArray_sort_asstrings_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_uint8), POINTER(c_int64), c_int64, POINTER(c_int64), c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'out', 'in', 'in']
    out['awkward_NumpyArray_sort_asstrings_uint8', uint8, uint8, int64, int64] = f

    f = lib.awkward_NumpyArray_unique_strings_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out', 'out']
    out['awkward_NumpyArray_unique_strings', uint8, int64, int64, int64] = f

    f = lib.awkward_NumpyArray_prepare_utf8_to_utf32_padded
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'out']
    out['awkward_NumpyArray_prepare_utf8_to_utf32_padded', uint8, int64, int64] = f

    f = lib.awkward_NumpyArray_utf8_to_utf32_padded
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64, POINTER(c_uint32)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_utf8_to_utf32_padded', uint8, int64, uint32] = f

    f = lib.awkward_NumpyArray_pad_zero_to_length_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64, POINTER(c_uint8)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_pad_zero_to_length', uint8, int64, uint8] = f

    f = lib.awkward_NumpyArray_subrange_equal_bool
    f.argtypes = [POINTER(c_bool), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal_bool', bool_, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_int8
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', int8, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_int16
    f.argtypes = [POINTER(c_int16), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', int16, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_int32
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', int32, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_int64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', int64, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', uint8, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_uint16
    f.argtypes = [POINTER(c_uint16), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', uint16, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_uint32
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', uint32, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_uint64
    f.argtypes = [POINTER(c_uint64), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', uint64, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_float32
    f.argtypes = [POINTER(c_float), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', float32, int64, int64, bool_] = f

    f = lib.awkward_NumpyArray_subrange_equal_float64
    f.argtypes = [POINTER(c_double), POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_bool)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'out']
    out['awkward_NumpyArray_subrange_equal', float64, int64, int64, bool_] = f

    f = lib.awkward_RecordArray_reduce_nonlocal_outoffsets_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_RecordArray_reduce_nonlocal_outoffsets_64', int64, int64, int64] = f

    f = lib.awkward_RegularArray_combinations_64
    f.argtypes = [POINTER(POINTER(c_int64)), POINTER(c_int64), POINTER(c_int64), c_int64, c_bool, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_RegularArray_combinations_64', int64, int64, int64] = f

    f = lib.awkward_RegularArray_getitem_carry_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_carry', int64, int64] = f

    f = lib.awkward_RegularArray_getitem_jagged_expand_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_jagged_expand', int64, int64, int64] = f

    f = lib.awkward_RegularArray_getitem_next_array_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_array', int64, int64, int64] = f

    f = lib.awkward_RegularArray_getitem_next_array_advanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_array_advanced', int64, int64, int64, int64] = f

    f = lib.awkward_RegularArray_getitem_next_array_regularize_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_array_regularize', int64, int64] = f

    f = lib.awkward_RegularArray_getitem_next_at_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_at', int64] = f

    f = lib.awkward_RegularArray_getitem_next_range_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_range', int64] = f

    f = lib.awkward_RegularArray_getitem_next_range_spreadadvanced_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_RegularArray_getitem_next_range_spreadadvanced', int64, int64] = f

    f = lib.awkward_RegularArray_localindex_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_RegularArray_localindex', int64] = f

    f = lib.awkward_RegularArray_reduce_local_nextparents_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_RegularArray_reduce_local_nextparents_64', int64] = f

    f = lib.awkward_RegularArray_reduce_nonlocal_preparenext_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_RegularArray_reduce_nonlocal_preparenext_64', int64, int64, int64] = f

    f = lib.awkward_RegularArray_rpad_and_clip_axis1_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_RegularArray_rpad_and_clip_axis1', int64] = f

    f = lib.awkward_UnionArray_fillindex_to64_from32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_UnionArray_fillindex', int64, int32] = f

    f = lib.awkward_UnionArray_fillindex_to64_from64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_UnionArray_fillindex', int64, int64] = f

    f = lib.awkward_UnionArray_fillindex_to64_fromU32
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_UnionArray_fillindex', int64, uint32] = f

    f = lib.awkward_UnionArray_fillindex_to64_count
    f.argtypes = [POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_UnionArray_fillindex_count', int64] = f

    f = lib.awkward_UnionArray_fillna_from32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_UnionArray_fillna', int64, int32] = f

    f = lib.awkward_UnionArray_fillna_from64_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_UnionArray_fillna', int64, int64] = f

    f = lib.awkward_UnionArray_fillna_fromU32_to64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_UnionArray_fillna', int64, uint32] = f

    f = lib.awkward_UnionArray_filltags_to8_from8
    f.argtypes = [POINTER(c_int8), c_int64, POINTER(c_int8), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_filltags', int8, int8] = f

    f = lib.awkward_UnionArray_filltags_to8_const
    f.argtypes = [POINTER(c_int8), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_UnionArray_filltags_const', int8] = f

    f = lib.awkward_UnionArray32_flatten_combine_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, int32, int64] = f

    f = lib.awkward_UnionArray64_flatten_combine_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, int64, int64] = f

    f = lib.awkward_UnionArrayU32_flatten_combine_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, uint32, int64] = f

    f = lib.awkward_UnionArray32_flatten_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_length', int64, int8, int32, int64] = f

    f = lib.awkward_UnionArray64_flatten_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_length', int64, int8, int64, int64] = f

    f = lib.awkward_UnionArrayU32_flatten_length_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64, POINTER(POINTER(c_int64))]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_flatten_length', int64, int8, uint32, int64] = f

    f = lib.awkward_UnionArray8_32_nestedfill_tags_index_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int32), POINTER(c_int64), c_int8, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_nestedfill_tags_index', int8, int32, int64, int64] = f

    f = lib.awkward_UnionArray8_64_nestedfill_tags_index_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int64), c_int8, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_nestedfill_tags_index', int8, int64, int64, int64] = f

    f = lib.awkward_UnionArray8_U32_nestedfill_tags_index_64
    f.argtypes = [POINTER(c_int8), POINTER(c_uint32), POINTER(c_int64), c_int8, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_nestedfill_tags_index', int8, uint32, int64, int64] = f

    f = lib.awkward_UnionArray8_32_project_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_project', int64, int64, int8, int32] = f

    f = lib.awkward_UnionArray8_64_project_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_project', int64, int64, int8, int64] = f

    f = lib.awkward_UnionArray8_U32_project_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_project', int64, int64, int8, uint32] = f

    f = lib.awkward_UnionArray8_32_regular_index
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), c_int64, POINTER(c_int8), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_regular_index', int32, int32, int8] = f

    f = lib.awkward_UnionArray8_64_regular_index
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int8), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_regular_index', int64, int64, int8] = f

    f = lib.awkward_UnionArray8_U32_regular_index
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), c_int64, POINTER(c_int8), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in']
    out['awkward_UnionArray_regular_index', uint32, uint32, int8] = f

    f = lib.awkward_UnionArray8_regular_index_getsize
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_UnionArray_regular_index_getsize', int64, int8] = f

    f = lib.awkward_UnionArray8_32_simplify8_32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), POINTER(c_int8), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int32] = f

    f = lib.awkward_UnionArray8_32_simplify8_64_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int64] = f

    f = lib.awkward_UnionArray8_32_simplify8_U32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, uint32] = f

    f = lib.awkward_UnionArray8_64_simplify8_32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int32] = f

    f = lib.awkward_UnionArray8_64_simplify8_64_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int64] = f

    f = lib.awkward_UnionArray8_64_simplify8_U32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, uint32] = f

    f = lib.awkward_UnionArray8_U32_simplify8_32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), POINTER(c_int8), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int32] = f

    f = lib.awkward_UnionArray8_U32_simplify8_64_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int64] = f

    f = lib.awkward_UnionArray8_U32_simplify8_U32_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, uint32] = f

    f = lib.awkward_UnionArray8_32_simplify_one_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify_one', int8, int64, int8, int32] = f

    f = lib.awkward_UnionArray8_64_simplify_one_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify_one', int8, int64, int8, int64] = f

    f = lib.awkward_UnionArray8_U32_simplify_one_to8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_simplify_one', int8, int64, int8, uint32] = f

    f = lib.awkward_UnionArray8_32_validity
    f.argtypes = [POINTER(c_int8), POINTER(c_int32), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_validity', int8, int32, int64] = f

    f = lib.awkward_UnionArray8_64_validity
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_validity', int8, int64, int64] = f

    f = lib.awkward_UnionArray8_U32_validity
    f.argtypes = [POINTER(c_int8), POINTER(c_uint32), c_int64, c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['in', 'in', 'in', 'in', 'in']
    out['awkward_UnionArray_validity', int8, uint32, int64] = f

    f = lib.awkward_argsort_bool
    f.argtypes = [POINTER(c_int64), POINTER(c_bool), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, bool_, int64] = f

    f = lib.awkward_argsort_int8
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, int8, int64] = f

    f = lib.awkward_argsort_int16
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, int16, int64] = f

    f = lib.awkward_argsort_int32
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, int32, int64] = f

    f = lib.awkward_argsort_int64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, int64, int64] = f

    f = lib.awkward_argsort_uint8
    f.argtypes = [POINTER(c_int64), POINTER(c_uint8), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, uint8, int64] = f

    f = lib.awkward_argsort_uint16
    f.argtypes = [POINTER(c_int64), POINTER(c_uint16), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, uint16, int64] = f

    f = lib.awkward_argsort_uint32
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, uint32, int64] = f

    f = lib.awkward_argsort_uint64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint64), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, uint64, int64] = f

    f = lib.awkward_argsort_float32
    f.argtypes = [POINTER(c_int64), POINTER(c_float), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, float32, int64] = f

    f = lib.awkward_argsort_float64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), c_int64, POINTER(c_int64), c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_argsort', int64, float64, int64] = f

    f = lib.awkward_index_rpad_and_clip_axis0_64
    f.argtypes = [POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_index_rpad_and_clip_axis0', int64] = f

    f = lib.awkward_index_rpad_and_clip_axis1_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'out', 'in', 'in']
    out['awkward_index_rpad_and_clip_axis1', int64, int64] = f

    f = lib.awkward_Index_nones_as_index_64
    f.argtypes = [POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in']
    out['awkward_Index_nones_as_index', int64] = f

    f = lib.awkward_localindex_64
    f.argtypes = [POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in']
    out['awkward_localindex', int64] = f

    f = lib.awkward_missing_repeat_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_missing_repeat', int64, int64] = f

    f = lib.awkward_reduce_argmax_int8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, int8, int64] = f

    f = lib.awkward_reduce_argmax_int16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, int16, int64] = f

    f = lib.awkward_reduce_argmax_int32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, int32, int64] = f

    f = lib.awkward_reduce_argmax_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, int64, int64] = f

    f = lib.awkward_reduce_argmax_uint8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, uint8, int64] = f

    f = lib.awkward_reduce_argmax_uint16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, uint16, int64] = f

    f = lib.awkward_reduce_argmax_uint32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, uint32, int64] = f

    f = lib.awkward_reduce_argmax_uint64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, uint64, int64] = f

    f = lib.awkward_reduce_argmax_float32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, float32, int64] = f

    f = lib.awkward_reduce_argmax_float64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax', int64, float64, int64] = f

    f = lib.awkward_reduce_argmax_complex64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax_complex', int64, float32, int64] = f

    f = lib.awkward_reduce_argmax_complex128_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmax_complex', int64, float64, int64] = f

    f = lib.awkward_reduce_argmin_int8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, int8, int64] = f

    f = lib.awkward_reduce_argmin_int16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, int16, int64] = f

    f = lib.awkward_reduce_argmin_int32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, int32, int64] = f

    f = lib.awkward_reduce_argmin_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, int64, int64] = f

    f = lib.awkward_reduce_argmin_uint8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, uint8, int64] = f

    f = lib.awkward_reduce_argmin_uint16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, uint16, int64] = f

    f = lib.awkward_reduce_argmin_uint32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, uint32, int64] = f

    f = lib.awkward_reduce_argmin_uint64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, uint64, int64] = f

    f = lib.awkward_reduce_argmin_float32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, float32, int64] = f

    f = lib.awkward_reduce_argmin_float64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin', int64, float64, int64] = f

    f = lib.awkward_reduce_argmin_complex64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin_complex', int64, float32, int64] = f

    f = lib.awkward_reduce_argmin_complex128_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_argmin_complex', int64, float64, int64] = f

    f = lib.awkward_reduce_count_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_reduce_count_64', int64, int64] = f

    f = lib.awkward_reduce_countnonzero_bool_64
    f.argtypes = [POINTER(c_int64), POINTER(c_bool), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, bool_, int64] = f

    f = lib.awkward_reduce_countnonzero_int8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, int8, int64] = f

    f = lib.awkward_reduce_countnonzero_int16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, int16, int64] = f

    f = lib.awkward_reduce_countnonzero_int32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, int32, int64] = f

    f = lib.awkward_reduce_countnonzero_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, int64, int64] = f

    f = lib.awkward_reduce_countnonzero_uint8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, uint8, int64] = f

    f = lib.awkward_reduce_countnonzero_uint16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, uint16, int64] = f

    f = lib.awkward_reduce_countnonzero_uint32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, uint32, int64] = f

    f = lib.awkward_reduce_countnonzero_uint64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, uint64, int64] = f

    f = lib.awkward_reduce_countnonzero_float32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, float32, int64] = f

    f = lib.awkward_reduce_countnonzero_float64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero', int64, float64, int64] = f

    f = lib.awkward_reduce_countnonzero_complex64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero_complex', int64, float32, int64] = f

    f = lib.awkward_reduce_countnonzero_complex128_64
    f.argtypes = [POINTER(c_int64), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_countnonzero_complex', int64, float64, int64] = f

    f = lib.awkward_reduce_max_int8_int8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int8]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', int8, int8, int64] = f

    f = lib.awkward_reduce_max_int16_int16_64
    f.argtypes = [POINTER(c_int16), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64, c_int16]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', int16, int16, int64] = f

    f = lib.awkward_reduce_max_int32_int32_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64, c_int32]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', int32, int32, int64] = f

    f = lib.awkward_reduce_max_int64_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', int64, int64, int64] = f

    f = lib.awkward_reduce_max_uint8_uint8_64
    f.argtypes = [POINTER(c_uint8), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64, c_uint8]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', uint8, uint8, int64] = f

    f = lib.awkward_reduce_max_uint16_uint16_64
    f.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64, c_uint16]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', uint16, uint16, int64] = f

    f = lib.awkward_reduce_max_uint32_uint32_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64, c_uint32]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', uint32, uint32, int64] = f

    f = lib.awkward_reduce_max_uint64_uint64_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64, c_uint64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', uint64, uint64, int64] = f

    f = lib.awkward_reduce_max_float32_float32_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64, c_float]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', float32, float32, int64] = f

    f = lib.awkward_reduce_max_float64_float64_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64, c_double]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max', float64, float64, int64] = f

    f = lib.awkward_reduce_max_complex64_complex64_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64, c_float]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max_complex', float32, float32, int64] = f

    f = lib.awkward_reduce_max_complex128_complex128_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64, c_double]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_max_complex', float64, float64, int64] = f

    f = lib.awkward_reduce_min_int8_int8_64
    f.argtypes = [POINTER(c_int8), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64, c_int8]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', int8, int8, int64] = f

    f = lib.awkward_reduce_min_int16_int16_64
    f.argtypes = [POINTER(c_int16), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64, c_int16]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', int16, int16, int64] = f

    f = lib.awkward_reduce_min_int32_int32_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64, c_int32]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', int32, int32, int64] = f

    f = lib.awkward_reduce_min_int64_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', int64, int64, int64] = f

    f = lib.awkward_reduce_min_uint8_uint8_64
    f.argtypes = [POINTER(c_uint8), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64, c_uint8]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', uint8, uint8, int64] = f

    f = lib.awkward_reduce_min_uint16_uint16_64
    f.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64, c_uint16]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', uint16, uint16, int64] = f

    f = lib.awkward_reduce_min_uint32_uint32_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64, c_uint32]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', uint32, uint32, int64] = f

    f = lib.awkward_reduce_min_uint64_uint64_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64, c_uint64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', uint64, uint64, int64] = f

    f = lib.awkward_reduce_min_float32_float32_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64, c_float]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', float32, float32, int64] = f

    f = lib.awkward_reduce_min_float64_float64_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64, c_double]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min', float64, float64, int64] = f

    f = lib.awkward_reduce_min_complex64_complex64_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64, c_float]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min_complex', float32, float32, int64] = f

    f = lib.awkward_reduce_min_complex128_complex128_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64, c_double]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    out['awkward_reduce_min_complex', float64, float64, int64] = f

    f = lib.awkward_reduce_prod_int32_int8_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int32, int8, int64] = f

    f = lib.awkward_reduce_prod_int32_int16_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int32, int16, int64] = f

    f = lib.awkward_reduce_prod_int32_int32_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int32, int32, int64] = f

    f = lib.awkward_reduce_prod_int64_int8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int64, int8, int64] = f

    f = lib.awkward_reduce_prod_int64_int16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int64, int16, int64] = f

    f = lib.awkward_reduce_prod_int64_int32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int64, int32, int64] = f

    f = lib.awkward_reduce_prod_int64_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', int64, int64, int64] = f

    f = lib.awkward_reduce_prod_uint32_uint8_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint32, uint8, int64] = f

    f = lib.awkward_reduce_prod_uint32_uint16_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint32, uint16, int64] = f

    f = lib.awkward_reduce_prod_uint32_uint32_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint32, uint32, int64] = f

    f = lib.awkward_reduce_prod_uint64_uint8_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint64, uint8, int64] = f

    f = lib.awkward_reduce_prod_uint64_uint16_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint64, uint16, int64] = f

    f = lib.awkward_reduce_prod_uint64_uint32_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint64, uint32, int64] = f

    f = lib.awkward_reduce_prod_uint64_uint64_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', uint64, uint64, int64] = f

    f = lib.awkward_reduce_prod_float32_float32_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', float32, float32, int64] = f

    f = lib.awkward_reduce_prod_float64_float64_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod', float64, float64, int64] = f

    f = lib.awkward_reduce_prod_complex64_complex64_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_complex', float32, float32, int64] = f

    f = lib.awkward_reduce_prod_complex128_complex128_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_complex', float64, float64, int64] = f

    f = lib.awkward_reduce_prod_bool_bool_64
    f.argtypes = [POINTER(c_bool), POINTER(c_bool), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, bool_, int64] = f

    f = lib.awkward_reduce_prod_bool_int8_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, int8, int64] = f

    f = lib.awkward_reduce_prod_bool_int16_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, int16, int64] = f

    f = lib.awkward_reduce_prod_bool_int32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, int32, int64] = f

    f = lib.awkward_reduce_prod_bool_int64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, int64, int64] = f

    f = lib.awkward_reduce_prod_bool_uint8_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, uint8, int64] = f

    f = lib.awkward_reduce_prod_bool_uint16_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, uint16, int64] = f

    f = lib.awkward_reduce_prod_bool_uint32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, uint32, int64] = f

    f = lib.awkward_reduce_prod_bool_uint64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, uint64, int64] = f

    f = lib.awkward_reduce_prod_bool_float32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, float32, int64] = f

    f = lib.awkward_reduce_prod_bool_float64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool', bool_, float64, int64] = f

    f = lib.awkward_reduce_prod_bool_complex64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool_complex', bool_, float32, int64] = f

    f = lib.awkward_reduce_prod_bool_complex128_64
    f.argtypes = [POINTER(c_bool), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_prod_bool_complex', bool_, float64, int64] = f

    f = lib.awkward_reduce_sum_int32_int8_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int32, int8, int64] = f

    f = lib.awkward_reduce_sum_int32_int16_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int32, int16, int64] = f

    f = lib.awkward_reduce_sum_int32_int32_64
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int32, int32, int64] = f

    f = lib.awkward_reduce_sum_int64_int8_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int64, int8, int64] = f

    f = lib.awkward_reduce_sum_int64_int16_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int64, int16, int64] = f

    f = lib.awkward_reduce_sum_int64_int32_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int64, int32, int64] = f

    f = lib.awkward_reduce_sum_int64_int64_64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', int64, int64, int64] = f

    f = lib.awkward_reduce_sum_uint32_uint8_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint32, uint8, int64] = f

    f = lib.awkward_reduce_sum_uint32_uint16_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint32, uint16, int64] = f

    f = lib.awkward_reduce_sum_uint32_uint32_64
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint32, uint32, int64] = f

    f = lib.awkward_reduce_sum_uint64_uint8_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint64, uint8, int64] = f

    f = lib.awkward_reduce_sum_uint64_uint16_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint64, uint16, int64] = f

    f = lib.awkward_reduce_sum_uint64_uint32_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint64, uint32, int64] = f

    f = lib.awkward_reduce_sum_uint64_uint64_64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', uint64, uint64, int64] = f

    f = lib.awkward_reduce_sum_float32_float32_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', float32, float32, int64] = f

    f = lib.awkward_reduce_sum_float64_float64_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum', float64, float64, int64] = f

    f = lib.awkward_reduce_sum_complex64_complex64_64
    f.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_complex', float32, float32, int64] = f

    f = lib.awkward_reduce_sum_complex128_complex128_64
    f.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_complex', float64, float64, int64] = f

    f = lib.awkward_reduce_sum_bool_bool_64
    f.argtypes = [POINTER(c_bool), POINTER(c_bool), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, bool_, int64] = f

    f = lib.awkward_reduce_sum_bool_int8_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, int8, int64] = f

    f = lib.awkward_reduce_sum_bool_int16_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, int16, int64] = f

    f = lib.awkward_reduce_sum_bool_int32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, int32, int64] = f

    f = lib.awkward_reduce_sum_bool_int64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_int64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, int64, int64] = f

    f = lib.awkward_reduce_sum_bool_uint8_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint8), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, uint8, int64] = f

    f = lib.awkward_reduce_sum_bool_uint16_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint16), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, uint16, int64] = f

    f = lib.awkward_reduce_sum_bool_uint32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint32), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, uint32, int64] = f

    f = lib.awkward_reduce_sum_bool_uint64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_uint64), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, uint64, int64] = f

    f = lib.awkward_reduce_sum_bool_float32_64
    f.argtypes = [POINTER(c_bool), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, float32, int64] = f

    f = lib.awkward_reduce_sum_bool_float64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool', bool_, float64, int64] = f

    f = lib.awkward_reduce_sum_bool_complex64_64
    f.argtypes = [POINTER(c_bool), POINTER(c_float), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool_complex', bool_, float32, int64] = f

    f = lib.awkward_reduce_sum_bool_complex128_64
    f.argtypes = [POINTER(c_bool), POINTER(c_double), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_bool_complex', bool_, float64, int64] = f

    f = lib.awkward_reduce_sum_int32_bool_64
    f.argtypes = [POINTER(c_int32), POINTER(c_bool), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_int32_bool_64', int32, bool_, int64] = f

    f = lib.awkward_reduce_sum_int64_bool_64
    f.argtypes = [POINTER(c_int64), POINTER(c_bool), POINTER(c_int64), c_int64, c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_reduce_sum_int64_bool_64', int64, bool_, int64] = f

    f = lib.awkward_sort_bool
    f.argtypes = [POINTER(c_bool), POINTER(c_bool), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', bool_, bool_, int64] = f

    f = lib.awkward_sort_int8
    f.argtypes = [POINTER(c_int8), POINTER(c_int8), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', int8, int8, int64] = f

    f = lib.awkward_sort_int16
    f.argtypes = [POINTER(c_int16), POINTER(c_int16), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', int16, int16, int64] = f

    f = lib.awkward_sort_int32
    f.argtypes = [POINTER(c_int32), POINTER(c_int32), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', int32, int32, int64] = f

    f = lib.awkward_sort_int64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', int64, int64, int64] = f

    f = lib.awkward_sort_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_uint8), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', uint8, uint8, int64] = f

    f = lib.awkward_sort_uint16
    f.argtypes = [POINTER(c_uint16), POINTER(c_uint16), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', uint16, uint16, int64] = f

    f = lib.awkward_sort_uint32
    f.argtypes = [POINTER(c_uint32), POINTER(c_uint32), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', uint32, uint32, int64] = f

    f = lib.awkward_sort_uint64
    f.argtypes = [POINTER(c_uint64), POINTER(c_uint64), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', uint64, uint64, int64] = f

    f = lib.awkward_sort_float32
    f.argtypes = [POINTER(c_float), POINTER(c_float), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', float32, float32, int64] = f

    f = lib.awkward_sort_float64
    f.argtypes = [POINTER(c_double), POINTER(c_double), c_int64, POINTER(c_int64), c_int64, c_int64, c_bool, c_bool]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    out['awkward_sort', float64, float64, int64] = f

    f = lib.awkward_unique_offsets_int8
    f.argtypes = [POINTER(c_int8), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_unique_offsets', int8, int64, int64] = f

    f = lib.awkward_unique_offsets_int16
    f.argtypes = [POINTER(c_int16), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_unique_offsets', int16, int64, int64] = f

    f = lib.awkward_unique_offsets_int32
    f.argtypes = [POINTER(c_int32), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_unique_offsets', int32, int64, int64] = f

    f = lib.awkward_unique_offsets_int64
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in', 'in']
    out['awkward_unique_offsets', int64, int64, int64] = f

    f = lib.awkward_unique_ranges_bool
    f.argtypes = [POINTER(c_bool), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges_bool', bool_, int64, int64] = f

    f = lib.awkward_unique_ranges_int8
    f.argtypes = [POINTER(c_int8), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', int8, int64, int64] = f

    f = lib.awkward_unique_ranges_int16
    f.argtypes = [POINTER(c_int16), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', int16, int64, int64] = f

    f = lib.awkward_unique_ranges_int32
    f.argtypes = [POINTER(c_int32), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', int32, int64, int64] = f

    f = lib.awkward_unique_ranges_int64
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', int64, int64, int64] = f

    f = lib.awkward_unique_ranges_uint8
    f.argtypes = [POINTER(c_uint8), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', uint8, int64, int64] = f

    f = lib.awkward_unique_ranges_uint16
    f.argtypes = [POINTER(c_uint16), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', uint16, int64, int64] = f

    f = lib.awkward_unique_ranges_uint32
    f.argtypes = [POINTER(c_uint32), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', uint32, int64, int64] = f

    f = lib.awkward_unique_ranges_uint64
    f.argtypes = [POINTER(c_uint64), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', uint64, int64, int64] = f

    f = lib.awkward_unique_ranges_float32
    f.argtypes = [POINTER(c_float), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', float32, int64, int64] = f

    f = lib.awkward_unique_ranges_float64
    f.argtypes = [POINTER(c_double), POINTER(c_int64), c_int64, POINTER(c_int64)]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'out']
    out['awkward_unique_ranges', float64, int64, int64] = f

    f = lib.awkward_sorting_ranges
    f.argtypes = [POINTER(c_int64), c_int64, POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in', 'in']
    out['awkward_sorting_ranges', int64, int64] = f

    f = lib.awkward_sorting_ranges_length
    f.argtypes = [POINTER(c_int64), POINTER(c_int64), c_int64]
    f.restype = ERROR
    f.dir = ['out', 'in', 'in']
    out['awkward_sorting_ranges_length', int64, int64] = f

    return out
