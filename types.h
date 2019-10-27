//
// Created by karl on 2019/10/27.
//

#ifndef FFS_TYPES_H
#define FFS_TYPES_H

#include <stdint.h>
#include <stdatomic.h>
#include <limits.h>

typedef uint_fast8_t _u8;
typedef uint_fast16_t _u16;
typedef uint_fast32_t _u32;
typedef uint_fast64_t _u64;

typedef int_fast8_t _i8;
typedef int_fast16_t _i16;
typedef int_fast32_t _i32;
typedef int_fast64_t _i64;

typedef atomic_uint_fast8_t _au8;
typedef atomic_uint_fast16_t _au16;
typedef atomic_uint_fast32_t _au32;
typedef atomic_uint_fast64_t _au64;

typedef atomic_int_fast8_t _ai8;
typedef atomic_int_fast16_t _ai16;
typedef atomic_int_fast32_t _ai32;
typedef atomic_int_fast64_t _ai64;

typedef char _c;
typedef atomic_char _ac;

typedef char _s[];

typedef _u8 _b;
typedef _au8 _ab;

#endif //FFS_TYPES_H
