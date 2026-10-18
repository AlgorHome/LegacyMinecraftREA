// SPDX-License-Identifier: Apache-2.0
#pragma once
// Fail closed for manual builds as well as the packaging script.
#ifndef LFD_D00_ONLY
#define LFD_D00_ONLY 1
#endif
#if LFD_D00_ONLY != 0 && LFD_D00_ONLY != 1
#error LFD_D00_ONLY must be 0 or 1
#endif
