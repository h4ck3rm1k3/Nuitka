#     Copyright 2013, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Templates for the constants handling.

"""

template_constants_reading = """
#include "nuitka/prelude.hpp"

// Sentinel PyObject to be used for all our call iterator endings. It will become
// a PyCObject pointing to NULL. It's address is unique, and that's enough.
PyObject *_sentinel_value = NULL;

%(constant_declarations)s

static void __initConstants( void )
{
    if ( %(needs_pickle)s )
    {
        UNSTREAM_INIT();
    }

%(constant_inits)s
}

void _initConstants( void )
{
    if ( _sentinel_value == NULL )
    {
#if PYTHON_VERSION < 300
        _sentinel_value = PyCObject_FromVoidPtr( NULL, NULL );
#else
        // The NULL value is not allowed for a capsule, so use something else.
        _sentinel_value = PyCapsule_New( (void *)27, "sentinel", NULL );
#endif
        assert( _sentinel_value );

        __initConstants();
    }
}
"""

template_constants_declaration = """\
// Call this to initialize all of the below
void _initConstants( void );

%(constant_declarations)s
"""
