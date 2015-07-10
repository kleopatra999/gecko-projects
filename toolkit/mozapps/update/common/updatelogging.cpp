/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#if defined(XP_WIN)
#include <windows.h>
#endif


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>

#include "updatelogging.h"

UpdateLog::UpdateLog() : logFP(nullptr)
{
}

void UpdateLog::Init(NS_tchar* sourcePath, const NS_tchar* fileName)
{
  if (logFP) {
    return;
  }

  NS_tsnprintf(mDstFilePath, sizeof(mDstFilePath)/sizeof(mDstFilePath[0]),
               NS_T("%s/%s"), sourcePath, fileName);
  // If there is a pre-existing file it is renamed by adding .bak to the file
  // name instead of overwriting it. If there is already a file with that name
  // that file is removed first.
  if (!NS_taccess(mDstFilePath, F_OK)) {
    NS_tchar bakFilePath[MAXPATHLEN];
    NS_tsnprintf(bakFilePath, sizeof(bakFilePath)/sizeof(bakFilePath[0]),
                 NS_T("%s/%s.bak"), sourcePath, fileName);
    NS_tremove(bakFilePath);
    NS_trename(mDstFilePath, bakFilePath);
  }
#if defined(XP_WIN)
  GetTempFileNameW(sourcePath, L"log", 0, mTmpFilePath);
  logFP = NS_tfopen(mTmpFilePath, NS_T("w"));
  // Delete this file now so it is possible to tell from the unelevated
  // updater process if the elevated updater process has written the log.
  NS_tremove(mDstFilePath);
#elif defined(XP_UNIX) && !defined(XP_MACOSX) && !defined(MOZ_WIDGET_GONK)
  // On Linux an in memory file is used and written to the destination file when
  // the logging is finished since the update.log file is located in the
  // application directory and the application directory is renamed when a
  // staged update renames the application directory. After Linux uses an
  // updates directory outside of the application directory this can use fopen
  // just as Mac and Gonk uses.
  size_t len;
  logFP = open_memstream(&logBuf, &len);
#else
  logFP = NS_tfopen(mDstFilePath, NS_T("w"));
#endif
}

void UpdateLog::Finish()
{
  if (!logFP) {
    return;
  }

  fclose(logFP);
  logFP = nullptr;

#if defined(XP_WIN)
  // When the log file already exists then the elevated updater has already
  // written the log file and the temp file for the log should be discarded.
  if (!NS_taccess(mDstFilePath, F_OK)) {
    DeleteFileW(mTmpFilePath);
  } else {
    MoveFileExW(mTmpFilePath, mDstFilePath, MOVEFILE_REPLACE_EXISTING);
  }
#endif

#if defined(XP_UNIX) && !defined(XP_MACOSX) && !defined(MOZ_WIDGET_GONK)
  if (logBuf) {
    logFP = NS_tfopen(mDstFilePath, NS_T("w"));
    fprintf(logFP, logBuf);
    free(logBuf);
    fclose(logFP);
    logFP = nullptr;
  }
#endif
}

void UpdateLog::Flush()
{
  if (!logFP) {
    return;
  }

  fflush(logFP);
}

void UpdateLog::Printf(const char *fmt, ... )
{
  if (!logFP) {
    return;
  }

  va_list ap;
  va_start(ap, fmt);
  vfprintf(logFP, fmt, ap);
  fprintf(logFP, "\n");
  va_end(ap);
}

void UpdateLog::WarnPrintf(const char *fmt, ... )
{
  if (!logFP) {
    return;
  }

  va_list ap;
  va_start(ap, fmt);
  fprintf(logFP, "*** Warning: ");
  vfprintf(logFP, fmt, ap);
  fprintf(logFP, "***\n");
  va_end(ap);
}
