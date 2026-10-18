# Message-dialog static initialization review — no source changes

Reviewed exact approved source a3f72874241914f6048d4ca9ec4fc0edc978625d,
diagnostics/NativeCapabilities/src/app.cpp. No additional native test or target
execution occurred. This review does not establish Xbox dialog compatibility.

## Ordering and isolation

MTA wWinMain calls CoreApplication::Run(Source). The runtime creates the view/UI
apartment; Initialize registers activation and SetWindow supplies CoreWindow.
Activation first calls window_.Activate(), then enforces start-once and rejects
unsupported activation/case arguments. Valid activation enters Start().

Start constructs Receipt (identity, package hashes and directory), writes STARTED
synchronously, arms the deadline, then creates independent observer/probe MTA
workers. The normal path does not create MessageDialog before those operations.
Worker/observer notify posts a callback through CoreDispatcher::RunAsync to the
UI thread; Show constructs MessageDialog and stores its ShowAsync operation.
This respects the non-agile dialog's UI-thread ownership. The retained operation
keeps the async handle available but does not inspect its eventual error.

No app-owned swapchain/renderer/presentation or retry action is added. Default
dialog dismissal has no test callback. CoreWindow dispatcher continues processing
events; dismissal does not start another case or terminate another process.

## Ranked risks and limitations

1. **Startup I/O can interfere with activation responsiveness.** Receipt creation
   hashes files and STARTED writes/flushed storage synchronously on the activation
   UI callback, before deadline observer launch. Slow/stuck I/O can delay activation
   and leave no final receipt; the ten-second case deadline does not bound that
   earlier path. No change or timeout/cancellation guarantee is inferred.
2. **Exact Xbox MessageDialog availability is untested.** Microsoft documents a
   public UniversalApiContract/non-XAML use case, not successful display on this
   owner console/build. Modal presentation, truncation, controller dismissal and
   display timing remain NOT EXECUTED. App classification is an owner installation
   setting, not proved by manifest or a dialog API call.
3. **Asynchronous dialog/dispatcher errors may be silent.** Show catches synchronous
   constructor/ShowAsync errors and attempts an ApplicationView title. Later
   ShowAsync errors have no Completed/GetResults handler, and RunAsync completion
   is not observed. Failure to schedule after notified=true suppresses further UI
   attempts. Thus a blank UI can coexist with a valid hardware receipt; no UI error
   log is guaranteed. This is a reporting limitation, not a reason to auto-retry.
4. **UI notification is separate from persistence.** In the normal completed path,
   worker returns after terminal persistence settles, or observer waits for it up
   to deadline. If storage remains pending at deadline, dialog may show an in-memory
   decision plus NOT CONFIRMED/IO_PENDING. A displayed PASS with unconfirmed storage
   is not formal acceptance. Downloaded final receipt must be validated separately.
5. **Exceptional/rejected startup paths may show a dialog earlier.** Unknown case,
   receipt initialization failure or thread-construction exception may call Show
   directly from the activation UI callback. This can affect owner-visible startup,
   but unknown dispatch still creates no GPU worker. A worker already started on
   an exceptional path can later produce its own notification; modal contention
   could suppress it. No second case is scheduled and no evidence is fabricated.
6. **UI process failure can end the run.** Queuing after a case decision reduces
   dependencies but cannot guarantee process survival through a platform UI fault.
   Existing committed checkpoint/terminal files should be preserved; absence of
   visible status never establishes the app did not enter the native path.

No confirmed source defect that prevents the authorized fresh-copy signing was
established. These risks must remain explicit in any future single-run approval.
No source fix, rebuild, logging change, extra capability or native test is included.

Microsoft references reviewed:
[MessageDialog](https://learn.microsoft.com/en-us/uwp/api/windows.ui.popups.messagedialog?view=winrt-26100),
[CoreDispatcher.RunAsync](https://learn.microsoft.com/en-us/uwp/api/windows.ui.core.coredispatcher.runasync?view=winrt-26100).
