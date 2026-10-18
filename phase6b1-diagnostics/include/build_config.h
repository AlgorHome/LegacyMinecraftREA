// SPDX-License-Identifier: Apache-2.0
#pragma once
#ifndef LFN_NATIVE_ONLY
#define LFN_NATIVE_ONLY 1
#endif
#ifndef LFN_JNI_ENABLED
#define LFN_JNI_ENABLED 0
#endif
#ifndef LFD_D00_ONLY
#define LFD_D00_ONLY 1
#endif
#ifndef LFN_CASE_D06_SRV03
#define LFN_CASE_D06_SRV03 1
#endif
#if defined(LFN_CASE_D06_HW01) || defined(LFN_CASE_D06_FMT01) || defined(LFN_CASE_D06_RES01A) || defined(LFN_CASE_D06_SRV01) || defined(LFN_CASE_D06_SRV02)
#error The accepted HW01/FMT01/RES01a/SRV01/SRV02 cases are excluded from this SRV03 build
#endif
#if LFN_NATIVE_ONLY != 1 || LFN_JNI_ENABLED != 0 || LFD_D00_ONLY != 1 || LFN_CASE_D06_SRV03 != 1
#error This project permits only native D06-SRV03; Java and additional cases are forbidden
#endif
