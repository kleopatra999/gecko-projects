/* -*- Mode: C++; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

#include "updaterfileutils_osx.h"

#include <Cocoa/Cocoa.h>
#include <pwd.h>

bool IsRecursivelyWritable(const char* aPath)
{
  NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];

  NSString* rootPath = [NSString stringWithUTF8String:aPath];
  NSFileManager* fileManager = [NSFileManager defaultManager];
  NSError* error = nil;
  NSArray* subPaths =
    [fileManager subpathsOfDirectoryAtPath:rootPath
                                     error:&error];
  NSMutableArray* paths =
    [NSMutableArray arrayWithCapacity:[subPaths count] + 1];
  [paths addObject:@""];
  [paths addObjectsFromArray:subPaths];

  if (error) {
    [pool drain];
    return false;
  }

  for (NSString* currPath in paths) {
    NSString* child = [rootPath stringByAppendingPathComponent:currPath];
    NSDictionary* attributes =
      [fileManager attributesOfItemAtPath:child
                                    error:&error];
    if (error) {
      [pool drain];
      return false;
    }
    NSNumber* accountID =
      (NSNumber*)[attributes valueForKey:NSFileOwnerAccountID];
    NSNumber* groupID =
      (NSNumber*)[attributes valueForKey:NSFileGroupOwnerAccountID];
    NSNumber* permissions =
      (NSNumber*)[attributes valueForKey:NSFilePosixPermissions];
    int perms = [permissions shortValue];
    // Check if the user has write access to the file. This is the case when
    // the user is the owner of the file and the owner has write access, or if
    // the user belongs to a group that has write access to the file (typically
    // "admin").
    if (!((unsigned int)[accountID shortValue] == getuid() && (perms & 0x80)) &&
        !((unsigned int)[groupID shortValue] == (getpwuid(getuid()))->pw_gid &&
            (perms & 0x10))) {
      [pool drain];
      return false;
    }
  }

  [pool drain];
  return true;
}
