#!/bin/bash

# Merge split oplus camera app
if [ ! -f "vendor/oplus/camera/proprietary/system_ext/priv-app/OplusCamera/OplusCamera.apk" ]; then
    cat vendor/oplus/camera/proprietary/system_ext/priv-app/OplusCamera/OplusCamera.apk.part* > vendor/oplus/camera/proprietary/system_ext/priv-app/OplusCamera/OplusCamera.apk
fi

# Automate OplusCamera APK Patching
patch_camera_apk() {
    local apk_dir="vendor/oplus/camera/proprietary/system_ext/priv-app/OplusCamera"
    local decompiled_dir="vendor/oplus/camera/OplusCamera_decompiled"
    local apktool_jar="prebuilts/extract-tools/common/apktool/apktool.jar"
    local frame_dir="vendor/oplus/camera/.apktool_framework"
    local marker="vendor/oplus/camera/.patched_camera_apk"

    mkdir -p "$frame_dir"

    # Decompile if not already decompiled
    if [ ! -d "$decompiled_dir" ]; then
        echo "OplusCamera: Decompiling stock APK (this may take a moment)..."
        java -jar "$apktool_jar" d --frame-path "$frame_dir" "${apk_dir}/OplusCamera.apk" -o "$decompiled_dir"
        rm -f "$marker"
    fi

    # Run the Python patching script
    python3 vendor/oplus/camera/patch_camera.py "$decompiled_dir"
    local patch_status=$?

    if [ ! -f "$marker" ] || [ $patch_status -eq 10 ]; then
        echo "OplusCamera: Rebuilding patched APK..."
        java -jar "$apktool_jar" b --frame-path "$frame_dir" "$decompiled_dir" -o "${apk_dir}/OplusCamera.apk"
        touch "$marker"
        echo "OplusCamera: Patched and rebuilt successfully."
    else
        echo "OplusCamera: APK already patched (no changes)."
    fi
}

# Automate OplusCamera SDK Jar Patching
patch_camera_sdk() {
    local sdk_dir="vendor/oplus/camera/proprietary/system_ext/framework"
    local decompiled_dir="vendor/oplus/camera/com.oplus.camera.unit.sdk_decompiled"
    local apktool_jar="prebuilts/extract-tools/common/apktool/apktool.jar"
    local frame_dir="vendor/oplus/camera/.apktool_framework"
    local marker="vendor/oplus/camera/.patched_camera_sdk"

    mkdir -p "$frame_dir"

    # Decompile if not already decompiled
    if [ ! -d "$decompiled_dir" ]; then
        echo "OplusCameraSDK: Decompiling stock SDK jar (this may take a moment)..."
        java -jar "$apktool_jar" d --frame-path "$frame_dir" "${sdk_dir}/com.oplus.camera.unit.sdk.jar" -o "$decompiled_dir"
        rm -f "$marker"
    fi

    # Run the Python patching script
    python3 vendor/oplus/camera/patch_camera.py "$decompiled_dir"
    local patch_status=$?

    if [ ! -f "$marker" ] || [ $patch_status -eq 10 ]; then
        echo "OplusCameraSDK: Rebuilding patched SDK jar..."
        java -jar "$apktool_jar" b --frame-path "$frame_dir" "$decompiled_dir" -o "${sdk_dir}/com.oplus.camera.unit.sdk.jar"
        touch "$marker"
        echo "OplusCameraSDK: Patched and rebuilt successfully."
    else
        echo "OplusCameraSDK: SDK jar already patched (no changes)."
    fi
}

patch_camera_apk
patch_camera_sdk
