# Branches

Every feature lives on its own `feature/<name>` branch. A feature branch starts from WTP's `develop`
whenever possible, so it can also be offered to the We the People team. Some features build on others;
their branch then starts from those (or from a merge of them).

An arrow points from the branch a feature is built on to the feature.

```mermaid
flowchart LR
    develop(["develop<br/>(mirror of WTP)"])

    subgraph rules["Rules and balancing"]
        balancing_economy["balancing-economy"]
        balancing_natives["balancing-natives"]
        balancing_misc["balancing-misc"]
        balancing_transport["balancing_transport"]
        market_boom_event["market-boom-event"]
        bought_native_land_stays["bought-native-land-stays"]
        military_upkeep["military-upkeep"]
        independent_fixes["independent_fixes"]
        performance["performance"]
    end

    subgraph player["Player features"]
        trade_routes["trade-routes"]
        auto_market_imports["auto-market-imports"]
        patrol["patrol"]
        human_pioneer_plan["human-pioneer-plan"]
        forts_control_trade["forts-control-trade"]
    end

    subgraph aiGroup["AI and features built on it"]
        ai["ai"]
        forts_control_trade_ai["forts-control-trade-ai"]
        siege["siege-warfare_and_advanced-war-ai"]
        colonist_automation["colonist-automation"]
        treasure_automation["treasure-automation"]
        human_action_log["human-action-log"]
    end

    subgraph mapsArt["Maps and art"]
        maps["maps"]
        art_cities["art-cities-improvements"]
    end

    subgraph review["barra81's features (for now on wtp-based/*)"]
        ui_helpers["ui-helpers"]
        building_upgrade["building-upgrade"]
        nested_tooltip["nested-tooltip"]
        hud_message_panel["hud-message-panel"]
        import_export_window["import-export-window"]
        transfer_amount_window["transfer-amount-window"]
        qol_game_options["qol-and-game-options"]
        game_options_upkeep["game-options-upkeep"]
        trade_route_logic["trade-route-logic"]
        trade_route_manager["trade-route-manager"]
    end

    develop --> balancing_economy & balancing_natives & balancing_misc & balancing_transport
    develop --> market_boom_event & bought_native_land_stays & military_upkeep & independent_fixes & performance
    develop --> trade_routes & patrol & human_pioneer_plan & forts_control_trade
    develop --> ai & maps & art_cities
    develop --> ui_helpers & qol_game_options

    trade_routes --> auto_market_imports
    ai --> forts_control_trade_ai
    forts_control_trade --> forts_control_trade_ai
    ai --> siege & colonist_automation & treasure_automation & human_action_log

    ui_helpers --> building_upgrade & hud_message_panel & import_export_window & transfer_amount_window
    hud_message_panel --> nested_tooltip
    auto_market_imports -. "needed, not merged in yet" .-> import_export_window
    qol_game_options & military_upkeep --> game_options_upkeep

    ai & colonist_automation & performance & trade_routes & treasure_automation --> trade_route_logic
    trade_route_logic --> trade_route_manager

    classDef base fill:#ececec,stroke:#555,color:#000
    classDef pending stroke-dasharray: 5 5
    class develop base
    class ui_helpers,building_upgrade,nested_tooltip,hud_message_panel,import_export_window,transfer_amount_window,qol_game_options,game_options_upkeep,trade_route_logic,trade_route_manager pending
```

## Other branches

| Branch | Role |
|---|---|
| `develop` | unchanged mirror of WTP's `develop`; never commit to it |
| `main` | `develop` + all merged `feature/*` branches; the play and release branch (protected, changes only by pull request) |
| `test/all` | `main` + feature branches that are still being tested; rebuilt and force-pushed, never merged into `main`; do not base work on it |
| `wtp-based/<name>` | barra81's features, built on `develop`; to be renamed into the `feature/<name>` structure |
| `review/<name>` | the content of a pull request into `feature/<name>` (e.g. barra81's features); deleted after the merge |

## How a change gets in

1. New work goes on the matching `feature/<name>` branch, or on a new one started from `develop`
   (or from the feature it needs).
2. The feature branch is merged into `main`.
3. Fixes that are only needed when two features meet go on a branch of their own that merges both
   (like `forts-control-trade-ai`), not directly on `main`.
