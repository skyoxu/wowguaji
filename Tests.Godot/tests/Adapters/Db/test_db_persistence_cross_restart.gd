extends "res://addons/gdUnit4/src/GdUnitTestSuite.gd"

func _new_db(name: String) -> Node:
    var db = preload("res://Game.Godot/Adapters/SqliteDataStore.cs").new()
    db.name = name
    get_tree().get_root().add_child(auto_free(db))
    return db

func test_cross_restart_persists_rows() -> void:
    # unique DB path per run
    var path = "user://utdb_%s/persist.db" % Time.get_unix_time_from_system()
    # first open and write
    var db1 = _new_db("SqlDb1")
    var ok1 = db1.TryOpen(path)
    assert_bool(ok1).is_true()
    # use repository bridge to persist a user row (schema via helper)
    var helper = preload("res://Game.Godot/Adapters/Db/DbTestHelper.cs").new()
    add_child(auto_free(helper))
    helper.CreateSchema()
    var bridge1 = preload("res://Game.Godot/Adapters/Db/RepositoryTestBridge.cs").new()
    add_child(auto_free(bridge1))
    var ok_ins = bridge1.UpsertUser("persist_user")
    assert_bool(ok_ins).is_true()
    # close first instance
    db1.Close()
    await get_tree().process_frame
    
    # reopen same path with a fresh instance
    var db2 = _new_db("SqlDb2")
    var ok2 = db2.TryOpen(path)
    assert_bool(ok2).is_true()
    var bridge2 = preload("res://Game.Godot/Adapters/Db/RepositoryTestBridge.cs").new()
    add_child(auto_free(bridge2))
    var uname = bridge2.FindUser("persist_user")
    assert_str(str(uname)).is_equal("persist_user")
