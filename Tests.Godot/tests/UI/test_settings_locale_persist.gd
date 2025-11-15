extends "res://addons/gdUnit4/src/GdUnitTestSuite.gd"

func _new_db(name: String) -> Node:
    var db = null
    if ClassDB.class_exists("SqliteDataStore"):
        db = ClassDB.instantiate("SqliteDataStore")
    else:
        var s = load("res://Game.Godot/Adapters/SqliteDataStore.cs")
        db = Node.new()
        db.set_script(s)
    db.name = name
    get_tree().get_root().add_child(auto_free(db))
    await get_tree().process_frame
    if not db.has_method("TryOpen"):
        await get_tree().process_frame
    return db

func _force_managed() -> void:
    var helper = preload("res://Game.Godot/Adapters/Db/DbTestHelper.cs").new()
    add_child(auto_free(helper))
    helper.ForceManaged()

func _new_panel() -> Node:
    var packed = load("res://Game.Godot/Scenes/UI/SettingsPanel.tscn")
    if packed == null:
        push_warning("SKIP: SettingsPanel.tscn not found")
        return null
    var panel = packed.instantiate()
    add_child(auto_free(panel))
    await get_tree().process_frame
    return panel

func _select_lang(panel: Node, code: String) -> void:
    var lang_opt = panel.get_node("VBox/LangRow/LangOpt")
    if lang_opt.get_item_count() == 0:
        lang_opt.add_item("en"); lang_opt.add_item("zh"); lang_opt.add_item("ja")
    var idx := -1
    for i in range(lang_opt.get_item_count()):
        if str(lang_opt.get_item_text(i)).to_lower() == code.to_lower():
            idx = i
            break
    if idx != -1:
        lang_opt.select(idx)
        # trigger runtime apply
        lang_opt.emit_signal("item_selected", idx)

func test_settings_locale_persist_cross_restart_via_db() -> void:
    var path = "user://utdb_%s/settings.db" % Time.get_unix_time_from_system()
    _force_managed()
    var db = await _new_db("SqlDb")
    assert_bool(db.TryOpen(path)).is_true()
    db.Execute("CREATE TABLE IF NOT EXISTS settings(user_id TEXT PRIMARY KEY, audio_volume REAL, graphics_quality TEXT, language TEXT, updated_at INTEGER);")

    var panel = await _new_panel()
    if panel == null:
        return
    _select_lang(panel, "zh")
    var save_btn = panel.get_node("VBox/Buttons/SaveBtn")
    save_btn.emit_signal("pressed")
    await get_tree().process_frame
    assert_str(TranslationServer.get_locale()).contains("zh")

    # close and reopen db
    db.Close()
    await get_tree().process_frame
    var db2 = await _new_db("SqlDb2")
    assert_bool(db2.TryOpen(path)).is_true()

    var panel2 = await _new_panel()
    var load_btn = panel2.get_node("VBox/Buttons/LoadBtn")
    load_btn.emit_signal("pressed")
    await get_tree().process_frame
    assert_str(TranslationServer.get_locale()).contains("zh")

