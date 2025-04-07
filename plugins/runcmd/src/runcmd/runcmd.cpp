#include <stdio.h>
#include <windows.h>
#include <use_ansi.h>
#include "stdafx.h"
#include <string>

using namespace std;

int main(int argc, char* argv[])
{
  FILE *fp;
  string cmd;

  for( int count = 1; count < argc; count++ )
	cmd += " " + string(argv[count]);

  fp = _popen(cmd.c_str(), "r");

  if (fp != NULL) {
    char buffer[BUFSIZ];

    while (fgets(buffer, sizeof buffer, fp) != NULL)
      fputs(buffer, stdout);
  }

  return 0;
}
