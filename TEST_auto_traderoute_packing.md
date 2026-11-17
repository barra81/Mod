# Test: import limit / maintain level in "Import all" / "Auto export all"

Branch `test/auto-traderoute-packing`, based on the original mod (`We-the-People-civ4col-mod/Mod`, `develop` ea3b1aaf3).
Needs a DLL build. Nothing here is built or tested yet (written from reading the code).

## What is suspected

`CvCity::handleAutoTraderouteSetup` (buttons "Import all" / "Auto export all" of the transport route popup) packs the two levels of a good into one int
by hand: the maintain level in the lower, the import limit in the upper 16 bits.
The reader (`CvCity::doTask`, `TASK_YIELD_TRADEROUTE`) and the popup (`CvDLLButtonPopup::OnOkClicked`) use `NetworkDataTradeRouteInts`:
import limit in the lower, maintain level in the upper 16 bits. So both values should be swapped for every good that button touches.

## Commits

1. `10072f73a` log only, original behaviour. Expected: verdict SWAPPED for goods with different values.
2. `c781bfa3a` fix (packing with `NetworkDataTradeRouteInts`). Expected: verdict OK.

## Test

1. Build the DLL of commit 1. New game or a save of the original mod, a city with a few goods.
2. Open the transport route popup of the city. For one or two goods set an import limit (e.g. 50) and a maintain level (e.g. 100), different values. OK.
3. Open the popup again, press "Import all" (then the same with "Auto export all"). Open it once more and write down the values of the goods.
4. Read `WTP_TradeRoutePacking.log` (the log folder of the game; the file only appears if logging is on, probably LoggingEnabled = 1 in the ini).
5. Repeat 1 to 4 with the DLL of commit 2.

## Result (to fill in)

| commit | button | good | before (limit / maintain) | after (limit / maintain) | log verdict |
|---|---|---|---|---|---|
| 10072f73a | Import all | yield 3 and 4 | 50 / 100 | 100 / 50 | SWAPPED |
| 10072f73a | Auto export all | yield 3 and 4 | 100 / 50 (state after the first button) | 50 / 100 | SWAPPED |
| c781bfa3a | Import all | | | | |
| c781bfa3a | Auto export all | | | | |

Commit 1 (21 Nov 2026 test run, city Jamestown, new game): confirmed. The popup showed the same swap as the log: after "Import all" the two goods
went from 50 / 100 to 100 / 50, after "Auto export all" back to 50 / 100. All other goods (0 / 0) are unaffected, as expected.
Commit 2 (fix): still to be tested.
