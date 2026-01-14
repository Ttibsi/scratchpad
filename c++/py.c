// requirements: python3-devel
// gcc -ggdb -Wall py.c -o t $(python3.13-config --cflags --ldflags --embed)

#include <stdio.h>
#include <Python.h>

// Define my function
static PyObject* py_double(PyObject* self, PyObject* args) {
    long val;

    // parameters are always passed as a tuple, irregardless of length
    // Parse the first element into val as a long
    if (!PyArg_ParseTuple(args, "l", &val)) {
        fprintf(stderr, "failed to parse");
        return NULL;
    }

    return PyLong_FromLong(val * 2);
}

static PyMethodDef my_module_methods[] = {
    {"doubleNum", py_double, METH_VARARGS, "Double the provided num"},
    {NULL, NULL, 0, NULL}
};

# define module for my function to exist in
static struct PyModuleDef emb_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "mytest",
    .m_size = 0,
    .m_methods = my_module_methods
};

static PyObject* PyInit_myMod(void) { return PyModuleDef_Init(&emb_module); }

const char* src = "import mytest\n"
    "num = mytest.doubleNum(5)\n"
    "print(f\"Hello from python!: {num}\")\n"
    "print(type(num))";

int main(int argc, char* argv[]) {
    PyStatus status = PyStatus_Ok();
    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    PyImport_AppendInittab("mytest", &PyInit_myMod);

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        fprintf(stderr, "Exception thrown....");
        return 1;
    }
    PyConfig_Clear(&config);

    PyRun_SimpleString(src);
    if (Py_FinalizeEx() < 0) {
        exit(120);
    }

    PyConfig_Clear(&config);
    return 0;
}
