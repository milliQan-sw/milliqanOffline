# AUTO GENERATED ON 2024-08-02 AT 15:42:46
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-kernel-signatures.py
#
# This step is normally run explicitly before generating a package

# fmt: off

# pylint: skip-file

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

from awkward._connect.cuda import fetch_specialization
from awkward._connect.cuda import import_cupy

import math

cupy = import_cupy("Awkward Arrays with CUDA")

def by_signature(cuda_kernel_templates):
    out = {}

    def min_max_type(dtype):
      supported_types = {
          'bool': cupy.int32,
          'int8': cupy.int32,
          'int16': cupy.int32,
          'int32': cupy.int32,
          'int64': cupy.int64,
          'uint8': cupy.uint32,
          'uint16': cupy.uint32,
          'uint32': cupy.uint32,
          'uint64': cupy.uint64,
          'float32': cupy.float32,
          'float64': cupy.float64
      }
      if str(dtype) in supported_types:
          return supported_types[str(dtype)]
      else:
          raise ValueError("Unsupported dtype.", dtype)

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_BitMaskedArray_to_ByteMaskedArray', int8, uint8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, False]
    out['awkward_BitMaskedArray_to_ByteMaskedArray', int8, uint8] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_BitMaskedArray_to_IndexedOptionArray', int64, uint8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, False]
    out['awkward_BitMaskedArray_to_IndexedOptionArray', int64, uint8] = f

    def f(grid, block, args):
        (tocarry, mask, length, validwhen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_getitem_nextcarry_a', tocarry.dtype, mask.dtype]))(grid, block, (tocarry, mask, length, validwhen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_getitem_nextcarry_b', tocarry.dtype, mask.dtype]))(grid, block, (tocarry, mask, length, validwhen, scan_in_array, invocation_index, err_code))
    out["awkward_ByteMaskedArray_getitem_nextcarry_a", int64, int8] = None
    out["awkward_ByteMaskedArray_getitem_nextcarry_b", int64, int8] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ByteMaskedArray_getitem_nextcarry', int64, int8] = f

    def f(grid, block, args):
        (tocarry, outindex, mask, length, validwhen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_getitem_nextcarry_outindex_a', tocarry.dtype, outindex.dtype, mask.dtype]))(grid, block, (tocarry, outindex, mask, length, validwhen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_getitem_nextcarry_outindex_b', tocarry.dtype, outindex.dtype, mask.dtype]))(grid, block, (tocarry, outindex, mask, length, validwhen, scan_in_array, invocation_index, err_code))
    out["awkward_ByteMaskedArray_getitem_nextcarry_outindex_a", int64, int64, int8] = None
    out["awkward_ByteMaskedArray_getitem_nextcarry_outindex_b", int64, int64, int8] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ByteMaskedArray_getitem_nextcarry_outindex', int64, int64, int8] = f

    def f(grid, block, args):
        (numnull, mask, length, validwhen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_numnull_a', numnull.dtype, mask.dtype]))(grid, block, (numnull, mask, length, validwhen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_numnull_b', numnull.dtype, mask.dtype]))(grid, block, (numnull, mask, length, validwhen, scan_in_array, invocation_index, err_code))
    out["awkward_ByteMaskedArray_numnull_a", int64, int8] = None
    out["awkward_ByteMaskedArray_numnull_b", int64, int8] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ByteMaskedArray_numnull', int64, int8] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_overlay_mask', int8, int8, int8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ByteMaskedArray_overlay_mask', int8, int8, int8] = f

    def f(grid, block, args):
        (nextcarry, nextparents, outindex, mask, parents, length, validwhen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_reduce_next_64_a', nextcarry.dtype, nextparents.dtype, outindex.dtype, mask.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, mask, parents, length, validwhen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_reduce_next_64_b', nextcarry.dtype, nextparents.dtype, outindex.dtype, mask.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, mask, parents, length, validwhen, scan_in_array, invocation_index, err_code))
    out["awkward_ByteMaskedArray_reduce_next_64_a", int64, int64, int64, int8, int64] = None
    out["awkward_ByteMaskedArray_reduce_next_64_b", int64, int64, int64, int8, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False]
    out['awkward_ByteMaskedArray_reduce_next_64', int64, int64, int64, int8, int64] = f

    def f(grid, block, args):
        (nextshifts, mask, length, valid_when, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_a", nextshifts.dtype, mask.dtype]))(grid, block, (nextshifts, mask, length, valid_when, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_b", nextshifts.dtype, mask.dtype]))(grid, block, (nextshifts, mask, length, valid_when, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_a", int64, int8] = None
    out["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_b", int64, int8] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64', int64, int8] = f

    def f(grid, block, args):
        (nextshifts, mask, length, valid_when, shifts, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", nextshifts.dtype, mask.dtype, shifts.dtype]))(grid, block, (nextshifts, mask, length, valid_when, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", nextshifts.dtype, mask.dtype, shifts.dtype]))(grid, block, (nextshifts, mask, length, valid_when, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", int64, int8, int64] = None
    out["awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", int64, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ByteMaskedArray_toIndexedOptionArray', int64, int8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ByteMaskedArray_toIndexedOptionArray', int64, int8] = f

    def f(grid, block, args):
        (index_in, offsets_in, mask_out, starts_out, stops_out, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_Content_getitem_next_missing_jagged_getmaskstartstop_a", index_in.dtype, offsets_in.dtype, mask_out.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index_in, offsets_in, mask_out, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_Content_getitem_next_missing_jagged_getmaskstartstop_b", index_in.dtype, offsets_in.dtype, mask_out.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index_in, offsets_in, mask_out, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
    out["awkward_Content_getitem_next_missing_jagged_getmaskstartstop_a", int64, int64, int64, int64, int64] = None
    out["awkward_Content_getitem_next_missing_jagged_getmaskstartstop_b", int64, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'out', 'out', 'out', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_fill', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, False]
    out['awkward_IndexedArray_fill', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_fill', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, False]
    out['awkward_IndexedArray_fill', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_fill', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, False]
    out['awkward_IndexedArray_fill', int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_fill_count', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_IndexedArray_fill_count', int64] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_nextcarry_a", int64, int32] = None
    out["awkward_IndexedArray_flatten_nextcarry_b", int64, int32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_flatten_nextcarry', int64, int32] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_nextcarry_a", int64, int64] = None
    out["awkward_IndexedArray_flatten_nextcarry_b", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_flatten_nextcarry', int64, int64] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_nextcarry_a", int64, uint32] = None
    out["awkward_IndexedArray_flatten_nextcarry_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_flatten_nextcarry', int64, uint32] = f

    def f(grid, block, args):
        (outoffsets, outindex, outindexlength, offsets, offsetslength, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(outindexlength, dtype=cupy.int64)
        scan_in_array_outoffsets = cupy.zeros(outindexlength + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_a", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_outoffsets = cupy.cumsum(scan_in_array_outoffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_b", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_none2empty_a", int64, int32, int64] = None
    out["awkward_IndexedArray_flatten_none2empty_b", int64, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_flatten_none2empty', int64, int32, int64] = f

    def f(grid, block, args):
        (outoffsets, outindex, outindexlength, offsets, offsetslength, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(outindexlength, dtype=cupy.int64)
        scan_in_array_outoffsets = cupy.zeros(outindexlength + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_a", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_outoffsets = cupy.cumsum(scan_in_array_outoffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_b", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_none2empty_a", int64, int64, int64] = None
    out["awkward_IndexedArray_flatten_none2empty_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_flatten_none2empty', int64, int64, int64] = f

    def f(grid, block, args):
        (outoffsets, outindex, outindexlength, offsets, offsetslength, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(outindexlength, dtype=cupy.int64)
        scan_in_array_outoffsets = cupy.zeros(outindexlength + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_a", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_outoffsets = cupy.cumsum(scan_in_array_outoffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_flatten_none2empty_b", outoffsets.dtype, outindex.dtype, offsets.dtype]))(grid, block, (outoffsets, outindex, outindexlength, offsets, offsetslength, scan_in_array_k, scan_in_array_outoffsets, invocation_index, err_code))
    out["awkward_IndexedArray_flatten_none2empty_a", int64, uint32, int64] = None
    out["awkward_IndexedArray_flatten_none2empty_b", int64, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_flatten_none2empty', int64, uint32, int64] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_a", int64, int32] = None
    out["awkward_IndexedArray_getitem_nextcarry_b", int64, int32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry', int64, int32] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_a", int64, int64] = None
    out["awkward_IndexedArray_getitem_nextcarry_b", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry', int64, int64] = f

    def f(grid, block, args):
        (tocarry, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_a", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_b", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_a", int64, uint32] = None
    out["awkward_IndexedArray_getitem_nextcarry_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry', int64, uint32] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_a", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_b", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_outindex_a", int64, int32, int32] = None
    out["awkward_IndexedArray_getitem_nextcarry_outindex_b", int64, int32, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, int32, int32] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_a", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_b", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_outindex_a", int64, int64, int64] = None
    out["awkward_IndexedArray_getitem_nextcarry_outindex_b", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, int64, int64] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, lenindex, lencontent, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_a", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_getitem_nextcarry_outindex_b", tocarry.dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, lenindex, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_getitem_nextcarry_outindex_a", int64, uint32, uint32] = None
    out["awkward_IndexedArray_getitem_nextcarry_outindex_b", int64, uint32, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_IndexedArray_getitem_nextcarry_outindex', int64, uint32, uint32] = f

    def f(grid, block, args):
        (tocarry, starts, parents, parentslength, nextparents, nextlen, invocation_index, err_code) = args
        if nextlen < 1024:
            block_size = nextlen
        else:
            block_size = 1024
        if block_size > 0:
            grid_size1 = math.floor((nextlen + block_size - 1) / block_size)
            grid_size2 = math.floor((parentslength + block[0] - 1) / block[0])
        else:
            grid_size1, grid_size2 = 1, 1
        temp = cupy.zeros(nextlen, dtype=cupy.int64)
        scan_in_array_nextstarts = cupy.zeros(len(starts) + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_local_preparenext_64_a", tocarry.dtype, starts.dtype, parents.dtype, nextparents.dtype]))((grid_size1,), (block_size,), (tocarry, starts, parents, parentslength, nextparents, nextlen, temp, scan_in_array_nextstarts, len(starts), invocation_index, err_code))
        scan_in_array_nextstarts = cupy.cumsum(scan_in_array_nextstarts)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_local_preparenext_64_b", tocarry.dtype, starts.dtype, parents.dtype, nextparents.dtype]))((grid_size2,), block, (tocarry, starts, parents, parentslength, nextparents, nextlen, temp, scan_in_array_nextstarts, len(starts), invocation_index, err_code))
    out["awkward_IndexedArray_local_preparenext_64_a", int64, int64, int64, int64] = None
    out["awkward_IndexedArray_local_preparenext_64_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, False]
    out['awkward_IndexedArray_local_preparenext_64', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (numnull, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_a', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_b', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_a", int64, int32] = None
    out["awkward_IndexedArray_numnull_b", int64, int32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_numnull', int64, int32] = f

    def f(grid, block, args):
        (numnull, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_a', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_b', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_a", int64, int64] = None
    out["awkward_IndexedArray_numnull_b", int64, int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_numnull', int64, int64] = f

    def f(grid, block, args):
        (numnull, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_a', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_b', numnull.dtype, fromindex.dtype]))(grid, block, (numnull, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_a", int64, uint32] = None
    out["awkward_IndexedArray_numnull_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_numnull', int64, uint32] = f

    def f(grid, block, args):
        (numnull, tolength, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_a', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_b', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_parents_a", int64, int64, int32] = None
    out["awkward_IndexedArray_numnull_parents_b", int64, int64, int32] = None
    f.dir = ['out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_numnull_parents', int64, int64, int32] = f

    def f(grid, block, args):
        (numnull, tolength, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_a', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_b', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_parents_a", int64, int64, int64] = None
    out["awkward_IndexedArray_numnull_parents_b", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_numnull_parents', int64, int64, int64] = f

    def f(grid, block, args):
        (numnull, tolength, fromindex, lenindex, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_a', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_parents_b', numnull.dtype, tolength.dtype, fromindex.dtype]))(grid, block, (numnull, tolength, fromindex, lenindex, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_numnull_parents_a", int64, int64, uint32] = None
    out["awkward_IndexedArray_numnull_parents_b", int64, int64, uint32] = None
    f.dir = ['out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_numnull_parents', int64, int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_numnull_unique_64', int64]))(grid, block, args)
    f.dir = ['out', 'in']
    f.is_ptr = [True, False]
    out['awkward_IndexedArray_numnull_unique_64', int64] = f

    def f(grid, block, args):
        (toindex, fromindex, lenindex, parents, starts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_a", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_b", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_index_of_nulls_a", int64, int32, int64, int64] = None
    out["awkward_IndexedArray_index_of_nulls_b", int64, int32, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True]
    out['awkward_IndexedArray_index_of_nulls', int64, int32, int64, int64] = f

    def f(grid, block, args):
        (toindex, fromindex, lenindex, parents, starts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_a", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_b", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_index_of_nulls_a", int64, int64, int64, int64] = None
    out["awkward_IndexedArray_index_of_nulls_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True]
    out['awkward_IndexedArray_index_of_nulls', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (toindex, fromindex, lenindex, parents, starts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenindex, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_a", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_index_of_nulls_b", toindex.dtype, fromindex.dtype, parents.dtype, starts.dtype]))(grid, block, (toindex, fromindex, lenindex, parents, starts, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_index_of_nulls_a", int64, uint32, int64, int64] = None
    out["awkward_IndexedArray_index_of_nulls_b", int64, uint32, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True]
    out['awkward_IndexedArray_index_of_nulls', int64, uint32, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_overlay_mask', int64, int8, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_overlay_mask', int64, int8, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_overlay_mask', int64, int8, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_overlay_mask', int64, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_overlay_mask', int64, int8, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_IndexedArray_overlay_mask', int64, int8, uint32] = f

    def f(grid, block, args):
        (nextcarry, nextparents, outindex, index, parents, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_a", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_b", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_64_a", int64, int64, int64, int32, int64] = None
    out["awkward_IndexedArray_reduce_next_64_b", int64, int64, int64, int32, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, int32, int64] = f

    def f(grid, block, args):
        (nextcarry, nextparents, outindex, index, parents, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_a", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_b", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_64_a", int64, int64, int64, int64, int64] = None
    out["awkward_IndexedArray_reduce_next_64_b", int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (nextcarry, nextparents, outindex, index, parents, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_a", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_64_b", nextcarry.dtype, nextparents.dtype, outindex.dtype, index.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, outindex, index, parents, length, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_64_a", int64, int64, int64, uint32, int64] = None
    out["awkward_IndexedArray_reduce_next_64_b", int64, int64, int64, uint32, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_IndexedArray_reduce_next_64', int64, int64, int64, uint32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_reduce_next_fix_offsets_64', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_IndexedArray_reduce_next_fix_offsets_64', int64, int64] = f

    out['awkward_IndexedArray_unique_next_index_and_offsets_64', int64, int64, int64, int64] = None

    def f(grid, block, args):
        (nextshifts, index, length, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", int64, int32] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", int64, int32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, int32] = f

    def f(grid, block, args):
        (nextshifts, index, length, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", int64, int64] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", int64, int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, int64] = f

    def f(grid, block, args):
        (nextshifts, index, length, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", nextshifts.dtype, index.dtype]))(grid, block, (nextshifts, index, length, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_a", int64, uint32] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64', int64, uint32] = f

    def f(grid, block, args):
        (nextshifts, index, length, shifts, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", int64, int32, int64] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", int64, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int32, int64] = f

    def f(grid, block, args):
        (nextshifts, index, length, shifts, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", int64, int64, int64] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, int64, int64] = f

    def f(grid, block, args):
        (nextshifts, index, length, shifts, invocation_index, err_code) = args
        scan_in_array_k = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_nullsum = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_nullsum = cupy.cumsum(scan_in_array_nullsum)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", nextshifts.dtype, index.dtype, shifts.dtype]))(grid, block, (nextshifts, index, length, shifts, scan_in_array_k, scan_in_array_nullsum, invocation_index, err_code))
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_a", int64, uint32, int64] = None
    out["awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_b", int64, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64', int64, uint32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int32, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int32, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int32, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int32, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, uint32, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, uint32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, uint32, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, uint32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_simplify', int64, uint32, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_IndexedArray_simplify', int64, uint32, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_validity', int32]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_IndexedArray_validity', int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_validity', int64]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_IndexedArray_validity', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_IndexedArray_validity', uint32]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_IndexedArray_validity', uint32] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tostarts, tostops, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_next_64_a", int32, int64, int64, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_next_64_b", int32, int64, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    f.is_ptr = [True, True, True, False, True, True, True]
    out['awkward_IndexedArray_ranges_next_64', int32, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tostarts, tostops, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_next_64_a", int64, int64, int64, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_next_64_b", int64, int64, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    f.is_ptr = [True, True, True, False, True, True, True]
    out['awkward_IndexedArray_ranges_next_64', int64, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tostarts, tostops, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype, tolength.dtype]))(grid, block, (index, fromstarts, fromstops, length, tostarts, tostops, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_next_64_a", uint32, int64, int64, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_next_64_b", uint32, int64, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out', 'out', 'out']
    f.is_ptr = [True, True, True, False, True, True, True]
    out['awkward_IndexedArray_ranges_next_64', uint32, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tocarry, invocation_index, err_code) = args
        scan_in_array = cupy.zeros_like(index, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_carry_next_64_a", int32, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_carry_next_64_b", int32, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_IndexedArray_ranges_carry_next_64', int32, int64, int64, int64] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tocarry, invocation_index, err_code) = args
        scan_in_array = cupy.zeros_like(index, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_carry_next_64_a", int64, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_carry_next_64_b", int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_IndexedArray_ranges_carry_next_64', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, fromstarts, fromstops, length, tocarry, invocation_index, err_code) = args
        scan_in_array = cupy.zeros_like(index, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_a", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedArray_ranges_carry_next_64_b", index.dtype, fromstarts.dtype, fromstops.dtype, tocarry.dtype]))(grid, block, (index, fromstarts, fromstops, length, tocarry, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedArray_ranges_carry_next_64_a", uint32, int64, int64, int64] = None
    out["awkward_IndexedArray_ranges_carry_next_64_b", uint32, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_IndexedArray_ranges_carry_next_64', uint32, int64, int64, int64] = f

    def f(grid, block, args):
        (toindex, frommask, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_a", toindex.dtype, frommask.dtype]))(grid, block, (toindex, frommask, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_b", toindex.dtype, frommask.dtype]))(grid, block, (toindex, frommask, length, scan_in_array, invocation_index, err_code))
    out["awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_a", int64, int8] = None
    out["awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_b", int64, int8] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_IndexedOptionArray_rpad_and_clip_mask_axis1', int64, int8] = f

    def f(grid, block, args):
        (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, invocation_index, err_code) = args
        if offsetslength > 0:
            len_array = int(fromoffsets[offsetslength - 1])
        else:
            len_array = 0
        scan_in_array = cupy.zeros(len_array, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_a", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_b", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_broadcast_tooffsets_a", int64, int64, int32, int32] = None
    out["awkward_ListArray_broadcast_tooffsets_b", int64, int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True, False]
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, int32, int32] = f

    def f(grid, block, args):
        (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, invocation_index, err_code) = args
        if offsetslength > 0:
            len_array = int(fromoffsets[offsetslength - 1])
        else:
            len_array = 0
        scan_in_array = cupy.zeros(len_array, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_a", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_b", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_broadcast_tooffsets_a", int64, int64, int64, int64] = None
    out["awkward_ListArray_broadcast_tooffsets_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True, False]
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, invocation_index, err_code) = args
        if offsetslength > 0:
            len_array = int(fromoffsets[offsetslength - 1])
        else:
            len_array = 0
        scan_in_array = cupy.zeros(len_array, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_a", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_broadcast_tooffsets_b", tocarry.dtype, fromoffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_broadcast_tooffsets_a", int64, int64, uint32, uint32] = None
    out["awkward_ListArray_broadcast_tooffsets_b", int64, int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, True, False]
    out['awkward_ListArray_broadcast_tooffsets', int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_offsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_a", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))(grid, block, (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, invocation_index, err_code))
        scan_in_array_offsets = cupy.cumsum(scan_in_array_offsets)
        scan_in_array_parents = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        scan_in_array_local_indices = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        for i in range(1, length + 1):
            scan_in_array_parents[scan_in_array_offsets[i - 1]:scan_in_array_offsets[i]] = i - 1
        if int(scan_in_array_offsets[length]) < 1024:
            block_size = int(scan_in_array_offsets[length])
        else:
            block_size = 1024
        if block_size > 0:
            grid_size = math.floor((int(scan_in_array_offsets[length]) + block_size - 1) / block_size)
        else:
            grid_size = 1
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_b", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_c", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
    out["awkward_ListArray_combinations_a", int64, int64, int64, int32, int32] = None
    out["awkward_ListArray_combinations_b", int64, int64, int64, int32, int32] = None
    out["awkward_ListArray_combinations_c", int64, int64, int64, int32, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations', int64, int64, int64, int32, int32] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_offsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_a", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))(grid, block, (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, invocation_index, err_code))
        scan_in_array_offsets = cupy.cumsum(scan_in_array_offsets)
        scan_in_array_parents = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        scan_in_array_local_indices = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        for i in range(1, length + 1):
            scan_in_array_parents[scan_in_array_offsets[i - 1]:scan_in_array_offsets[i]] = i - 1
        if int(scan_in_array_offsets[length]) < 1024:
            block_size = int(scan_in_array_offsets[length])
        else:
            block_size = 1024
        if block_size > 0:
            grid_size = math.floor((int(scan_in_array_offsets[length]) + block_size - 1) / block_size)
        else:
            grid_size = 1
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_b", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_c", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
    out["awkward_ListArray_combinations_a", int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_combinations_b", int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_combinations_c", int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_offsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_a", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))(grid, block, (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, invocation_index, err_code))
        scan_in_array_offsets = cupy.cumsum(scan_in_array_offsets)
        scan_in_array_parents = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        scan_in_array_local_indices = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        for i in range(1, length + 1):
            scan_in_array_parents[scan_in_array_offsets[i - 1]:scan_in_array_offsets[i]] = i - 1
        if int(scan_in_array_offsets[length]) < 1024:
            block_size = int(scan_in_array_offsets[length])
        else:
            block_size = 1024
        if block_size > 0:
            grid_size = math.floor((int(scan_in_array_offsets[length]) + block_size - 1) / block_size)
        else:
            grid_size = 1
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_b", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_c", tocarry[0].dtype, toindex.dtype, fromindex.dtype, starts.dtype, stops.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, starts, stops, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
    out["awkward_ListArray_combinations_a", int64, int64, int64, uint32, uint32] = None
    out["awkward_ListArray_combinations_b", int64, int64, int64, uint32, uint32] = None
    out["awkward_ListArray_combinations_c", int64, int64, int64, uint32, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations', int64, int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (totallen, tooffsets, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_totallen = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_tooffsets = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_a", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_totallen = cupy.cumsum(scan_in_array_totallen)
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_b", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets,  invocation_index, err_code))
    out["awkward_ListArray_combinations_length_a", int64, int64, int32, int32] = None
    out["awkward_ListArray_combinations_length_b", int64, int64, int32, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations_length', int64, int64, int32, int32] = f

    def f(grid, block, args):
        (totallen, tooffsets, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_totallen = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_tooffsets = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_a", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_totallen = cupy.cumsum(scan_in_array_totallen)
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_b", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets,  invocation_index, err_code))
    out["awkward_ListArray_combinations_length_a", int64, int64, int64, int64] = None
    out["awkward_ListArray_combinations_length_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations_length', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (totallen, tooffsets, n, replacement, starts, stops, length, invocation_index, err_code) = args
        scan_in_array_totallen = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_tooffsets = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_a", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_totallen = cupy.cumsum(scan_in_array_totallen)
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_combinations_length_b", totallen.dtype, tooffsets.dtype, starts.dtype, stops.dtype]))(grid, block, (totallen, tooffsets, n, replacement, starts, stops, length, scan_in_array_totallen, scan_in_array_tooffsets,  invocation_index, err_code))
    out["awkward_ListArray_combinations_length_a", int64, int64, uint32, uint32] = None
    out["awkward_ListArray_combinations_length_b", int64, int64, uint32, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True, True, False]
    out['awkward_ListArray_combinations_length', int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (tooffsets, fromstarts, fromstops, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_a", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_b", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_compact_offsets_a", int64, int32, int32] = None
    out["awkward_ListArray_compact_offsets_b", int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_compact_offsets', int64, int32, int32] = f

    def f(grid, block, args):
        (tooffsets, fromstarts, fromstops, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_a", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_b", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_compact_offsets_a", int64, int64, int64] = None
    out["awkward_ListArray_compact_offsets_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_compact_offsets', int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, fromstarts, fromstops, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_a", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_compact_offsets_b", tooffsets.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, fromstarts, fromstops, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_compact_offsets_a", int64, uint32, uint32] = None
    out["awkward_ListArray_compact_offsets_b", int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_compact_offsets', int64, uint32, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_fill', int64, int64, int32, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, True, True, False, False]
    out['awkward_ListArray_fill', int64, int64, int32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_fill', int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, True, True, False, False]
    out['awkward_ListArray_fill', int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_fill', int64, int64, uint32, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, True, True, False, False]
    out['awkward_ListArray_fill', int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_a", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_b", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_apply_a", int64, int64, int64, int64, int64, int32, int32] = None
    out["awkward_ListArray_getitem_jagged_apply_b", int64, int64, int64, int64, int64, int32, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, True, False, True, True, False]
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, int32, int32] = f

    def f(grid, block, args):
        (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_a", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_b", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_apply_a", int64, int64, int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_getitem_jagged_apply_b", int64, int64, int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, True, False, True, True, False]
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_a", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_apply_b", tooffsets.dtype, tocarry.dtype, slicestarts.dtype, slicestops.dtype, sliceindex.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_apply_a", int64, int64, int64, int64, int64, uint32, uint32] = None
    out["awkward_ListArray_getitem_jagged_apply_b", int64, int64, int64, int64, int64, uint32, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, True, False, True, True, False]
    out['awkward_ListArray_getitem_jagged_apply', int64, int64, int64, int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (carrylen, slicestarts, slicestops, sliceouterlen, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_carrylen_a", carrylen.dtype, slicestarts.dtype, slicestops.dtype]))(grid, block, (carrylen, slicestarts, slicestops, sliceouterlen, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_carrylen_b", carrylen.dtype, slicestarts.dtype, slicestops.dtype]))(grid, block, (carrylen, slicestarts, slicestops, sliceouterlen, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_carrylen_a", int64, int64, int64] = None
    out["awkward_ListArray_getitem_jagged_carrylen_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_getitem_jagged_carrylen', int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_a", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_b", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_descend_a", int64, int64, int64, int32, int32] = None
    out["awkward_ListArray_getitem_jagged_descend_b", int64, int64, int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, True]
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, int32, int32] = f

    def f(grid, block, args):
        (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_a", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_b", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_descend_a", int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_getitem_jagged_descend_b", int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, True]
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(sliceouterlen, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_a", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_descend_b", tooffsets.dtype, slicestarts.dtype, slicestops.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_descend_a", int64, int64, int64, uint32, uint32] = None
    out["awkward_ListArray_getitem_jagged_descend_b", int64, int64, int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, True]
    out['awkward_ListArray_getitem_jagged_descend', int64, int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int32, int32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, uint32, uint32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_jagged_expand', int64, int64, int64, int64, uint32, uint32] = f

    def f(grid, block, args):
        (numvalid, slicestarts, slicestops, length, missing, missinglength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(missinglength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_numvalid_a", numvalid.dtype, slicestarts.dtype, slicestops.dtype, missing.dtype]))(grid, block, (numvalid, slicestarts, slicestops, length, missing, missinglength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_numvalid_b", numvalid.dtype, slicestarts.dtype, slicestops.dtype, missing.dtype]))(grid, block, (numvalid, slicestarts, slicestops, length, missing, missinglength, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_numvalid_a", int64, int64, int64, int64] = None
    out["awkward_ListArray_getitem_jagged_numvalid_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, False]
    out['awkward_ListArray_getitem_jagged_numvalid', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing, invocation_index, err_code) = args
        if length > 0 and length < int(slicestops[length - 1]):
            len_array = int(slicestops[length - 1])
        else:
            len_array = length
        scan_in_array_k = cupy.zeros(len_array, dtype=cupy.int64)
        scan_in_array_tosmalloffsets = cupy.zeros(length + 1, dtype=cupy.int64)
        scan_in_array_tolargeoffsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_shrink_a", tocarry.dtype, tosmalloffsets.dtype, tolargeoffsets.dtype, slicestarts.dtype, slicestops.dtype, missing.dtype]))(grid, block, (tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing, scan_in_array_k, scan_in_array_tosmalloffsets, scan_in_array_tolargeoffsets, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_tosmalloffsets = cupy.cumsum(scan_in_array_tosmalloffsets)
        scan_in_array_tolargeoffsets = cupy.cumsum(scan_in_array_tolargeoffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_jagged_shrink_b", tocarry.dtype, tosmalloffsets.dtype, tolargeoffsets.dtype, slicestarts.dtype, slicestops.dtype, missing.dtype]))(grid, block, (tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing, scan_in_array_k, scan_in_array_tosmalloffsets, scan_in_array_tolargeoffsets, invocation_index, err_code))
    out["awkward_ListArray_getitem_jagged_shrink_a", int64, int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_getitem_jagged_shrink_b", int64, int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, True]
    out['awkward_ListArray_getitem_jagged_shrink', int64, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array', int64, int64, int32, int32, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False, False]
    out['awkward_ListArray_getitem_next_array', int64, int64, int32, int32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array', int64, int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False, False]
    out['awkward_ListArray_getitem_next_array', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array', int64, int64, uint32, uint32, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False, False]
    out['awkward_ListArray_getitem_next_array', int64, int64, uint32, uint32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array_advanced', int64, int64, int32, int32, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, int32, int32, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array_advanced', int64, int64, int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_array_advanced', int64, int64, uint32, uint32, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False]
    out['awkward_ListArray_getitem_next_array_advanced', int64, int64, uint32, uint32, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_at', int64, int32, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_getitem_next_at', int64, int32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_at', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_getitem_next_at', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_at', int64, uint32, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_getitem_next_at', int64, uint32, uint32] = f

    def f(grid, block, args):
        (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_a", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_b", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_a", int32, int64, int32, int32] = None
    out["awkward_ListArray_getitem_next_range_b", int32, int64, int32, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range', int32, int64, int32, int32] = f

    def f(grid, block, args):
        (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_a", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_b", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_a", int64, int64, int64, int64] = None
    out["awkward_ListArray_getitem_next_range_b", int64, int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range', int64, int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_a", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_b", tooffsets.dtype, tocarry.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_a", uint32, int64, uint32, uint32] = None
    out["awkward_ListArray_getitem_next_range_b", uint32, int64, uint32, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range', uint32, int64, uint32, uint32] = f

    def f(grid, block, args):
        (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array_carrylength = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_a", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
        scan_in_array_carrylength = cupy.cumsum(scan_in_array_carrylength)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_b", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_carrylength_a", int64, int32, int32] = None
    out["awkward_ListArray_getitem_next_range_carrylength_b", int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range_carrylength', int64, int32, int32] = f

    def f(grid, block, args):
        (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array_carrylength = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_a", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
        scan_in_array_carrylength = cupy.cumsum(scan_in_array_carrylength)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_b", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_carrylength_a", int64, int64, int64] = None
    out["awkward_ListArray_getitem_next_range_carrylength_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range_carrylength', int64, int64, int64] = f

    def f(grid, block, args):
        (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, invocation_index, err_code) = args
        scan_in_array_carrylength = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_a", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
        scan_in_array_carrylength = cupy.cumsum(scan_in_array_carrylength)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_carrylength_b", carrylength.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (carrylength, fromstarts, fromstops, lenstarts, start, stop, step, scan_in_array_carrylength, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_carrylength_a", int64, uint32, uint32] = None
    out["awkward_ListArray_getitem_next_range_carrylength_b", int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False, False]
    out['awkward_ListArray_getitem_next_range_carrylength', int64, uint32, uint32] = f

    def f(grid, block, args):
        (total, fromoffsets, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_a", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_b", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_counts_a", int64, int32] = None
    out["awkward_ListArray_getitem_next_range_counts_b", int64, int32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_getitem_next_range_counts', int64, int32] = f

    def f(grid, block, args):
        (total, fromoffsets, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_a", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_b", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_counts_a", int64, int64] = None
    out["awkward_ListArray_getitem_next_range_counts_b", int64, int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_getitem_next_range_counts', int64, int64] = f

    def f(grid, block, args):
        (total, fromoffsets, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_a", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_getitem_next_range_counts_b", total.dtype, fromoffsets.dtype]))(grid, block, (total, fromoffsets, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_getitem_next_range_counts_a", int64, uint32] = None
    out["awkward_ListArray_getitem_next_range_counts_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_getitem_next_range_counts', int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_getitem_next_range_spreadadvanced', int64, int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_localindex', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_localindex', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_localindex', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_localindex', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_localindex', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListArray_localindex', int64, uint32] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.empty(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
        if lenstarts > 0:
            scan_in_array[0] = cupy.min(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_min_range_a", int64, int32, int32] = None
    out["awkward_ListArray_min_range_b", int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_min_range', int64, int32, int32] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.empty(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
        if lenstarts > 0:
            scan_in_array[0] = cupy.min(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_min_range_a", int64, int64, int64] = None
    out["awkward_ListArray_min_range_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_min_range', int64, int64, int64] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.empty(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
        if lenstarts > 0:
            scan_in_array[0] = cupy.min(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_min_range_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_min_range_a", int64, uint32, uint32] = None
    out["awkward_ListArray_min_range_b", int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListArray_min_range', int64, uint32, uint32] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, target, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_and_clip_length_axis1_a", int64, int32, int32] = None
    out["awkward_ListArray_rpad_and_clip_length_axis1_b", int64, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, int32, int32] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, target, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_and_clip_length_axis1_a", int64, int64, int64] = None
    out["awkward_ListArray_rpad_and_clip_length_axis1_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, int64, int64] = f

    def f(grid, block, args):
        (tomin, fromstarts, fromstops, target, lenstarts, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(lenstarts, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_a", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_and_clip_length_axis1_b", tomin.dtype, fromstarts.dtype, fromstops.dtype]))(grid, block, (tomin, fromstarts, fromstops, target, lenstarts, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_and_clip_length_axis1_a", int64, uint32, uint32] = None
    out["awkward_ListArray_rpad_and_clip_length_axis1_b", int64, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListArray_rpad_and_clip_length_axis1', int64, uint32, uint32] = f

    def f(grid, block, args):
        (toindex, fromstarts, fromstops, tostarts, tostops, target, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_a", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_b", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_axis1_a", int64, int32, int32, int32, int32] = None
    out["awkward_ListArray_rpad_axis1_b", int64, int32, int32, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False]
    out['awkward_ListArray_rpad_axis1', int64, int32, int32, int32, int32] = f

    def f(grid, block, args):
        (toindex, fromstarts, fromstops, tostarts, tostops, target, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_a", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_b", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_axis1_a", int64, int64, int64, int64, int64] = None
    out["awkward_ListArray_rpad_axis1_b", int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False]
    out['awkward_ListArray_rpad_axis1', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (toindex, fromstarts, fromstops, tostarts, tostops, target, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_a", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListArray_rpad_axis1_b", toindex.dtype, fromstarts.dtype, fromstops.dtype, tostarts.dtype, tostops.dtype]))(grid, block, (toindex, fromstarts, fromstops, tostarts, tostops, target, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListArray_rpad_axis1_a", int64, uint32, uint32, uint32, uint32] = None
    out["awkward_ListArray_rpad_axis1_b", int64, uint32, uint32, uint32, uint32] = None
    f.dir = ['out', 'in', 'in', 'out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, False]
    out['awkward_ListArray_rpad_axis1', int64, uint32, uint32, uint32, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_validity', int32, int32]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListArray_validity', int32, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_validity', int64, int64]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListArray_validity', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListArray_validity', uint32, uint32]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListArray_validity', uint32, uint32] = f

    def f(grid, block, args):
        (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length_offsets, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_drop_none_indexes_a", tooffsets.dtype, noneindexes.dtype, fromoffsets.dtype]))(grid, block, (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_drop_none_indexes_b", tooffsets.dtype, noneindexes.dtype, fromoffsets.dtype]))(grid, block, (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_drop_none_indexes_a", int32, int32, int32] = None
    out["awkward_ListOffsetArray_drop_none_indexes_b", int32, int32, int32] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListOffsetArray_drop_none_indexes', int32, int32, int32] = f

    def f(grid, block, args):
        (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length_offsets, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_drop_none_indexes_a", tooffsets.dtype, noneindexes.dtype, fromoffsets.dtype]))(grid, block, (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_drop_none_indexes_b", tooffsets.dtype, noneindexes.dtype, fromoffsets.dtype]))(grid, block, (tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_drop_none_indexes_a", int64, int64, int64] = None
    out["awkward_ListOffsetArray_drop_none_indexes_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListOffsetArray_drop_none_indexes', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_flatten_offsets', int64, int32, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_ListOffsetArray_flatten_offsets', int64, int32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_flatten_offsets', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_ListOffsetArray_flatten_offsets', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_flatten_offsets', int64, uint32, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True]
    out['awkward_ListOffsetArray_flatten_offsets', int64, uint32, int64] = f

    def f(grid, block, args):
        (tocarry, fromindex, length, invocation_index, err_code) = args
        scan_in_array = cupy.empty(length, dtype=cupy.int64)
        if length > 0:
            scan_in_array = cupy.argsort(fromindex)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_local_preparenext_64", tocarry.dtype, fromindex.dtype]))(grid, block, (tocarry, fromindex, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_local_preparenext_64", int64, int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_local_preparenext_64', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_reduce_local_nextparents_64', int64, uint32] = f

    def f(grid, block, args):
        (outoffsets, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=cupy.int64)
        scan_in_array = cupy.zeros(outlength, dtype=cupy.uint64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_local_outoffsets_64_a", cupy.dtype(outoffsets.dtype).type, parents.dtype]))((grid_size,), block, (outoffsets, parents, lenparents, outlength, scan_in_array, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_local_outoffsets_64_b", cupy.dtype(outoffsets.dtype).type, parents.dtype]))((grid_size,), block, (outoffsets, parents, lenparents, outlength, scan_in_array, temp, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_local_outoffsets_64_c", cupy.dtype(outoffsets.dtype).type, parents.dtype]))((grid_size,), block, (outoffsets, parents, lenparents, outlength, scan_in_array, temp, invocation_index, err_code))
    out["awkward_ListOffsetArray_reduce_local_outoffsets_64_a", int64, int64] = None
    out["awkward_ListOffsetArray_reduce_local_outoffsets_64_b", int64, int64] = None
    out["awkward_ListOffsetArray_reduce_local_outoffsets_64_c", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_reduce_local_outoffsets_64', int64, int64] = f

    def f(grid, block, args):
        (maxcount, offsetscopy, offsets, length, invocation_index, err_code) = args
        scan_in_array = cupy.empty(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_a", maxcount.dtype, offsetscopy.dtype, offsets.dtype]))(grid, block, (maxcount, offsetscopy, offsets, length, scan_in_array, invocation_index, err_code))
        if length > 0:
            scan_in_array[0] = cupy.max(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_b", maxcount.dtype, offsetscopy.dtype, offsets.dtype]))(grid, block, (maxcount, offsetscopy, offsets, length, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_a", int64, int64, int64] = None
    out["awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_b", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in']
    f.is_ptr = [True, True, True, False]
    out['awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64', int64, int64, int64] = f

    out['awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64', int64, int64, int64, int64, int64, int64, int64] = None

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64', int64, int64] = f

    def f(grid, block, args):
        (outstarts, outstops, distincts, lendistincts, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lendistincts + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lendistincts, dtype=cupy.int64)
        scan_in_array = cupy.zeros(outlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_a", outstarts.dtype, outstops.dtype, distincts.dtype]))((grid_size,), block, (outstarts, outstops, distincts, lendistincts, outlength, temp, scan_in_array, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_b", outstarts.dtype, outstops.dtype, distincts.dtype]))((grid_size,), block, (outstarts, outstops, distincts, lendistincts, outlength, temp, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_a", int64, int64, int64] = None
    out["awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_b", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64', int64, int64, int64] = f

    out['awkward_ListOffsetArray_reduce_nonlocal_preparenext_64', int64, int64, int64, int64, int64, int64, int64] = None

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_and_clip_axis1', int64, uint32] = f

    def f(grid, block, args):
        (toindex, fromoffsets, fromlength, target, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_a", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_b", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_axis1_a", int64, int32] = None
    out["awkward_ListOffsetArray_rpad_axis1_b", int64, int32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_axis1', int64, int32] = f

    def f(grid, block, args):
        (toindex, fromoffsets, fromlength, target, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_a", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_b", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_axis1_a", int64, int64] = None
    out["awkward_ListOffsetArray_rpad_axis1_b", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_axis1', int64, int64] = f

    def f(grid, block, args):
        (toindex, fromoffsets, fromlength, target, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_a", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_axis1_b", toindex.dtype, fromoffsets.dtype]))(grid, block, (toindex, fromoffsets, fromlength, target, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_axis1_a", int64, uint32] = None
    out["awkward_ListOffsetArray_rpad_axis1_b", int64, uint32] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_ListOffsetArray_rpad_axis1', int64, uint32] = f

    def f(grid, block, args):
        (tooffsets, fromoffsets, fromlength, target, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_a", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_b", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_length_axis1_a", int32, int32, int64] = None
    out["awkward_ListOffsetArray_rpad_length_axis1_b", int32, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_ListOffsetArray_rpad_length_axis1', int32, int32, int64] = f

    def f(grid, block, args):
        (tooffsets, fromoffsets, fromlength, target, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_a", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_b", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_length_axis1_a", int64, int64, int64] = None
    out["awkward_ListOffsetArray_rpad_length_axis1_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_ListOffsetArray_rpad_length_axis1', int64, int64, int64] = f

    def f(grid, block, args):
        (tooffsets, fromoffsets, fromlength, target, tolength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(fromlength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_a", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_ListOffsetArray_rpad_length_axis1_b", tooffsets.dtype, fromoffsets.dtype, tolength.dtype]))(grid, block, (tooffsets, fromoffsets, fromlength, target, tolength, scan_in_array, invocation_index, err_code))
    out["awkward_ListOffsetArray_rpad_length_axis1_a", uint32, uint32, int64] = None
    out["awkward_ListOffsetArray_rpad_length_axis1_b", uint32, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_ListOffsetArray_rpad_length_axis1', uint32, uint32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_toRegularArray', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_toRegularArray', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_toRegularArray', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_toRegularArray', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_ListOffsetArray_toRegularArray', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_ListOffsetArray_toRegularArray', int64, uint32] = f

    def f(grid, block, args):
        (index, starts_in, stops_in, starts_out, stops_out, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_a", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_b", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
    out["awkward_MaskedArray_getitem_next_jagged_project_a", int32, int64, int64, int64, int64] = None
    out["awkward_MaskedArray_getitem_next_jagged_project_b", int32, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_MaskedArray_getitem_next_jagged_project', int32, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, starts_in, stops_in, starts_out, stops_out, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_a", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_b", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
    out["awkward_MaskedArray_getitem_next_jagged_project_a", int64, int64, int64, int64, int64] = None
    out["awkward_MaskedArray_getitem_next_jagged_project_b", int64, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_MaskedArray_getitem_next_jagged_project', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (index, starts_in, stops_in, starts_out, stops_out, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_a", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_MaskedArray_getitem_next_jagged_project_b", index.dtype, starts_in.dtype, stops_in.dtype, starts_out.dtype, stops_out.dtype]))(grid, block, (index, starts_in, stops_in, starts_out, stops_out, length, scan_in_array, invocation_index, err_code))
    out["awkward_MaskedArray_getitem_next_jagged_project_a", uint32, int64, int64, int64, int64] = None
    out["awkward_MaskedArray_getitem_next_jagged_project_b", uint32, int64, int64, int64, int64] = None
    f.dir = ['in', 'in', 'in', 'out', 'out', 'in']
    f.is_ptr = [True, True, True, True, True, False]
    out['awkward_MaskedArray_getitem_next_jagged_project', uint32, int64, int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts, invocation_index, err_code) = args
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_rearrange_shifted_a", toptr.dtype, fromshifts.dtype, fromoffsets.dtype, fromparents.dtype, fromstarts.dtype]))(grid, block, (toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_rearrange_shifted_b", toptr.dtype, fromshifts.dtype, fromoffsets.dtype, fromparents.dtype, fromstarts.dtype]))(grid, block, (toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts, invocation_index, err_code))
    out["awkward_NumpyArray_rearrange_shifted_a", int64, int64, int64, int64, int64] = None
    out["awkward_NumpyArray_rearrange_shifted_b", int64, int64, int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False, True, True]
    out['awkward_NumpyArray_rearrange_shifted', int64, int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_NumpyArray_reduce_adjust_starts_64', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, True]
    out['awkward_NumpyArray_reduce_adjust_starts_64', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_NumpyArray_reduce_adjust_starts_shifts_64', int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, True, True]
    out['awkward_NumpyArray_reduce_adjust_starts_shifts_64', int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_NumpyArray_reduce_mask_ByteMaskedArray_64', int8, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_NumpyArray_reduce_mask_ByteMaskedArray_64', int8, int64] = f

    out['awkward_ListOffsetArray_argsort_strings', int64, int64, uint8, int64, int64] = None

    out['awkward_NumpyArray_sort_asstrings_uint8', uint8, uint8, int64, int64] = None

    out['awkward_NumpyArray_unique_strings', uint8, int64, int64, int64] = None

    out['awkward_NumpyArray_prepare_utf8_to_utf32_padded', uint8, int64, int64] = None

    out['awkward_NumpyArray_utf8_to_utf32_padded', uint8, int64, uint32] = None

    def f(grid, block, args):
        (fromptr, fromoffsets, offsetslength, target, toptr, invocation_index, err_code) = args
        diff = cupy.diff(fromoffsets)
        mask = diff > target
        scan_in_array = cupy.where(mask, diff, target)
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_pad_zero_to_length", fromptr.dtype, fromoffsets.dtype, toptr.dtype]))(grid, block, (fromptr, fromoffsets, offsetslength, target, toptr, scan_in_array, invocation_index, err_code))
    out["awkward_NumpyArray_pad_zero_to_length", uint8, int64, uint8] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_NumpyArray_pad_zero_to_length', uint8, int64, uint8] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.full((length - 1) * (length - 2), 0, dtype=cupy.int64)
        else:
            scan_in_array = cupy.full(0, 0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal_bool", bool_, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal_bool", bool_, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal_bool', bool_, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", int8, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', int8, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", int16, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', int16, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", int32, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', int32, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", int64, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', int64, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", uint8, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', uint8, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", uint16, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', uint16, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", uint32, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', uint32, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", uint64, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', uint64, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", float32, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', float32, int64, int64, bool_] = f

    def f(grid, block, args):
        (tmpptr, fromstarts, fromstops, length, toequal, invocation_index, err_code) = args
        if length > 1:
            scan_in_array = cupy.zeros((length - 1) * (length - 2), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(0, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_NumpyArray_subrange_equal", cupy.dtype(tmpptr.dtype).type, fromstarts.dtype, fromstops.dtype, bool_]))(grid, block, (tmpptr, fromstarts, fromstops, length, toequal, scan_in_array, invocation_index, err_code))
        toequal[0] = cupy.any(scan_in_array == True)
    out["awkward_NumpyArray_subrange_equal", float64, int64, int64, bool_] = None
    f.dir = ['in', 'in', 'in', 'in', 'out']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_NumpyArray_subrange_equal', float64, int64, int64, bool_] = f

    def f(grid, block, args):
        (outoffsets, outcarry, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=cupy.int64)
        scan_in_array = cupy.zeros(lenparents, dtype=cupy.int64)
        scan_in_array_outoffsets = cupy.zeros(outlength + 1, dtype=outoffsets.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RecordArray_reduce_nonlocal_outoffsets_64_a", outoffsets.dtype, outcarry.dtype, parents.dtype]))((grid_size,), block, (outoffsets, outcarry, parents, lenparents, outlength, temp, scan_in_array, scan_in_array_outoffsets, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RecordArray_reduce_nonlocal_outoffsets_64_b", outoffsets.dtype, outcarry.dtype, parents.dtype]))((grid_size,), block, (outoffsets, outcarry, parents, lenparents, outlength, temp, scan_in_array, scan_in_array_outoffsets, invocation_index, err_code))
        scan_in_array_outoffsets = cupy.cumsum(scan_in_array_outoffsets)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RecordArray_reduce_nonlocal_outoffsets_64_c", outoffsets.dtype, outcarry.dtype, parents.dtype]))((grid_size,), block, (outoffsets, outcarry, parents, lenparents, outlength, temp, scan_in_array, scan_in_array_outoffsets, invocation_index, err_code))
    out["awkward_RecordArray_reduce_nonlocal_outoffsets_64_a", int64, int64, int64] = None
    out["awkward_RecordArray_reduce_nonlocal_outoffsets_64_b", int64, int64, int64] = None
    out["awkward_RecordArray_reduce_nonlocal_outoffsets_64_c", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_RecordArray_reduce_nonlocal_outoffsets_64', int64, int64, int64] = f

    def f(grid, block, args):
        (tocarry, toindex, fromindex, n, replacement, size, length, invocation_index, err_code) = args
        scan_in_array_offsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RegularArray_combinations_64_a", tocarry[0].dtype, toindex.dtype, fromindex.dtype]))(grid, block, (tocarry, toindex, fromindex, n, replacement, size, length, scan_in_array_offsets, invocation_index, err_code))
        scan_in_array_offsets = cupy.cumsum(scan_in_array_offsets)
        scan_in_array_parents = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        scan_in_array_local_indices = cupy.zeros(int(scan_in_array_offsets[length]), dtype=cupy.int64)
        for i in range(1, length + 1):
            scan_in_array_parents[scan_in_array_offsets[i - 1]:scan_in_array_offsets[i]] = i - 1
        if int(scan_in_array_offsets[length]) < 1024:
            block_size = int(scan_in_array_offsets[length])
        else:
            block_size = 1024
        if block_size > 0:
            grid_size = math.floor((int(scan_in_array_offsets[length]) + block_size - 1) / block_size)
        else:
            grid_size = 1
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RegularArray_combinations_64_b", tocarry[0].dtype, toindex.dtype, fromindex.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, size, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_RegularArray_combinations_64_c", tocarry[0].dtype, toindex.dtype, fromindex.dtype]))((grid_size,), (block_size,), (tocarry, toindex, fromindex, n, replacement, size, length, scan_in_array_offsets, scan_in_array_parents, scan_in_array_local_indices, invocation_index, err_code))
    out["awkward_RegularArray_combinations_64_a", int64, int64, int64] = None
    out["awkward_RegularArray_combinations_64_b", int64, int64, int64] = None
    out["awkward_RegularArray_combinations_64_c", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False, False]
    out['awkward_RegularArray_combinations_64', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_carry', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_RegularArray_getitem_carry', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_jagged_expand', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_RegularArray_getitem_jagged_expand', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_array', int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_RegularArray_getitem_next_array', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_array_advanced', int64, int64, int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False]
    out['awkward_RegularArray_getitem_next_array_advanced', int64, int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_array_regularize', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_RegularArray_getitem_next_array_regularize', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_at', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_RegularArray_getitem_next_at', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_range', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False, False, False]
    out['awkward_RegularArray_getitem_next_range', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_getitem_next_range_spreadadvanced', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_RegularArray_getitem_next_range_spreadadvanced', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_localindex', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, False, False]
    out['awkward_RegularArray_localindex', int64] = f

    def f(grid, block, args):
        (nextparents, size, length, invocation_index, err_code) = args
        scan_in_array = cupy.ones(length * size, dtype=cupy.int64)
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_reduce_local_nextparents_64', nextparents.dtype]))(grid, block, (nextparents, size, length, scan_in_array, invocation_index, err_code))
    out["awkward_RegularArray_reduce_local_nextparents_64", int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, False, False]
    out['awkward_RegularArray_reduce_local_nextparents_64', int64] = f

    def f(grid, block, args):
        (nextcarry, nextparents, parents, size, length, invocation_index, err_code) = args
        scan_in_array = cupy.ones(length * size, dtype=cupy.int64)
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_reduce_nonlocal_preparenext_64', nextcarry.dtype, nextparents.dtype, parents.dtype]))(grid, block, (nextcarry, nextparents, parents, size, length, scan_in_array, invocation_index, err_code))
    out["awkward_RegularArray_reduce_nonlocal_preparenext_64", int64, int64, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_RegularArray_reduce_nonlocal_preparenext_64', int64, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_RegularArray_rpad_and_clip_axis1', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_RegularArray_rpad_and_clip_axis1', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillindex', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False]
    out['awkward_UnionArray_fillindex', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillindex', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False]
    out['awkward_UnionArray_fillindex', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillindex', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False]
    out['awkward_UnionArray_fillindex', int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillindex_count', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, False, False]
    out['awkward_UnionArray_fillindex_count', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillna', int64, int32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_UnionArray_fillna', int64, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillna', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_UnionArray_fillna', int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_fillna', int64, uint32]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_UnionArray_fillna', int64, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_filltags', int8, int8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False, False]
    out['awkward_UnionArray_filltags', int8, int8] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_filltags_const', int8]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, False, False]
    out['awkward_UnionArray_filltags_const', int8] = f

    def f(grid, block, args):
        (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array_tooffsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_a', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_b', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
    out["awkward_UnionArray_flatten_combine_a", int8, int64, int64, int8, int32, int64] = None
    out["awkward_UnionArray_flatten_combine_b", int8, int64, int64, int8, int32, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, True]
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, int32, int64] = f

    def f(grid, block, args):
        (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array_tooffsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_a', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_b', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
    out["awkward_UnionArray_flatten_combine_a", int8, int64, int64, int8, int64, int64] = None
    out["awkward_UnionArray_flatten_combine_b", int8, int64, int64, int8, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, True]
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, int64, int64] = f

    def f(grid, block, args):
        (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array_tooffsets = cupy.zeros(length + 1, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_a', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
        scan_in_array_tooffsets = cupy.cumsum(scan_in_array_tooffsets)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_combine_b', totags.dtype, toindex.dtype, tooffsets.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws, scan_in_array_tooffsets, invocation_index, err_code))
    out["awkward_UnionArray_flatten_combine_a", int8, int64, int64, int8, uint32, int64] = None
    out["awkward_UnionArray_flatten_combine_b", int8, int64, int64, int8, uint32, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, False, True]
    out['awkward_UnionArray_flatten_combine', int8, int64, int64, int8, uint32, int64] = f

    def f(grid, block, args):
        (total_length, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_a', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_b', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_flatten_length_a", int64, int8, int32, int64] = None
    out["awkward_UnionArray_flatten_length_b", int64, int8, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_UnionArray_flatten_length', int64, int8, int32, int64] = f

    def f(grid, block, args):
        (total_length, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_a', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_b', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_flatten_length_a", int64, int8, int64, int64] = None
    out["awkward_UnionArray_flatten_length_b", int64, int8, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_UnionArray_flatten_length', int64, int8, int64, int64] = f

    def f(grid, block, args):
        (total_length, fromtags, fromindex, length, offsetsraws, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_a', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_flatten_length_b', total_length.dtype, fromtags.dtype, fromindex.dtype, offsetsraws[0].dtype]))(grid, block, (total_length, fromtags, fromindex, length, offsetsraws, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_flatten_length_a", int64, int8, uint32, int64] = None
    out["awkward_UnionArray_flatten_length_b", int64, int8, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True]
    out['awkward_UnionArray_flatten_length', int64, int8, uint32, int64] = f

    def f(grid, block, args):
        (totags, toindex, tmpstarts, tag, fromcounts, length, invocation_index, err_code) = args
        if length > 0:
            scan_in_array = cupy.zeros(int(tmpstarts[length -1] + fromcounts[length - 1]), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_a", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_b", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_nestedfill_tags_index_a", int8, int32, int64, int64] = None
    out["awkward_UnionArray_nestedfill_tags_index_b", int8, int32, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, False]
    out['awkward_UnionArray_nestedfill_tags_index', int8, int32, int64, int64] = f

    def f(grid, block, args):
        (totags, toindex, tmpstarts, tag, fromcounts, length, invocation_index, err_code) = args
        if length > 0:
            scan_in_array = cupy.zeros(int(tmpstarts[length -1] + fromcounts[length - 1]), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_a", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_b", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_nestedfill_tags_index_a", int8, int64, int64, int64] = None
    out["awkward_UnionArray_nestedfill_tags_index_b", int8, int64, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, False]
    out['awkward_UnionArray_nestedfill_tags_index', int8, int64, int64, int64] = f

    def f(grid, block, args):
        (totags, toindex, tmpstarts, tag, fromcounts, length, invocation_index, err_code) = args
        if length > 0:
            scan_in_array = cupy.zeros(int(tmpstarts[length -1] + fromcounts[length - 1]), dtype=cupy.int64)
        else:
            scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_a", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_nestedfill_tags_index_b", totags.dtype, toindex.dtype, tmpstarts.dtype, fromcounts.dtype]))(grid, block, (totags, toindex, tmpstarts, tag, fromcounts, length, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_nestedfill_tags_index_a", int8, uint32, int64, int64] = None
    out["awkward_UnionArray_nestedfill_tags_index_b", int8, uint32, int64, int64] = None
    f.dir = ['out', 'out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, True, False]
    out['awkward_UnionArray_nestedfill_tags_index', int8, uint32, int64, int64] = f

    def f(grid, block, args):
        (lenout, tocarry, fromtags, fromindex, length, which, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_a", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_b", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_project_a", int64, int64, int8, int32] = None
    out["awkward_UnionArray_project_b", int64, int64, int8, int32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False]
    out['awkward_UnionArray_project', int64, int64, int8, int32] = f

    def f(grid, block, args):
        (lenout, tocarry, fromtags, fromindex, length, which, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_a", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_b", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_project_a", int64, int64, int8, int64] = None
    out["awkward_UnionArray_project_b", int64, int64, int8, int64] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False]
    out['awkward_UnionArray_project', int64, int64, int8, int64] = f

    def f(grid, block, args):
        (lenout, tocarry, fromtags, fromindex, length, which, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_a", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_project_b", lenout.dtype, tocarry.dtype, fromtags.dtype, fromindex.dtype]))(grid, block, (lenout, tocarry, fromtags, fromindex, length, which, scan_in_array, invocation_index, err_code))
    out["awkward_UnionArray_project_a", int64, int64, int8, uint32] = None
    out["awkward_UnionArray_project_b", int64, int64, int8, uint32] = None
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False]
    out['awkward_UnionArray_project', int64, int64, int8, uint32] = f

    def f(grid, block, args):
        (toindex, current, size, fromtags, length, invocation_index, err_code) = args
        atomicAdd_toptr = cupy.array(current, dtype=cupy.uint64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_a", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_b", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_c", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
    out["awkward_UnionArray_regular_index_a", int32, int32, int8] = None
    out["awkward_UnionArray_regular_index_b", int32, int32, int8] = None
    out["awkward_UnionArray_regular_index_c", int32, int32, int8] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_UnionArray_regular_index', int32, int32, int8] = f

    def f(grid, block, args):
        (toindex, current, size, fromtags, length, invocation_index, err_code) = args
        atomicAdd_toptr = cupy.array(current, dtype=cupy.uint64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_a", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_b", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_c", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
    out["awkward_UnionArray_regular_index_a", int64, int64, int8] = None
    out["awkward_UnionArray_regular_index_b", int64, int64, int8] = None
    out["awkward_UnionArray_regular_index_c", int64, int64, int8] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_UnionArray_regular_index', int64, int64, int8] = f

    def f(grid, block, args):
        (toindex, current, size, fromtags, length, invocation_index, err_code) = args
        atomicAdd_toptr = cupy.array(current, dtype=cupy.uint64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_a", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_b", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_c", toindex.dtype, current.dtype, fromtags.dtype]))(grid, block, (toindex, current, size, fromtags, length, atomicAdd_toptr, invocation_index, err_code))
    out["awkward_UnionArray_regular_index_a", uint32, uint32, int8] = None
    out["awkward_UnionArray_regular_index_b", uint32, uint32, int8] = None
    out["awkward_UnionArray_regular_index_c", uint32, uint32, int8] = None
    f.dir = ['out', 'out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, True, False]
    out['awkward_UnionArray_regular_index', uint32, uint32, int8] = f

    def f(grid, block, args):
        (size, fromtags, length, invocation_index, err_code) = args
        if length > 0:
            size[0] = 0 if cupy.all(fromtags < 0) else cupy.max(fromtags)
        else:
            size[0] = 0
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_UnionArray_regular_index_getsize", size.dtype, fromtags.dtype]))(grid, block, (size, fromtags, length, invocation_index, err_code))
    out["awkward_UnionArray_regular_index_getsize", int64, int8] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_UnionArray_regular_index_getsize', int64, int8] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, uint32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int32, int8, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, uint32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, int64, int8, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, uint32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, True, True, False, False, False, False, False]
    out['awkward_UnionArray_simplify', int8, int64, int8, uint32, int8, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify_one', int8, int64, int8, int32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_UnionArray_simplify_one', int8, int64, int8, int32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify_one', int8, int64, int8, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_UnionArray_simplify_one', int8, int64, int8, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_simplify_one', int8, int64, int8, uint32]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, True, False, False, False, False]
    out['awkward_UnionArray_simplify_one', int8, int64, int8, uint32] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_validity', int8, int32, int64]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_UnionArray_validity', int8, int32, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_validity', int8, int64, int64]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_UnionArray_validity', int8, int64, int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_UnionArray_validity', int8, uint32, int64]))(grid, block, args)
    f.dir = ['in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, True]
    out['awkward_UnionArray_validity', int8, uint32, int64] = f

    out['awkward_argsort', int64, bool_, int64] = None

    out['awkward_argsort', int64, int8, int64] = None

    out['awkward_argsort', int64, int16, int64] = None

    out['awkward_argsort', int64, int32, int64] = None

    out['awkward_argsort', int64, int64, int64] = None

    out['awkward_argsort', int64, uint8, int64] = None

    out['awkward_argsort', int64, uint16, int64] = None

    out['awkward_argsort', int64, uint32, int64] = None

    out['awkward_argsort', int64, uint64, int64] = None

    out['awkward_argsort', int64, float32, int64] = None

    out['awkward_argsort', int64, float64, int64] = None

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_index_rpad_and_clip_axis0', int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, False, False]
    out['awkward_index_rpad_and_clip_axis0', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_index_rpad_and_clip_axis1', int64, int64]))(grid, block, args)
    f.dir = ['out', 'out', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_index_rpad_and_clip_axis1', int64, int64] = f

    def f(grid, block, args):
        (toindex, length, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(length, dtype=cupy.int64)
        scan_in_array_n_non_null = cupy.zeros(length, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_Index_nones_as_index_a", toindex.dtype]))(grid, block, (toindex, length, scan_in_array, scan_in_array_n_non_null, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        scan_in_array_n_non_null = cupy.cumsum(scan_in_array_n_non_null)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_Index_nones_as_index_b", toindex.dtype]))(grid, block, (toindex, length, scan_in_array, scan_in_array_n_non_null, invocation_index, err_code))
    out["awkward_Index_nones_as_index_a", int64] = None
    out["awkward_Index_nones_as_index_b", int64] = None
    f.dir = ['out', 'in']
    f.is_ptr = [True, False]
    out['awkward_Index_nones_as_index', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_localindex', int64]))(grid, block, args)
    f.dir = ['out', 'in']
    f.is_ptr = [True, False]
    out['awkward_localindex', int64] = f

    def f(grid, block, args):
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_missing_repeat', int64, int64]))(grid, block, args)
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False, False]
    out['awkward_missing_repeat', int64, int64] = f

    out['awkward_reduce_argmax', int64, int8, int64] = None

    out['awkward_reduce_argmax', int64, int16, int64] = None

    out['awkward_reduce_argmax', int64, int32, int64] = None

    out['awkward_reduce_argmax', int64, int64, int64] = None

    out['awkward_reduce_argmax', int64, uint8, int64] = None

    out['awkward_reduce_argmax', int64, uint16, int64] = None

    out['awkward_reduce_argmax', int64, uint32, int64] = None

    out['awkward_reduce_argmax', int64, uint64, int64] = None

    out['awkward_reduce_argmax', int64, float32, int64] = None

    out['awkward_reduce_argmax', int64, float64, int64] = None

    out['awkward_reduce_argmax_complex', int64, float32, int64] = None

    out['awkward_reduce_argmax_complex', int64, float64, int64] = None

    out['awkward_reduce_argmin', int64, int8, int64] = None

    out['awkward_reduce_argmin', int64, int16, int64] = None

    out['awkward_reduce_argmin', int64, int32, int64] = None

    out['awkward_reduce_argmin', int64, int64, int64] = None

    out['awkward_reduce_argmin', int64, uint8, int64] = None

    out['awkward_reduce_argmin', int64, uint16, int64] = None

    out['awkward_reduce_argmin', int64, uint32, int64] = None

    out['awkward_reduce_argmin', int64, uint64, int64] = None

    out['awkward_reduce_argmin', int64, float32, int64] = None

    out['awkward_reduce_argmin', int64, float64, int64] = None

    out['awkward_reduce_argmin_complex', int64, float32, int64] = None

    out['awkward_reduce_argmin_complex', int64, float64, int64] = None

    def f(grid, block, args):
        (toptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_count_64_a", cupy.dtype(toptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_count_64_b", cupy.dtype(toptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_count_64_a", int64, int64] = None
    out["awkward_reduce_count_64_b", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, True, False, False]
    out['awkward_reduce_count_64', int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, bool_, int64] = None
    out["awkward_reduce_countnonzero_b", int64, bool_, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, bool_, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, int8, int64] = None
    out["awkward_reduce_countnonzero_b", int64, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, int16, int64] = None
    out["awkward_reduce_countnonzero_b", int64, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, int32, int64] = None
    out["awkward_reduce_countnonzero_b", int64, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, int64, int64] = None
    out["awkward_reduce_countnonzero_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, uint8, int64] = None
    out["awkward_reduce_countnonzero_b", int64, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, uint16, int64] = None
    out["awkward_reduce_countnonzero_b", int64, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, uint32, int64] = None
    out["awkward_reduce_countnonzero_b", int64, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, uint64, int64] = None
    out["awkward_reduce_countnonzero_b", int64, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, float32, int64] = None
    out["awkward_reduce_countnonzero_b", int64, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_a", int64, float64, int64] = None
    out["awkward_reduce_countnonzero_b", int64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero', int64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_complex_a", int64, float32, int64] = None
    out["awkward_reduce_countnonzero_complex_b", int64, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero_complex', int64, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_countnonzero_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_countnonzero_complex_a", int64, float64, int64] = None
    out["awkward_reduce_countnonzero_complex_b", int64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_countnonzero_complex', int64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", int8, int8, int64] = None
    out["awkward_reduce_max_b", int8, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', int8, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", int16, int16, int64] = None
    out["awkward_reduce_max_b", int16, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', int16, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", int32, int32, int64] = None
    out["awkward_reduce_max_b", int32, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', int32, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", int64, int64, int64] = None
    out["awkward_reduce_max_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", uint8, uint8, int64] = None
    out["awkward_reduce_max_b", uint8, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', uint8, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", uint16, uint16, int64] = None
    out["awkward_reduce_max_b", uint16, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', uint16, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", uint32, uint32, int64] = None
    out["awkward_reduce_max_b", uint32, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', uint32, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", uint64, uint64, int64] = None
    out["awkward_reduce_max_b", uint64, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', uint64, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", float32, float32, int64] = None
    out["awkward_reduce_max_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_a", float64, float64, int64] = None
    out["awkward_reduce_max_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([identity, 0], lenparents)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_complex_a", float32, float32, int64] = None
    out["awkward_reduce_max_complex_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max_complex', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([identity, 0], lenparents)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_max_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_max_complex_a", float64, float64, int64] = None
    out["awkward_reduce_max_complex_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_max_complex', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", int8, int8, int64] = None
    out["awkward_reduce_min_b", int8, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', int8, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", int16, int16, int64] = None
    out["awkward_reduce_min_b", int16, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', int16, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", int32, int32, int64] = None
    out["awkward_reduce_min_b", int32, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', int32, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", int64, int64, int64] = None
    out["awkward_reduce_min_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", uint8, uint8, int64] = None
    out["awkward_reduce_min_b", uint8, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', uint8, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", uint16, uint16, int64] = None
    out["awkward_reduce_min_b", uint16, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', uint16, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", uint32, uint32, int64] = None
    out["awkward_reduce_min_b", uint32, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', uint32, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", uint64, uint64, int64] = None
    out["awkward_reduce_min_b", uint64, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', uint64, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", float32, float32, int64] = None
    out["awkward_reduce_min_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.full(lenparents, identity, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_a", float64, float64, int64] = None
    out["awkward_reduce_min_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([identity, 0], lenparents)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_complex_a", float32, float32, int64] = None
    out["awkward_reduce_min_complex_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min_complex', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, identity, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([identity, 0], lenparents)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_min_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, toptr.dtype.type(identity), temp, invocation_index, err_code))
    out["awkward_reduce_min_complex_a", float64, float64, int64] = None
    out["awkward_reduce_min_complex_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False, False]
    out['awkward_reduce_min_complex', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int32, int8, int64] = None
    out["awkward_reduce_prod_b", int32, int8, int64] = None
    out["awkward_reduce_prod_c", int32, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int32, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int32, int16, int64] = None
    out["awkward_reduce_prod_b", int32, int16, int64] = None
    out["awkward_reduce_prod_c", int32, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int32, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int32, int32, int64] = None
    out["awkward_reduce_prod_b", int32, int32, int64] = None
    out["awkward_reduce_prod_c", int32, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int32, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int64, int8, int64] = None
    out["awkward_reduce_prod_b", int64, int8, int64] = None
    out["awkward_reduce_prod_c", int64, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int64, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int64, int16, int64] = None
    out["awkward_reduce_prod_b", int64, int16, int64] = None
    out["awkward_reduce_prod_c", int64, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int64, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int64, int32, int64] = None
    out["awkward_reduce_prod_b", int64, int32, int64] = None
    out["awkward_reduce_prod_c", int64, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int64, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", int64, int64, int64] = None
    out["awkward_reduce_prod_b", int64, int64, int64] = None
    out["awkward_reduce_prod_c", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint32, uint8, int64] = None
    out["awkward_reduce_prod_b", uint32, uint8, int64] = None
    out["awkward_reduce_prod_c", uint32, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint32, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint32, uint16, int64] = None
    out["awkward_reduce_prod_b", uint32, uint16, int64] = None
    out["awkward_reduce_prod_c", uint32, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint32, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint32, uint32, int64] = None
    out["awkward_reduce_prod_b", uint32, uint32, int64] = None
    out["awkward_reduce_prod_c", uint32, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint32, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint64, uint8, int64] = None
    out["awkward_reduce_prod_b", uint64, uint8, int64] = None
    out["awkward_reduce_prod_c", uint64, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint64, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint64, uint16, int64] = None
    out["awkward_reduce_prod_b", uint64, uint16, int64] = None
    out["awkward_reduce_prod_c", uint64, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint64, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint64, uint32, int64] = None
    out["awkward_reduce_prod_b", uint64, uint32, int64] = None
    out["awkward_reduce_prod_c", uint64, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint64, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", uint64, uint64, int64] = None
    out["awkward_reduce_prod_b", uint64, uint64, int64] = None
    out["awkward_reduce_prod_c", uint64, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', uint64, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", float32, float32, int64] = None
    out["awkward_reduce_prod_b", float32, float32, int64] = None
    out["awkward_reduce_prod_c", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=toptr.dtype)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_c", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_a", float64, float64, int64] = None
    out["awkward_reduce_prod_b", float64, float64, int64] = None
    out["awkward_reduce_prod_c", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([1, 0], lenparents)
        temp = temp.astype(cupy.dtype(toptr.dtype))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_prod_complex_a", float32, float32, int64] = None
    out["awkward_reduce_prod_complex_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_complex', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.tile([1, 0], lenparents)
        temp = temp.astype(cupy.dtype(toptr.dtype))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_prod_complex_a", float64, float64, int64] = None
    out["awkward_reduce_prod_complex_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_complex', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, bool_, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, bool_, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, bool_, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, bool_, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, int8, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, int8, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, int16, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, int16, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, int32, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, int32, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, int64, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, int64, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, uint8, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, uint8, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, uint16, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, uint16, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, uint32, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, uint32, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, uint64, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, uint64, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, float32, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, float32, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_a", bool_, float64, int64] = None
    out["awkward_reduce_prod_bool_b", bool_, float64, int64] = None
    out["awkward_reduce_prod_bool_c", bool_, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool', bool_, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_complex_a", bool_, float32, int64] = None
    out["awkward_reduce_prod_bool_complex_b", bool_, float32, int64] = None
    out["awkward_reduce_prod_bool_complex_c", bool_, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool_complex', bool_, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.ones(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_prod_bool_complex_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_prod_bool_complex_a", bool_, float64, int64] = None
    out["awkward_reduce_prod_bool_complex_b", bool_, float64, int64] = None
    out["awkward_reduce_prod_bool_complex_c", bool_, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_prod_bool_complex', bool_, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int32, int8, int64] = None
    out["awkward_reduce_sum_b", int32, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int32, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int32, int16, int64] = None
    out["awkward_reduce_sum_b", int32, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int32, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int32, int32, int64] = None
    out["awkward_reduce_sum_b", int32, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int32, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int64, int8, int64] = None
    out["awkward_reduce_sum_b", int64, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int64, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int64, int16, int64] = None
    out["awkward_reduce_sum_b", int64, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int64, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int64, int32, int64] = None
    out["awkward_reduce_sum_b", int64, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int64, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", int64, int64, int64] = None
    out["awkward_reduce_sum_b", int64, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', int64, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint32, uint8, int64] = None
    out["awkward_reduce_sum_b", uint32, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint32, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint32, uint16, int64] = None
    out["awkward_reduce_sum_b", uint32, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint32, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint32, uint32, int64] = None
    out["awkward_reduce_sum_b", uint32, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint32, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint64, uint8, int64] = None
    out["awkward_reduce_sum_b", uint64, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint64, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint64, uint16, int64] = None
    out["awkward_reduce_sum_b", uint64, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint64, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint64, uint32, int64] = None
    out["awkward_reduce_sum_b", uint64, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint64, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", uint64, uint64, int64] = None
    out["awkward_reduce_sum_b", uint64, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', uint64, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", float32, float32, int64] = None
    out["awkward_reduce_sum_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_a", float64, float64, int64] = None
    out["awkward_reduce_sum_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(2 * lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_complex_a", float32, float32, int64] = None
    out["awkward_reduce_sum_complex_b", float32, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_complex', float32, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(2 * lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_complex_a", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_complex_b", cupy.dtype(toptr.dtype).type, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_complex_a", float64, float64, int64] = None
    out["awkward_reduce_sum_complex_b", float64, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_complex', float64, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, bool_, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, bool_, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, bool_, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, bool_, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, int8, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, int8, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, int8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, int8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, int16, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, int16, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, int16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, int16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, int32, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, int32, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, int32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, int32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, int64, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, int64, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, int64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, uint8, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, uint8, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, uint8, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, uint8, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, uint16, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, uint16, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, uint16, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, uint16, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, uint32, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, uint32, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, uint32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, uint32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, uint64, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, uint64, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, uint64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, uint64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, float32, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, float32, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_a", bool_, float64, int64] = None
    out["awkward_reduce_sum_bool_b", bool_, float64, int64] = None
    out["awkward_reduce_sum_bool_c", bool_, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool', bool_, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_complex_a", bool_, float32, int64] = None
    out["awkward_reduce_sum_bool_complex_b", bool_, float32, int64] = None
    out["awkward_reduce_sum_bool_complex_c", bool_, float32, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool_complex', bool_, float32, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        atomic_toptr = cupy.array(toptr, dtype=cupy.uint32)
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_a", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_b", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_bool_complex_c", bool_, cupy.dtype(fromptr.dtype).type, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, atomic_toptr, temp, invocation_index, err_code))
    out["awkward_reduce_sum_bool_complex_a", bool_, float64, int64] = None
    out["awkward_reduce_sum_bool_complex_b", bool_, float64, int64] = None
    out["awkward_reduce_sum_bool_complex_c", bool_, float64, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_bool_complex', bool_, float64, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_int32_bool_64_a", int32, bool_, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_int32_bool_64_b", int32, bool_, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_int32_bool_64_a", int32, bool_, int64] = None
    out["awkward_reduce_sum_int32_bool_64_b", int32, bool_, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_int32_bool_64', int32, bool_, int64] = f

    def f(grid, block, args):
        (toptr, fromptr, parents, lenparents, outlength, invocation_index, err_code) = args
        if block[0] > 0:
            grid_size = math.floor((lenparents + block[0] - 1) / block[0])
        else:
            grid_size = 1
        temp = cupy.zeros(lenparents, dtype=toptr.dtype)
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_int64_bool_64_a", int64, bool_, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
        cuda_kernel_templates.get_function(fetch_specialization(["awkward_reduce_sum_int64_bool_64_b", int64, bool_, parents.dtype]))((grid_size,), block, (toptr, fromptr, parents, lenparents, outlength, temp, invocation_index, err_code))
    out["awkward_reduce_sum_int64_bool_64_a", int64, bool_, int64] = None
    out["awkward_reduce_sum_int64_bool_64_b", int64, bool_, int64] = None
    f.dir = ['out', 'in', 'in', 'in', 'in']
    f.is_ptr = [True, True, True, False, False]
    out['awkward_reduce_sum_int64_bool_64', int64, bool_, int64] = f

    out['awkward_sort', bool_, bool_, int64] = None

    out['awkward_sort', int8, int8, int64] = None

    out['awkward_sort', int16, int16, int64] = None

    out['awkward_sort', int32, int32, int64] = None

    out['awkward_sort', int64, int64, int64] = None

    out['awkward_sort', uint8, uint8, int64] = None

    out['awkward_sort', uint16, uint16, int64] = None

    out['awkward_sort', uint32, uint32, int64] = None

    out['awkward_sort', uint64, uint64, int64] = None

    out['awkward_sort', float32, float32, int64] = None

    out['awkward_sort', float64, float64, int64] = None

    out['awkward_unique_offsets', int8, int64, int64] = None

    out['awkward_unique_offsets', int16, int64, int64] = None

    out['awkward_unique_offsets', int32, int64, int64] = None

    out['awkward_unique_offsets', int64, int64, int64] = None

    out['awkward_unique_ranges_bool', bool_, int64, int64] = None

    out['awkward_unique_ranges', int8, int64, int64] = None

    out['awkward_unique_ranges', int16, int64, int64] = None

    out['awkward_unique_ranges', int32, int64, int64] = None

    out['awkward_unique_ranges', int64, int64, int64] = None

    out['awkward_unique_ranges', uint8, int64, int64] = None

    out['awkward_unique_ranges', uint16, int64, int64] = None

    out['awkward_unique_ranges', uint32, int64, int64] = None

    out['awkward_unique_ranges', uint64, int64, int64] = None

    out['awkward_unique_ranges', float32, int64, int64] = None

    out['awkward_unique_ranges', float64, int64, int64] = None

    def f(grid, block, args):
        (toindex, tolength, parents, parentslength, invocation_index, err_code) = args
        scan_in_array_k = cupy.ones(parentslength, dtype=cupy.int64)
        scan_in_array_j = cupy.zeros(parentslength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_sorting_ranges_a', toindex.dtype, parents.dtype]))(grid, block, (toindex, tolength, parents, parentslength, scan_in_array_k, scan_in_array_j, invocation_index, err_code))
        scan_in_array_k = cupy.cumsum(scan_in_array_k)
        scan_in_array_j = cupy.cumsum(scan_in_array_j)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_sorting_ranges_b', toindex.dtype, parents.dtype]))(grid, block, (toindex, tolength, parents, parentslength, scan_in_array_k, scan_in_array_j, invocation_index, err_code))
    out["awkward_sorting_ranges_a", int64, int64] = None
    out["awkward_sorting_ranges_b", int64, int64] = None
    f.dir = ['out', 'in', 'in', 'in']
    f.is_ptr = [True, False, True, False]
    out['awkward_sorting_ranges', int64, int64] = f

    def f(grid, block, args):
        (tolength, parents, parentslength, invocation_index, err_code) = args
        scan_in_array = cupy.zeros(parentslength, dtype=cupy.int64)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_sorting_ranges_length_a', tolength.dtype, parents.dtype]))(grid, block, (tolength, parents, parentslength, scan_in_array, invocation_index, err_code))
        scan_in_array = cupy.cumsum(scan_in_array)
        cuda_kernel_templates.get_function(fetch_specialization(['awkward_sorting_ranges_length_b', tolength.dtype, parents.dtype]))(grid, block, (tolength, parents, parentslength, scan_in_array, invocation_index, err_code))
    out["awkward_sorting_ranges_length_a", int64, int64] = None
    out["awkward_sorting_ranges_length_b", int64, int64] = None
    f.dir = ['out', 'in', 'in']
    f.is_ptr = [True, True, False]
    out['awkward_sorting_ranges_length', int64, int64] = f

    return out
