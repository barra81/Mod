/* tiny host: runs the game's python24.dll as a console interpreter (Py_Main) */
#include <windows.h>
#include <stdio.h>
typedef int (*PyMainFn)(int, char **);
typedef void (*SetHomeFn)(char *);
int main(int argc, char **argv)
{
	HMODULE h = LoadLibraryA("python24.dll");
	PyMainFn pm;
	if (!h) { printf("cannot load python24.dll (%lu)\n", GetLastError()); return 1; }
	pm = (PyMainFn)GetProcAddress(h, "Py_Main");
	if (!pm) { printf("no Py_Main\n"); return 1; }
	return pm(argc, argv);
}
