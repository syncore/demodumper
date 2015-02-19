#include <Python.h>
#include "pyhuffman.h"
#include "qcommon.h"

#if PY_MAJOR_VERSION >= 3
    #define PyInt_FromLong PyLong_FromLong
#endif

PyDoc_STRVAR( huffman__doc__, "huffman" );
PyDoc_STRVAR( init__doc__, "init()" );
PyDoc_STRVAR( cleanup__doc__, "cleanup()" );
PyDoc_STRVAR( fill__doc__, "fill(count)" );
PyDoc_STRVAR( open__doc__, "open(file)" );
PyDoc_STRVAR( close__doc__, "close()" );
PyDoc_STRVAR( readrawlong__doc__, "readrawlong()" );
PyDoc_STRVAR( tell__doc__, "tell()" );
PyDoc_STRVAR( readbits__doc__, "readbits(count)" );
PyDoc_STRVAR( readbyte__doc__, "readbyte()" );
PyDoc_STRVAR( readshort__doc__, "readshort()" );
PyDoc_STRVAR( readlong__doc__, "readlong()" );
PyDoc_STRVAR( readstring__doc__, "readstring()" );
PyDoc_STRVAR( readbigstring__doc__, "readbigstring()" );
PyDoc_STRVAR( readfloat__doc__, "readfloat()" );

static huffman_t msgHuff;
static msg_t msg;
static FILE * file;
static byte data[ MAX_MSGLEN ];

static char stringBuf[ MAX_STRING_CHARS ];
static char bigStringBuf[ BIG_INFO_STRING ];

static int readBits( msg_t* msg, int bits ) {
    int value = 0;
    int nbits = 0;
    qboolean sign = qfalse;
    int b;
    int i;
    int get;

    if ( bits < 0 ) {
        bits = -bits;
        sign = qtrue;
    }

    if ( bits & 7 ) {
        nbits = bits & 7;

        for ( i = 0; i < nbits; ++i ) {
          b = Huff_getBit( msg->data, &msg->bit );
            value |= b << i;
        }

        bits = bits - nbits;
    }

    if ( bits ) {
        for ( i = 0; i < bits; i+= 8 ) {

            Huff_offsetReceive( msgHuff.decompressor.tree, &get, msg->data, &msg->bit );
            value |= ( get << ( i + nbits ) );
        }
    }

    msg->readcount = ( msg->bit >> 3 ) + 1;

    if ( sign ) {
        if ( value & ( 1 << ( bits - 1 ) ) ) {
            value |= -1 ^ ( ( 1 << bits ) - 1 );
        }
    }

    //printf( "%d %d %d\n", msg->bit, msg->readcount, value );
    return value;
}

static int readByte( msg_t* msg ) {
    int c = (unsigned char) readBits( msg, 8 );

    if ( msg->readcount > msg->cursize ) {
        c = -1;
    }
    return c;
}

static int readShort( msg_t* msg ) {
    int c = (short) readBits( msg, 16 );

    if ( msg->readcount > msg->cursize ) {
        c = -1;
    }

    return c;
}

static int readLong( msg_t* msg ) {
    int c =  readBits( msg, 32 );

    if ( msg->readcount > msg->cursize ) {
        c = -1;
    }

    return c;
}

static char* readString( msg_t* msg ) {
   size_t l;
    int c;

    l = 0;
    do {
        
        c = readByte( msg );        /* use ReadByte so -1 is out of bounds */
        if ( c == -1 || c == 0 ) {
            break;
        }
        /* translate all fmt spec to avoid crash bugs */
        if ( c == '%' ) {
            c = '.';
        }
        /* don't allow higher ascii values */
        if ( c > 127 ) {
            c = '.';
        }

        stringBuf[ l ] = c;
        l++;
    } while ( l < sizeof( stringBuf ) - 1 );

    stringBuf[ l ] = 0;

    return stringBuf;
}

static char* readFloat( msg_t* msg ) {
  int l;
  int c;
  
  for (l=0; l<4; l++) {    
    c = readByte( msg );        /* use ReadByte so -1 is out of bounds */
    stringBuf[ l ] = c;
  }
  return stringBuf;
}

static PyObject * py_readfloat( PyObject *self, PyObject *args ) {
  char* raw_float = readFloat(&msg);
  return PyFloat_FromDouble(_PyFloat_Unpack4(raw_float, 1));
}

static char* readBigString( msg_t* msg ) {
    size_t l;
    int c;

    l = 0;
    do {
        //printf( "l : %d\n", l );
        c = readByte( msg );        /* use ReadByte so -1 is out of bounds */
        if ( c == -1 || c == 0 ) {
            break;
        }
        /* translate all fmt spec to avoid crash bugs */
        if ( c == '%' ) {
            c = '.';
        }

        bigStringBuf[ l ] = c;
        l++;
    } while ( l < sizeof( bigStringBuf ) - 1 );

    bigStringBuf[ l ] = 0;
    //printf( "%d %s\n", l, bigStringBuf );
    return bigStringBuf;
}

static PyObject * py_init( PyObject *self, PyObject *args )
{
  int i, j;
  Huff_Init( &msgHuff );

  for( i = 0; i < 256; i++ ) 
    for( j = 0; j < msg_hData[ i ]; j++ ) 
      Huff_addRef( &msgHuff.decompressor, (byte) i );

  //data = ( byte *)malloc( sizeof( byte ) * MAX_MSGLEN );
  Py_INCREF(Py_True);
  return Py_True;
}

static PyObject * py_cleanup( PyObject *self, PyObject *args )
{
  //free( data );
  Py_INCREF(Py_True);
  return Py_True;
}

static PyObject * py_fill( PyObject *self, PyObject *args )
{
  int len = 0;
  int count = 0;

  if ( !PyArg_ParseTuple( args, "i", &len ) )
    return NULL;

  count = fread( &data, 1, len, file );
  //printf( "real read %d %d\n", count, len );

  msg.bit = 0;
  msg.data = data;
  msg.cursize = len;
  msg.maxsize = MAX_MSGLEN;
  msg.allowoverflow = qfalse;
  msg.oob = qfalse;
  msg.overflowed = qfalse;
  msg.readcount = 0;

  //printf( "ok\n" );

  Py_INCREF( Py_True );
  return Py_True;
}

static PyObject * py_open( PyObject *self, PyObject *args )
{
  char * f;

  if ( !PyArg_ParseTuple( args, "s", &f ) )
    return NULL;

  file = fopen( f, "rb" );
  if( file != NULL ) {
    Py_INCREF(Py_True);
    return Py_True;
  }
  Py_INCREF(Py_False);
  return Py_False;
}

static PyObject * py_close( PyObject *self, PyObject *args )
{
  if( file != NULL )
  {
    fclose( file );
    file = NULL;
    Py_INCREF(Py_True);
    return Py_True;
  }
  Py_INCREF(Py_False);
  return Py_False;
}

static PyObject * py_readrawlong( PyObject *self, PyObject *args )
{
  int lng;
  fread( &lng, sizeof( int ), 1, file );
  return PyInt_FromLong( ( long )lng );
}

static PyObject * py_readbits( PyObject *self, PyObject *args )
{
  int n = 0;
  if ( !PyArg_ParseTuple( args, "i", &n ) )
    return NULL;
  return PyInt_FromLong( ( long )readBits( &msg, n ) );
}

static PyObject * py_readbyte( PyObject *self, PyObject *args )
{
  return PyInt_FromLong( ( long )readByte( &msg ) );
}

static PyObject * py_readshort( PyObject *self, PyObject *args )
{
  return PyInt_FromLong( ( long )readShort( &msg ) );
}

static PyObject * py_readlong( PyObject *self, PyObject *args )
{
  return PyInt_FromLong( ( long )readLong( &msg ) );
}

static PyObject * py_readstring( PyObject *self, PyObject *args )
{
  //#if PY_MAJOR_VERSION >= 3
  char* bob = readString( &msg );
  return PyUnicode_DecodeLatin1(bob, strlen(bob), "strict" );
  //#else
  //return Py_BuildValue( "y", readString( &msg ));
  //#endif
}

static PyObject * py_readbigstring( PyObject *self, PyObject *args )
{
  //#if PY_MAJOR_VERSION >= 3
  char* bob = readString( &msg );
  return PyUnicode_DecodeLatin1(bob, strlen(bob), "strict" );
  //#else
  //return Py_BuildValue( "y", readBigString( &msg ));
  //#endif
}


static PyObject * py_tell( PyObject *self, PyObject *args )
{
  return PyInt_FromLong( ftell( file ) );
}

static PyMethodDef huffman_methods[] = {
  { "init",  py_init, METH_VARARGS, init__doc__ },
  { "fill",  py_fill, METH_VARARGS, fill__doc__ },
  { "cleanup",  py_cleanup, METH_VARARGS, cleanup__doc__ },
  { "open",  py_open, METH_VARARGS, open__doc__ },
  { "close",  py_close, METH_VARARGS, close__doc__ },
  { "readrawlong",  py_readrawlong, METH_VARARGS, readrawlong__doc__ },

  { "readbits",  py_readbits, METH_VARARGS, readbits__doc__ },
  { "readbyte",  py_readbyte, METH_VARARGS, readbyte__doc__ },
  { "readshort",  py_readshort, METH_VARARGS, readshort__doc__ },
  { "readlong",  py_readlong, METH_VARARGS, readlong__doc__ },
  { "readstring",  py_readstring, METH_VARARGS, readstring__doc__ },
  { "readbigstring",  py_readbigstring, METH_VARARGS, readbigstring__doc__ },
  { "readfloat",  py_readfloat, METH_VARARGS, readfloat__doc__ },

  { "tell",  py_tell, METH_VARARGS, tell__doc__ },
  { NULL, NULL }
};

#if PY_MAJOR_VERSION >=3
PyMODINIT_FUNC PyInit_huffman( void )
{
  PyObject *m;

  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "huffman",     /* m_name */
    huffman__doc__,  /* m_doc */
    -1,                  /* m_size */
    huffman_methods,    /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
  m = PyModule_Create(&moduledef);
  if (m == NULL)
    return NULL;
}
#else
PyMODINIT_FUNC inithuffman( void )
{
  Py_InitModule3( "huffman", huffman_methods, huffman__doc__ );
}
#endif
